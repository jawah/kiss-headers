from __future__ import annotations

import unittest

from kiss_headers import parse_it


class MyKissHeadersReservedKeyword(unittest.TestCase):
    def test_reserved_header_name_keyword(self):
        headers = parse_it(
            "From: Ousret; origin=www.github.com\nIS: 1\nWhile: Not-True"
        )

        self.assertIn("From", headers)

        self.assertEqual("Ousret; origin=www.github.com", headers.from_)

        self.assertIn("Ousret", headers.from_)

        self.assertEqual("Not-True", headers.while_)


if __name__ == "__main__":
    unittest.main()
