import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import app


class MacroSystemTest(unittest.TestCase):
    def setUp(self):
        self.original_config_path = app.CONFIG_PATH
        self.tempdir = tempfile.TemporaryDirectory(dir=Path.cwd())
        app.CONFIG_PATH = Path(self.tempdir.name) / "app_config.json"
        self.engine = app.ShowEngine()

    def tearDown(self):
        self.engine.stop_macro_scheduler()
        app.CONFIG_PATH = self.original_config_path
        self.tempdir.cleanup()

    def save_base_config(self, macros):
        return self.engine.update_config({
            "osc_targets": [{"id": "resolume", "label": "Resolume", "host": "127.0.0.1", "port": 7000, "enabled": True}],
            "macros": macros,
        })

    def test_empty_config_and_macro_persistence_updates_delete_and_blank_fields(self):
        self.assertEqual(self.engine.macros_payload(), [])
        result = self.save_base_config([
            {"id": "button_one", "name": "Flash", "type": "osc_button", "enabled": True, "address": "/flash", "value_type": "float", "value": "0.75", "target_ids": ["resolume"]},
            {"id": "clock_one", "name": "Clock", "type": "osc_clock", "enabled": False, "address": "/clock", "time_format": "12h", "prefix": "", "suffix": "", "target_ids": []},
        ])
        macros = result["config"]["macros"]
        self.assertEqual([macro["id"] for macro in macros], ["button_one", "clock_one"])
        self.assertEqual(macros[1]["prefix"], "")
        self.assertEqual(macros[1]["suffix"], "")

        reloaded = app.ShowEngine()
        self.addCleanup(reloaded.stop_macro_scheduler)
        self.assertEqual([macro["id"] for macro in reloaded.macros_payload()], ["button_one", "clock_one"])

        update = self.engine.save_macro({"id": "button_one", "name": "Flash Hard", "type": "osc_button", "enabled": True, "address": "/flash", "value_type": "int", "value": "7", "target_ids": ["resolume"]})
        by_id = {macro["id"]: macro for macro in update["macros"]}
        self.assertEqual(by_id["button_one"]["name"], "Flash Hard")
        self.assertEqual(by_id["clock_one"]["address"], "/clock")

        delete = self.engine.delete_macro("button_one")
        self.assertEqual([macro["id"] for macro in delete["macros"]], ["clock_one"])

    def test_osc_button_trigger_disabled_and_invalid_config(self):
        self.save_base_config([
            {"id": "button_one", "name": "Flash", "type": "osc_button", "enabled": True, "address": "/flash", "value_type": "int", "value": "3", "target_ids": ["resolume"]},
            {"id": "button_disabled", "name": "Muted", "type": "osc_button", "enabled": False, "address": "/muted", "value_type": "trigger", "value": "1"},
            {"id": "button_invalid", "name": "Invalid", "type": "osc_button", "enabled": True, "address": "", "value_type": "trigger", "value": "1"},
        ])
        calls = []
        self.engine.send_osc_typed_value = lambda config, address, value_type, value, target_ids=None, label="OSC macro": calls.append((address, value_type, value, target_ids, label)) or {"address": address, "value": value, "value_type": value_type, "sent_count": 1, "errors": []}
        self.engine.trigger_macro("button_one")
        self.assertEqual(calls[0][:4], ("/flash", "int", 3, ["resolume"]))
        with self.assertRaises(ValueError):
            self.engine.trigger_macro("button_disabled")
        real_engine = app.ShowEngine()
        self.addCleanup(real_engine.stop_macro_scheduler)
        real_engine.update_config({"macros": [{"id": "button_invalid", "name": "Invalid", "type": "osc_button", "enabled": True, "address": "", "value_type": "trigger", "value": "1"}]})
        with self.assertRaises(ValueError):
            real_engine.trigger_macro("button_invalid")

    def test_clock_formatting_dedupe_two_clocks_failure_and_scheduler_singleton(self):
        now = datetime(2026, 7, 21, 21, 42, 30)
        self.assertEqual(app.format_macro_clock_value({"time_format": "12h", "prefix": "LIVE ", "suffix": ""}, now), "LIVE 9:42 PM")
        self.assertEqual(app.format_macro_clock_value({"time_format": "24h", "prefix": "", "suffix": " UTC"}, now), "21:42 UTC")
        self.assertNotIn(":30", app.format_macro_clock_value({"time_format": "24h"}, now))

        self.save_base_config([
            {"id": "clock_12", "name": "Stream Clock", "type": "osc_clock", "enabled": True, "address": "/clock/a", "time_format": "12h", "prefix": "LIVE ", "suffix": "", "target_ids": ["resolume"]},
            {"id": "clock_24", "name": "Backstage Clock", "type": "osc_clock", "enabled": True, "address": "/clock/b", "time_format": "24h", "prefix": "", "suffix": "", "target_ids": ["resolume"]},
            {"id": "clock_off", "name": "Off Clock", "type": "osc_clock", "enabled": False, "address": "/clock/off", "time_format": "24h"},
        ])
        calls = []
        self.engine.send_osc_typed_value = lambda config, address, value_type, value, target_ids=None, label="OSC macro": calls.append((address, value)) or {"address": address, "value": value, "value_type": value_type, "sent_count": 1, "errors": []}
        clocks = {macro["id"]: macro for macro in self.engine.macros_payload()}
        self.engine.send_macro_clock(clocks["clock_12"], now=now)
        self.engine.send_macro_clock(clocks["clock_12"], now=now)
        self.engine.send_macro_clock(clocks["clock_24"], now=now)
        self.engine.send_macro_clock(clocks["clock_off"], now=now)
        self.assertEqual(calls, [("/clock/a", "LIVE 9:42 PM"), ("/clock/b", "21:42")])
        self.engine.send_macro_clock(clocks["clock_12"], now=now + timedelta(minutes=1))
        self.assertEqual(calls[-1], ("/clock/a", "LIVE 9:43 PM"))

        attempts = {"count": 0}
        def flaky_send(config, address, value_type, value, target_ids=None, label="OSC macro"):
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise ValueError("temporary send failure")
            return {"address": address, "value": value, "value_type": value_type, "sent_count": 1, "errors": []}
        self.engine.send_osc_typed_value = flaky_send
        self.engine.send_macro_clock(clocks["clock_24"], now=now + timedelta(minutes=1))
        self.engine.send_macro_clock(clocks["clock_24"], now=now + timedelta(minutes=2))
        self.assertEqual(attempts["count"], 2)
        self.assertEqual(self.engine.macro_status["clock_24"]["error"], "")

        self.engine.ensure_macro_scheduler()
        first_thread = self.engine.macro_scheduler_thread
        self.engine.ensure_macro_scheduler()
        self.assertIs(first_thread, self.engine.macro_scheduler_thread)


if __name__ == "__main__":
    unittest.main()