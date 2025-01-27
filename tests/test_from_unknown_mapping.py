from __future__ import annotations

import unittest

from kiss_headers import parse_it


class UnknownMappingTest(unittest.TestCase):
    def test_parse_with_bytes(self):
        headers = parse_it({"User-Agent": b"Hello!"})

        self.assertTrue("User-Agent" in headers)

    def test_parse_with_None(self):
        headers = parse_it({"User-Agent": None, "Test": "Hello!"})

        self.assertTrue("User-Agent" not in headers)
        self.assertTrue("Test" in headers)

    def test_with_type_madness(self):
        headers = parse_it(
            {
                "User-Agent": b"Hello!",
                "Age": 30,
                "Type": 1.554,
                "BeCrazy": {"pff!": "?"},
                "Again": ["a", 0, 8, -1],
            }
        )

        self.assertTrue("User-Agent" in headers)
        self.assertTrue(headers.get("User-agent").content == "Hello!")
        self.assertTrue(headers.get("Age").content == "30")
        self.assertTrue(headers.get("Again").content == '["a", 0, 8, -1]')
