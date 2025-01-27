from __future__ import annotations

import unittest

from kiss_headers.structures import CaseInsensitiveDict


class MyCaseInsensibleDictTest(unittest.TestCase):
    def test_insensible_key(self):
        k = CaseInsensitiveDict({"abc": 1, "qwerty": 2, "content-TYPE": "json"})

        self.assertIn("content-type", k)

        self.assertIn("content_type", k)

        self.assertIn("ABc", k)

    def test_items(self):
        k = CaseInsensitiveDict({"abc": 1, "qwerty": 2, "content-TYPE": "json"})

        self.assertEqual(
            list(k.items()), [("abc", 1), ("qwerty", 2), ("content-TYPE", "json")]
        )

    def test_eq(self):
        k = CaseInsensitiveDict({"abc": 1, "qwerty": 2, "content-TYPE": "json"})

        self.assertEqual(k, {"abc": 1, "qwerty": 2, "content-TYPE": "json"})

        self.assertEqual(k, k)


if __name__ == "__main__":
    unittest.main()
