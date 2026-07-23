import tempfile
import unittest
from pathlib import Path

import app


class VisualXButtonPersistenceTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        self.engine = app.ShowEngine()

    def tearDown(self):
        app.CONFIG_PATH = self.original_config_path
        self.tempdir.cleanup()

    def visual_by_id(self, config, item_id):
        return next(item for item in config["visual_controls"] if item["id"] == item_id)

    def test_visual_x_buttons_survive_reload_partial_updates_clear_and_trigger(self):
        first_save = self.engine.update_config({
            "visual_controls": {
                "items": {
                    "visual_l1_off": {
                        "id": "visual_l1_off",
                        "kind": "off",
                        "layer": 1,
                        "clip": 0,
                        "name": "L1 X",
                        "label": "L1 X",
                        "address": "/resolume/layer/1/clear",
                    },
                    "visual_l2_off": {
                        "id": "visual_l2_off",
                        "kind": "off",
                        "layer": 2,
                        "clip": 0,
                        "name": "L2 X",
                        "label": "L2 X",
                        "address": "/resolume/layer/2/clear",
                    },
                }
            }
        })
        self.assertEqual(self.visual_by_id(first_save["config"], "visual_l1_off")["address"], "/resolume/layer/1/clear")
        self.assertEqual(self.visual_by_id(first_save["config"], "visual_l2_off")["address"], "/resolume/layer/2/clear")

        disk_config = app.ShowEngine().config_payload()
        self.assertEqual(self.visual_by_id(disk_config, "visual_l1_off")["address"], "/resolume/layer/1/clear")
        self.assertEqual(self.visual_by_id(disk_config, "visual_l2_off")["address"], "/resolume/layer/2/clear")

        unrelated_save = self.engine.update_config({"music_root": "C:/Music"})
        self.assertEqual(self.visual_by_id(unrelated_save["config"], "visual_l1_off")["address"], "/resolume/layer/1/clear")
        self.assertEqual(self.visual_by_id(unrelated_save["config"], "visual_l2_off")["address"], "/resolume/layer/2/clear")

        partial_clip_save = self.engine.update_config({
            "visual_controls": {
                "items": {
                    "visual_1": {
                        "id": "visual_1",
                        "kind": "clip",
                        "layer": 1,
                        "clip": 1,
                        "name": "L1 C1",
                        "label": "L1 C1",
                        "address": "/resolume/layer/1/clip/1/connect",
                    }
                }
            }
        })
        self.assertEqual(self.visual_by_id(partial_clip_save["config"], "visual_l1_off")["address"], "/resolume/layer/1/clear")
        self.assertEqual(self.visual_by_id(partial_clip_save["config"], "visual_l2_off")["address"], "/resolume/layer/2/clear")

        clear_save = self.engine.update_config({
            "visual_controls": {
                "items": {
                    "visual_l1_off": {
                        "id": "visual_l1_off",
                        "kind": "off",
                        "layer": 1,
                        "clip": 0,
                        "name": "L1 X",
                        "label": "L1 X",
                        "address": "",
                    }
                }
            }
        })
        self.assertEqual(self.visual_by_id(clear_save["config"], "visual_l1_off")["address"], "")
        self.assertEqual(self.visual_by_id(clear_save["config"], "visual_l2_off")["address"], "/resolume/layer/2/clear")

        restarted = app.ShowEngine()
        reloaded = restarted.config_payload()
        self.assertEqual(self.visual_by_id(reloaded, "visual_l1_off")["address"], "")
        self.assertEqual(self.visual_by_id(reloaded, "visual_l2_off")["address"], "/resolume/layer/2/clear")

        sent = []
        restarted.send_osc_float = lambda config, address, value, log_send=True: sent.append((address, value))
        trigger_result = restarted.visual_trigger("visual_l2_off")
        self.assertTrue(trigger_result["ok"])
        self.assertEqual(sent, [("/resolume/layer/2/clear", 1.0)])


if __name__ == "__main__":
    unittest.main()