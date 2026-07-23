import tempfile
import unittest
from pathlib import Path

import app


class CameraOpacitySwitchTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        self.engine = app.ShowEngine()

    def tearDown(self):
        app.CONFIG_PATH = self.original_config_path
        self.tempdir.cleanup()

    def test_camera_opacity_command_is_binary_off_on(self):
        self.engine.update_config({"camera_opacity_addresses": {"main_box": "/composition/layers/1/video/opacity"}})
        sent = []
        self.engine.send_osc_float = lambda config, address, value, log_send=True: sent.append((address, value))

        off = self.engine.camera_opacity_trigger("main_box", 49)
        on = self.engine.camera_opacity_trigger("main_box", 50)

        self.assertEqual(off["sent"][0]["display"], "0%")
        self.assertEqual(on["sent"][0]["display"], "100%")
        self.assertEqual(sent, [("/composition/layers/1/video/opacity", 0.0), ("/composition/layers/1/video/opacity", 1.0)])


if __name__ == "__main__":
    unittest.main()
