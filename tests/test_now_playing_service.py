import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import app


class UnifiedNowPlayingServiceTest(unittest.TestCase):
    def test_normalization_and_public_payload_are_safe(self):
        service = app.UnifiedNowPlayingService()
        changed = service.update_source_state("spotify", {
            "source": "spotify",
            "item_type": "track",
            "track_key": "spotify:track:abc",
            "title": "<b>Song</b>",
            "artist": "Artist",
            "album": "Album",
            "artwork_path": "C:/Users/private/current_artwork.jpg",
            "has_artwork": True,
            "is_playing": True,
            "progress_ms": 83000,
            "duration_ms": 248000,
            "refresh_token": "secret",
            "raw": {"access_token": "secret"},
        })
        self.assertFalse(changed)
        service.activate_source("spotify")
        public = service.get_public_state()
        self.assertEqual(public["source"], "spotify")
        self.assertEqual(public["title"], "<b>Song</b>")
        self.assertEqual(public["artwork_url"], "/api/now-playing/artwork?v=1")
        serialized = json.dumps(public)
        self.assertNotIn("refresh_token", serialized)
        self.assertNotIn("access_token", serialized)
        self.assertNotIn("C:/Users/private", serialized)

    def test_source_authority_and_duplicate_detection(self):
        service = app.UnifiedNowPlayingService()
        service.update_source_state("beatlink", {"title": "CDJ Track", "artist": "DJ", "track_key": "beatlink:1", "is_playing": True})
        service.activate_source("beatlink")
        version = service.get_public_state()["state_version"]
        service.update_source_state("spotify", {"title": "Spotify Track", "artist": "SP", "track_key": "spotify:1", "is_playing": True})
        self.assertEqual(service.get_public_state()["title"], "CDJ Track")
        self.assertEqual(service.get_public_state()["state_version"], version)
        service.activate_source("spotify")
        self.assertEqual(service.get_public_state()["title"], "Spotify Track")
        spotify_version = service.get_public_state()["state_version"]
        service.update_source_state("spotify", {"title": "Spotify Track", "artist": "SP", "track_key": "spotify:1", "is_playing": True})
        self.assertEqual(service.get_public_state()["state_version"], spotify_version)
        service.update_source_state("spotify", {"title": "Spotify Track", "artist": "SP", "track_key": "spotify:1", "is_playing": False})
        self.assertGreater(service.get_public_state()["state_version"], spotify_version)

    def test_invalid_update_does_not_replace_active_state_and_subscriber_gets_event(self):
        service = app.UnifiedNowPlayingService()
        service.update_source_state("manual", {"title": "Manual Title", "track_key": "manual:1", "is_playing": True})
        service.activate_source("manual")
        subscriber_id, events, initial = service.subscribe()
        try:
            self.assertEqual(initial["title"], "Manual Title")
            self.assertFalse(service.update_source_state("manual", "not a dict"))
            self.assertEqual(service.get_public_state()["title"], "Manual Title")
            service.update_source_state("manual", {"title": "Manual Title 2", "track_key": "manual:2", "is_playing": True})
            event = events.get(timeout=1)
            self.assertEqual(event["event"], "now-playing")
            self.assertEqual(event["data"]["title"], "Manual Title 2")
        finally:
            service.unsubscribe(subscriber_id)
        self.assertEqual(service.get_status()["connected_clients"], 0)


class NowPlayingApiTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.original_engine = app.ENGINE
        self.original_admin_token_path = app.ADMIN_TOKEN_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        app.ADMIN_TOKEN_PATH = Path(self.tempdir.name) / "admin_token.txt"
        app.ENGINE = app.ShowEngine()
        app.ENGINE.now_playing.update_source_state("spotify", {"title": "API Song", "artist": "API Artist", "track_key": "spotify:api", "is_playing": True})
        app.ENGINE.now_playing.activate_source("spotify")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), app.AppRequestHandler)
        self.server.bind_host = "127.0.0.1"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        app.ENGINE.stop_macro_scheduler()
        app.ENGINE = self.original_engine
        app.CONFIG_PATH = self.original_config_path
        app.ADMIN_TOKEN_PATH = self.original_admin_token_path
        self.tempdir.cleanup()

    def test_now_playing_endpoint_shape(self):
        with urlopen(f"http://127.0.0.1:{self.server.server_port}/api/now-playing", timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertTrue(payload["ok"])
        state = payload["now_playing"]
        self.assertEqual(state["source"], "spotify")
        self.assertEqual(state["title"], "API Song")
        self.assertIn("artwork_url", state)
        self.assertNotIn("artwork_path", state)
        self.assertNotIn("config", payload)



    def test_private_lan_clients_can_read_settings_without_admin_token(self):
        base = f"http://127.0.0.1:{self.server.server_port}"
        with urlopen(f"{base}/api/status?settings=0&blt=0", timeout=10) as response:
            public_status = json.loads(response.read().decode("utf-8"))
        self.assertNotIn("settings", public_status)
        self.assertIn("now_playing", public_status)

        with urlopen(f"{base}/api/admin/session", timeout=10) as response:
            session = json.loads(response.read().decode("utf-8"))
        self.assertTrue(session["ok"])
        token = session["admin_token"]
        request = Request(f"{base}/api/status?settings=1&blt=0", headers={app.ADMIN_TOKEN_HEADER: token})
        with urlopen(request, timeout=10) as response:
            admin_status = json.loads(response.read().decode("utf-8"))
        self.assertIn("settings", admin_status)
        config_path = admin_status["config"]["path"].replace(chr(92), "/")
        self.assertFalse(config_path.startswith("C:/"))
        self.assertTrue(config_path.endswith("app_config.json"))

if __name__ == "__main__":
    unittest.main()
