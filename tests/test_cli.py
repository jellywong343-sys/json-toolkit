import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from json_toolkit.cli import differences, load_json, query, render

class JsonToolkitTests(unittest.TestCase):
    def test_render_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text('{"b":2,"a":1}', encoding="utf-8")
            data = load_json(path)
            self.assertEqual(render(data, sort_keys=True).splitlines()[1].strip(), '"a": 1,')
            self.assertEqual(render(data, compact=True), '{"b":2,"a":1}')

    def test_diff_and_query(self):
        left = {"user": {"name": "A"}, "items": [1, 2]}
        right = {"user": {"name": "B"}, "items": [1, 3], "active": True}
        paths = {item["path"] for item in differences(left, right)}
        self.assertEqual(paths, {"$.active", "$.items[1]", "$.user.name"})
        self.assertEqual(query(right, "items[1]"), 3)

if __name__ == "__main__":
    unittest.main()
