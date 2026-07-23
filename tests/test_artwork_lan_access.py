import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

import app


class ArtworkLanAccessTest(unittest.TestCase):
    def test_bracketed_mix_identity_survives_normalization(self):
        track = {"artist": "Pittsburgh Track Authority", "title": "Tech 97 [Manic Mix]"}
        original = app.index_entry_from_mp3_path(Path("Pittsburgh Track Authority - Tech 97 - 01 Tech 97.mp3"))
        manic = app.index_entry_from_mp3_path(Path("Pittsburgh Track Authority - Tech 97 - 02 Tech 97 -Manic Mix-.mp3"))

        self.assertIn("manic", app.make_match_key(track["artist"], track["title"]))
        self.assertGreater(app.score_track_match(track, manic), app.score_track_match(track, original))

    def test_disk_fallback_finds_mp3_missing_from_index(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tempdir:
            music_root = Path(tempdir) / "Music Collection"
            music_root.mkdir()
            (music_root / "Pittsburgh Track Authority - Tech 97 - 01 Tech 97.mp3").touch()
            manic_path = music_root / "Pittsburgh Track Authority - Tech 97 - 02 Tech 97 -Manic Mix-.mp3"
            manic_path.touch()
            (music_root / "Pittsburgh Track Authority - Tech 97 - 03 Tech 97 -Calm Mix-.mp3").touch()

            match = app.find_best_track_match_on_disk(
                {"artist": "Pittsburgh Track Authority", "title": "Tech 97 [Manic Mix]"},
                music_root,
            )

        self.assertIsNotNone(match)
        entry, score = match
        self.assertEqual(Path(entry["path"]).name, manic_path.name)
        self.assertGreaterEqual(score, 0.72)


    def test_now_playing_display_route_serves_html_and_api(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.AppRequestHandler)
        server.bind_host = "127.0.0.1"
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            with urlopen(f"{base}/display/now-playing", timeout=3) as response:
                html = response.read().decode("utf-8")
            self.assertIn("Now Playing Display", html)

            with urlopen(f"{base}/api/now-playing", timeout=3) as response:
                payload = json.loads(response.read().decode("utf-8"))
            self.assertTrue(payload["ok"])
            self.assertIn("now_playing", payload)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_admin_session_reports_no_token_required_for_lan_mode(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.AppRequestHandler)
        server.bind_host = "127.0.0.1"
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            with urlopen(f"{base}/api/admin/session", timeout=3) as response:
                session = json.loads(response.read().decode("utf-8"))
            self.assertTrue(session["ok"])
            self.assertFalse(session["admin_required"])
            self.assertEqual(session["admin_token"], "")

            with urlopen(f"{base}/api/status?settings=1&blt=0", timeout=3) as response:
                status = json.loads(response.read().decode("utf-8"))
            self.assertIn("settings", status)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
