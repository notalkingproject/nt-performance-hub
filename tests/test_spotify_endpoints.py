import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

import app


class SpotifyEndpointTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.original_token_path = app.SPOTIFY_TOKEN_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        app.SPOTIFY_TOKEN_PATH = Path(self.tempdir.name) / "spotify_tokens.json"
        app.ENGINE = app.ShowEngine()
        app.ENGINE.update_config({
            "spotify_enabled": True,
            "spotify_client_id": "client-id-test",
            "spotify_redirect_uri": "http://127.0.0.1:8080/spotify/callback",
        })
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), app.AppRequestHandler)
        self.server.bind_host = "127.0.0.1"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        app.CONFIG_PATH = self.original_config_path
        app.SPOTIFY_TOKEN_PATH = self.original_token_path
        self.tempdir.cleanup()

    def test_spotify_login_endpoint_returns_authorization_url(self):
        with urlopen(f"http://127.0.0.1:{self.server.server_port}/spotify/login", timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertTrue(payload["ok"])
        self.assertIn("https://accounts.spotify.com/authorize", payload["authorization_url"])
        self.assertIn("code_challenge_method=S256", payload["authorization_url"])

    def test_spotify_status_endpoint_returns_shape_without_token(self):
        with urlopen(f"http://127.0.0.1:{self.server.server_port}/api/spotify/status", timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertTrue(payload["ok"])
        self.assertIn("spotify", payload)
        self.assertFalse(payload["spotify"]["connected"])


if __name__ == "__main__":
    unittest.main()
