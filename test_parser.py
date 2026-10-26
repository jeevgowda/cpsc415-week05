import unittest
import json

class TestParser(unittest.TestCase):
    def test_json_extraction_clean(self):
        # Test clean JSON parsing behavior
        raw = "{\"vendor\": \"Test Store\", \"total\": 15.00}"
        parsed = json.loads(raw)
        self.assertEqual(parsed["vendor"], "Test Store")
        self.assertEqual(parsed["total"], 15.00)

    def test_json_extraction_markdown_fence(self):
        # Test extraction when model wraps JSON in markdown fences
        raw = "```json\n{\"vendor\": \"Cafe\", \"total\": 5.50}\n```"
        cleaned = raw.strip()
        if cleaned.startswith("```json"): cleaned = cleaned[7:]
        if cleaned.endswith("```"): cleaned = cleaned[:-3]
        parsed = json.loads(cleaned.strip())
        self.assertEqual(parsed["vendor"], "Cafe")

if __name__ == "__main__":
    unittest.main()
