from __future__ import annotations

import unittest

from kiss_headers import Attributes
from kiss_headers.utils import header_content_split


class AttributesTestCase(unittest.TestCase):
    def test_eq(self):
        with self.subTest(
            "Ensure that Attributes instances are compared the correct way"
        ):
            attr_a = Attributes(["a", "p=8a", "a", "XX"])
            attr_b = Attributes(["p=8a", "a", "a", "XX"])
            attr_c = Attributes(["p=8a", "a", "A", "Xx"])
            attr_d = Attributes(["p=8a", "a", "A", "Xx", "XX=a"])
            attr_e = Attributes(["p=8A", "a", "A", "Xx"])

            self.assertEqual(attr_a, attr_b)

            self.assertEqual(attr_a, attr_c)

            self.assertNotEqual(attr_a, attr_d)

            self.assertNotEqual(attr_a, attr_e)

    def test_esc_double_quote(self):
        with self.subTest(
            "Ensure that the double quote character is handled correctly."
        ):
            attributes = Attributes(
                header_content_split(r'text/html; charset="UTF-\"8"', ";")
            )

            self.assertEqual(attributes["charset"], 'UTF-"8')

            self.assertEqual(str(attributes), r'text/html; charset="UTF-\"8"')


if __name__ == "__main__":
    unittest.main()
