import json
import unittest
import os
import sys
from utils import json_string_from_file, text_from_file, extract_json_array, lines_to_json


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.valid_json_file = "test_valid.json"
        data = {"name": "Alice", "age": 30}
        with open(self.valid_json_file, "w") as f:
            json.dump(data, f)

        self.invalid_json_file = "test_invalid.json"
        with open(self.invalid_json_file, "w") as f:
            f.write("not json data")

        self.text_file = "test_text.txt"
        text = "line 1\nline 2\nline 3"
        with open(self.text_file, "w") as f:
            f.write(text)

    def tearDown(self):
        files = [self.valid_json_file, self.invalid_json_file, self.text_file]
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    def test_json_string_from_file(self):
        expected_output = '{"name": "Alice", "age": 30}'
        self.assertEqual(json_string_from_file(self.valid_json_file), expected_output)

        with self.assertRaises(json.JSONDecodeError):
            json_string_from_file(self.invalid_json_file)

        with open("test_json_with_newlines.json", "w") as f:
            f.write('{"name": "Bob",\n "age": 40}\n')
        expected_output = '{"name": "Bob", "age": 40}'
        self.assertEqual(json_string_from_file("test_json_with_newlines.json"), expected_output)

    def test_text_from_file(self):
        expected_output = "line 1\nline 2\nline 3"
        self.assertEqual(text_from_file(self.text_file), expected_output)

        with open("test_text_with_whitespace.txt", "w") as f:
            f.write("   line 1\nline 2\nline 3    \n")
        expected_output = "line 1\nline 2\nline 3"
        self.assertEqual(text_from_file("test_text_with_whitespace.txt"), expected_output)

        with open("test_text_with_newlines.txt", "w") as f:
            f.write("\nline 1\nline 2\nline 3\n")
        expected_output = "line 1\nline 2\nline 3"
        self.assertEqual(text_from_file("test_text_with_newlines.txt"), expected_output)

    def test_extract_json_array(self):
        raw = 'The JSON array: [{"title": "t1"}, {"title": "t2"}]'
        expected_output = json.loads('[{"title": "t1"}, {"title": "t2"}]')
        self.assertEqual(extract_json_array(raw), expected_output)

        raw = '[{"title": "t1"}, {"title": "t2"}]'
        expected_output = json.loads('[{"title": "t1"}, {"title": "t2"}]')
        self.assertEqual(extract_json_array(raw), expected_output)

    def test_lines_to_json(self):
        raw = "line 1\nline 2\nline 3"
        expected_output = [
            {"title": "line 1"},
            {"title": "line 2"},
            {"title": "line 3"},
        ]
        self.assertEqual(lines_to_json(raw), expected_output)

        raw = "\n\n"
        expected_output = []
        self.assertEqual(lines_to_json(raw), expected_output)

        raw = "line 1\n\nline 2\nline 3\n\n"
        expected_output = [
            {"title": "line 1"},
            {"title": "line 2"},
            {"title": "line 3"},
        ]
        self.assertEqual(lines_to_json(raw), expected_output)

