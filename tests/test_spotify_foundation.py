import tempfile
import time
import unittest
from pathlib import Path

import app


def spotify_track_payload(title="Neon Transit", artist="Signal Pattern", album="After Hours", is_playing=True, progress_ms=83000):
    slug = title.lower().replace(" ", "-")
    return {
        "source": "spotify",
        "item_type": "track",
        "track_id": slug,
        "track_uri": f"spotify:track:{slug}",
        "title": title,
        "artist": artist,
        "album": album,
        "artwork_url": "",
        "duration_ms": 248000,
        "progress_ms": progress_ms,
        "is_playing": is_playing,
        "device_name": "Performance Hub Test Player",
        "explicit": False,
    }


def spotify_none_payload():
    return {"source": "spotify", "item_type": "none", "is_playing": False, "device_name": "Performance Hub Test Player"}


class SpotifyFoundationTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.original_token_path = app.SPOTIFY_TOKEN_PATH
        self.original_admin_token_path = app.ADMIN_TOKEN_PATH
        self.original_urlopen = app.urlopen
        self.original_spotify_form_request = app.spotify_form_request
        self.original_spotify_json_get = app.spotify_json_get
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        temp_path = Path(self.tempdir.name)
        app.CONFIG_PATH = temp_path / "app_config.json"
        app.SPOTIFY_TOKEN_PATH = temp_path / "spotify_tokens.json"
        app.ADMIN_TOKEN_PATH = temp_path / "admin_token.txt"
        self.engine = app.ShowEngine()

    def tearDown(self):
        self.engine.stop_spotify_monitor()
        app.urlopen = self.original_urlopen
        app.spotify_form_request = self.original_spotify_form_request
        app.spotify_json_get = self.original_spotify_json_get
        app.CONFIG_PATH = self.original_config_path
        app.SPOTIFY_TOKEN_PATH = self.original_token_path
        app.ADMIN_TOKEN_PATH = self.original_admin_token_path
        self.tempdir.cleanup()

    def test_defaults_and_public_payload_do_not_expose_token_path(self):
        cfg = app.spotify_config({})
        self.assertFalse(cfg["spotify_enabled"])
        self.assertEqual(cfg["spotify_redirect_uri"], "http://127.0.0.1:8080/spotify/callback")
        self.assertEqual(cfg["spotify_market"], "US")
        self.assertEqual(cfg["spotify_track_template"], "{artist} - {title}")
        self.assertTrue(cfg["spotify_keep_last_track_when_paused"])
        self.assertEqual(cfg["spotify_idle_grace_seconds"], 30)
        self.assertFalse(app.spotify_token_status()["connected"])
        payload = self.engine.config_payload()
        self.assertIn("spotify_status", payload)
        self.assertNotIn("spotify_tokens", str(payload))
        self.assertNotIn(str(app.SPOTIFY_TOKEN_PATH), str(payload))

    def test_playback_normalization_states(self):
        playing = app.normalize_spotify_playback(spotify_track_payload())
        self.assertEqual(playing["source"], "spotify")
        self.assertEqual(playing["item_type"], "track")
        self.assertTrue(playing["is_playing"])
        self.assertEqual(playing["title"], "Neon Transit")
        self.assertEqual(playing["artist"], "Signal Pattern")
        self.assertTrue(app.spotify_playback_is_activatable(playing))

        paused = app.normalize_spotify_playback(spotify_track_payload(is_playing=False, progress_ms=121000))
        self.assertFalse(paused["is_playing"])
        self.assertTrue(app.spotify_playback_is_activatable(paused))

        idle = app.normalize_spotify_playback(spotify_none_payload())
        self.assertEqual(idle["item_type"], "none")
        self.assertFalse(app.spotify_playback_is_activatable(idle))

    def test_cached_spotify_track_activates_and_unrelated_save_preserves_config(self):
        saved = self.engine.update_config({
            "spotify_enabled": True,
            "spotify_client_id": "client-id-placeholder",
            "spotify_track_template": "{title} by {artist}",
            "spotify_poll_seconds_playing": "4",
            "spotify_poll_seconds_idle": "9",
            "spotify_idle_grace_seconds": "30",
            "spotify_keep_last_track_when_paused": False,
        })
        self.assertTrue(saved["config"]["spotify_enabled"])
        self.assertEqual(saved["config"]["spotify_track_template"], "{title} by {artist}")

        current = app.normalize_spotify_playback(spotify_track_payload())
        self.engine.spotify_current = current
        self.engine.remember_spotify_track(current)
        self.engine.spotify_last_poll_monotonic = time.monotonic()
        sent_contexts = []
        artwork_calls = []
        self.engine.send_blt_outputs = lambda context, source: sent_contexts.append((context, source)) or [{"label": "Now Playing", "value": context["full_track"]}]
        self.engine.write_spotify_artwork = lambda item: artwork_calls.append(item) or True
        activated = self.engine.activate_spotify_source()
        self.assertTrue(activated["ok"])
        self.assertEqual(activated["state"]["manual_mode"], "spotify")
        self.assertEqual(sent_contexts[0][0]["full_track"], "Neon Transit by Signal Pattern")
        self.assertEqual(sent_contexts[0][1], "Spotify")
        self.assertEqual(artwork_calls[0]["title"], "Neon Transit")
        unrelated = self.engine.update_config({"music_root": "C:/Music"})
        self.assertEqual(unrelated["config"]["spotify_client_id"], "client-id-placeholder")
        self.assertEqual(unrelated["config"]["spotify_track_template"], "{title} by {artist}")
        self.assertFalse(unrelated["config"]["spotify_keep_last_track_when_paused"])

    def test_no_playback_still_selects_spotify(self):
        self.engine.update_config({"spotify_enabled": True, "spotify_market": "GB", "spotify_keep_last_track_when_paused": False})
        self.engine.spotify_current = app.normalize_spotify_playback(spotify_none_payload())
        self.engine.spotify_last_poll_monotonic = time.monotonic()
        sent_contexts = []
        artwork_calls = []
        self.engine.send_blt_outputs = lambda context, source: sent_contexts.append((context, source)) or []
        self.engine.write_spotify_artwork = lambda current: artwork_calls.append(current) or True
        activated = self.engine.activate_spotify_source()
        self.assertTrue(activated["ok"])
        self.assertEqual(activated["state"]["manual_mode"], "spotify")
        self.assertEqual(sent_contexts[0][0]["full_track"], "")
        self.assertEqual(sent_contexts[0][1], "Spotify")
        self.assertEqual(artwork_calls, [])
        self.assertEqual(activated["config"]["spotify_market"], "GB")

    def test_no_active_playback_preserves_recent_track_for_configured_grace(self):
        self.engine.update_config({"spotify_idle_grace_seconds": 30, "spotify_keep_last_track_when_paused": True})
        playing = app.normalize_spotify_playback(spotify_track_payload())
        self.engine.spotify_current = playing
        self.engine.remember_spotify_track(playing)
        self.engine.spotify_current = app.normalize_spotify_playback(spotify_none_payload())
        idle = self.engine.spotify_status()["current"]
        self.assertEqual(idle["title"], "Neon Transit")
        self.assertTrue(idle["preserved"])
        self.assertEqual(idle["preserved_reason"], "no_active_playback")

        self.engine.spotify_last_active_monotonic -= 31
        expired = self.engine.spotify_status()["current"]
        self.assertEqual(expired["item_type"], "none")
        sent_contexts = []
        self.engine.send_blt_outputs = lambda context, source: sent_contexts.append((context, source)) or []
        activated = self.engine.activate_spotify_source()
        self.assertTrue(activated["ok"])
        self.assertEqual(activated["state"]["manual_mode"], "spotify")
        self.assertEqual(sent_contexts[0][0]["full_track"], "")

    def test_same_track_playback_change_updates_unified_display_without_resending_outputs(self):
        self.engine.update_config({"spotify_keep_last_track_when_paused": True})
        current = app.normalize_spotify_playback(spotify_track_payload(is_playing=False, progress_ms=121000))
        self.engine.spotify_current = current
        context = self.engine.spotify_context(current)
        self.engine.manual_mode = "spotify"
        self.engine.latest_spotify_output_key = self.engine.spotify_output_key(current, context)
        self.engine.now_playing.update_source_state("spotify", {"title": current["title"], "artist": current["artist"], "track_key": current["track_key"], "is_playing": False})
        self.engine.now_playing.activate_source("spotify")
        playing = dict(current)
        playing["is_playing"] = True
        playing["progress_ms"] = int(current.get("progress_ms", 0)) + 5000
        self.engine.spotify_current = playing
        self.engine.spotify_last_poll_monotonic = time.monotonic()
        sent_contexts = []
        self.engine.send_blt_outputs = lambda context, source: sent_contexts.append((context, source)) or []
        refreshed = self.engine.refresh_active_spotify_output()
        self.assertIsNone(refreshed)
        self.assertEqual(sent_contexts, [])
        public = self.engine.now_playing.get_public_state()
        self.assertTrue(public["is_playing"])
        self.assertFalse(public["is_paused"])
        self.assertEqual(public["title"], current["title"])

    def test_match_normalization_preserves_bracketed_mix_identity(self):
        track = {"artist": "Pittsburgh Track Authority", "title": "Tech 97 [Manic Mix]"}
        original = {
            "filename": "Pittsburgh Track Authority - Tech 97 - 01 Tech 97",
            "title": "Tech 97",
            "artist": "Pittsburgh Track Authority",
            "match_key": app.make_match_key("Pittsburgh Track Authority", "Tech 97"),
            "fallback_key": app.normalize_match_text("Pittsburgh Track Authority - Tech 97 - 01 Tech 97"),
        }
        manic = {
            "filename": "Pittsburgh Track Authority - Tech 97 - 02 Tech 97 -Manic Mix-",
            "title": "Tech 97 [Manic Mix]",
            "artist": "Pittsburgh Track Authority",
            "match_key": app.make_match_key("Pittsburgh Track Authority", "Tech 97 [Manic Mix]"),
            "fallback_key": app.normalize_match_text("Pittsburgh Track Authority - Tech 97 - 02 Tech 97 -Manic Mix-"),
        }
        self.assertIn("manic", app.make_match_key(track["artist"], track["title"]))
        self.assertGreater(app.score_track_match(track, manic), app.score_track_match(track, original))
    def test_oauth_pkce_login_callback_refresh_and_real_polling_without_secret(self):
        self.engine.update_config({"spotify_enabled": True, "spotify_client_id": "placeholder-client"})
        login = self.engine.spotify_login()
        self.assertTrue(login["ok"])
        self.assertIn("https://accounts.spotify.com/authorize", login["authorization_url"])
        self.assertIn("code_challenge_method=S256", login["authorization_url"])
        self.assertNotIn("client_secret", login["authorization_url"])

        token_requests = []
        def fake_form_request(url, form, headers=None, timeout=0):
            token_requests.append(dict(form))
            if form["grant_type"] == "authorization_code":
                self.assertIn("code_verifier", form)
                self.assertNotIn("client_secret", form)
                return {"access_token": "access-one", "refresh_token": "refresh-one", "expires_in": 1, "scope": app.SPOTIFY_MINIMUM_SCOPE, "token_type": "Bearer"}
            if form["grant_type"] == "refresh_token":
                self.assertEqual(form["refresh_token"], "refresh-one")
                self.assertNotIn("client_secret", form)
                return {"access_token": "access-two", "expires_in": 3600, "scope": app.SPOTIFY_MINIMUM_SCOPE, "token_type": "Bearer"}
            raise AssertionError(f"unexpected grant {form}")

        playback_calls = []
        def fake_json_get(url, access_token, timeout=0):
            playback_calls.append((url, access_token))
            if url.endswith("/v1/me"):
                return 200, {"display_name": "Test Account"}
            return 200, {
                "currently_playing_type": "track",
                "is_playing": True,
                "progress_ms": 12000,
                "item": {
                    "id": "real-track",
                    "uri": "spotify:track:real-track",
                    "name": "Real Track",
                    "duration_ms": 180000,
                    "artists": [{"name": "Real Artist"}],
                    "album": {"name": "Real Album", "images": [{"url": "https://image.example/large.jpg", "width": 640, "height": 640}]},
                },
            }

        app.spotify_form_request = fake_form_request
        app.spotify_json_get = fake_json_get
        callback = self.engine.spotify_callback({"code": ["auth-code"], "state": [self.engine.spotify_oauth_state]})
        self.assertTrue(callback["ok"])
        saved_tokens = app.load_spotify_tokens()
        self.assertEqual(saved_tokens["refresh_token"], "refresh-one")
        self.assertEqual(saved_tokens["account_name"], "Test Account")

        sent_contexts = []
        artwork_calls = []
        self.engine.send_blt_outputs = lambda context, source: sent_contexts.append((context, source)) or []
        self.engine.write_spotify_artwork = lambda current: artwork_calls.append(current) or True
        activated = self.engine.activate_spotify_source()
        self.assertTrue(activated["ok"])
        self.assertEqual(activated["state"]["manual_mode"], "spotify")
        self.assertEqual(artwork_calls[0]["title"], "Real Track")
        self.assertEqual(sent_contexts[0][0]["full_track"], "Real Artist - Real Track")
        self.assertEqual(sent_contexts[0][1], "Spotify")
        self.assertEqual(playback_calls[-1][1], "access-two")
        self.assertTrue(any(request["grant_type"] == "refresh_token" for request in token_requests))


if __name__ == "__main__":
    unittest.main()