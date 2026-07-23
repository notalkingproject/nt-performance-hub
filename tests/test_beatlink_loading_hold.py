import tempfile
import unittest
from pathlib import Path

import app


class BeatLinkLoadingHoldTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        self.engine = app.ShowEngine()
        self.engine.update_config({"blt_params_url": "http://beatlink.test/params.json"})

    def tearDown(self):
        app.CONFIG_PATH = self.original_config_path
        self.tempdir.cleanup()

    def test_loading_metadata_keeps_previous_valid_master_track(self):
        valid_context = {
            "title": "Real Track",
            "artist": "Real Artist",
            "album": "Real Album",
            "full_track": "Real Artist - Real Track",
            "track_info": "128 BPM | Player 1 | CDJ-3000",
            "bpm": "128",
            "tempo": "128",
            "player_number": "1",
            "device_name": "CDJ-3000",
            "source_player": "1",
            "player": "Player 1",
            "comment": "",
            "track_id": "real-track-id",
            "track_number": "42",
        }
        loading_context = {
            "title": "",
            "artist": "",
            "album": "",
            "full_track": "Loaded track",
            "track_info": "153 BPM | Player 1 | CDJ-3000",
            "bpm": "153",
            "tempo": "153",
            "player_number": "1",
            "device_name": "CDJ-3000",
            "source_player": "1",
            "player": "Player 1",
            "comment": "",
            "track_id": "",
            "track_number": "",
        }
        contexts = [valid_context, loading_context]
        artwork_calls = []
        sent = []
        self.engine.fetch_blt_context = lambda source=None: contexts.pop(0) if contexts else loading_context
        self.engine.update_track_artwork = lambda context, track_key, force=False: artwork_calls.append((context, track_key)) or context
        self.engine.send_blt_outputs = lambda context, source: sent.append((context, source)) or []

        first = self.engine.poll_blt(send_on_change=True)
        self.assertTrue(first["ok"])
        self.assertEqual(self.engine.latest_blt_context["full_track"], "Real Artist - Real Track")
        self.assertEqual(len(artwork_calls), 1)
        self.assertEqual(len(sent), 1)

        second = self.engine.poll_blt(send_on_change=True)
        self.assertFalse(second["ok"])
        self.assertFalse(second.get("changed", False))
        self.assertEqual(second["context"]["full_track"], "Real Artist - Real Track")
        self.assertEqual(self.engine.latest_blt_context["full_track"], "Real Artist - Real Track")
        self.assertEqual(len(artwork_calls), 1)
        self.assertEqual(len(sent), 1)

    def test_artwork_matcher_ignores_loading_placeholder(self):
        self.assertFalse(self.engine.is_valid_blt_track_context({"full_track": "Loaded track", "title": "", "artist": ""}))


if __name__ == "__main__":
    unittest.main()
