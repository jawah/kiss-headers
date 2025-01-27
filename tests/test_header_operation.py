from __future__ import annotations

import unittest

from kiss_headers import Header


class MyKissHeaderOperation(unittest.TestCase):
    def test_isub_adjective_error(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertNotIn("text/xml", content_type)

        with self.assertRaises(ValueError):
            content_type = content_type - "text/xml"

        with self.assertRaises(TypeError):
            content_type = content_type - 1

    def test_isub_adjective(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertIn("text/html", content_type)

        content_type = content_type - "text/html"

        self.assertNotIn("text/html", content_type)

        self.assertEqual('charset="utf-8"', str(content_type))

    def test_iadd_adjective(self):
        content_type = Header("Content-Type", 'charset="utf-8"')

        self.assertNotIn("text/html", content_type)

        content_type = content_type + "text/html"

        self.assertIn("text/html", content_type)

        self.assertEqual('charset="utf-8"; text/html', str(content_type))

    def test_subtract_adjective(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertIn("text/html", content_type)

        content_type -= "text/html"

        self.assertNotIn("text/html", content_type)

        self.assertEqual('charset="utf-8"', str(content_type))

    def test_add_adjective(self):
        content_type = Header("Content-Type", 'charset="utf-8"')

        self.assertNotIn("text/html", content_type)

        content_type += "text/html"

        self.assertIn("text/html", content_type)

        self.assertEqual('charset="utf-8"; text/html', str(content_type))

    def test_simple_attr_removal(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertIn("charset", content_type)

        self.assertEqual("utf-8", content_type.charset)

        del content_type.charset

        self.assertNotIn("charset", content_type)

        self.assertEqual(str(content_type), "text/html")

    def test_complex_attr_removal(self):
        content_type = Header(
            "Content-Type",
            'text/html; charset="utf-8"; format=flowed; format="origin";',
        )

        del content_type.format

        self.assertEqual('text/html; charset="utf-8"', str(content_type))

        with self.assertRaises(AttributeError):
            del content_type.format

        del content_type["charset"]

        self.assertEqual("text/html", str(content_type))

        with self.assertRaises(KeyError):
            del content_type["charset"]

    def test_complex_second_attr_removal(self):
        content_type = Header(
            "Content-Type",
            'text/html; format=flowed; charset="utf-8"; format=flowed; format="origin";',
        )

        del content_type.format

        self.assertEqual('text/html; charset="utf-8"', str(content_type))

    def test_simple_attr_add(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertNotIn("format", content_type)

        content_type.format = "flowed"

        self.assertIn("format", content_type)

        self.assertEqual("flowed", content_type.format)

        self.assertEqual('text/html; charset="utf-8"; format="flowed"', content_type)

    def test_contain_space_delimiter(self):
        authorization = Header("Authorization", "Bearer mysupersecrettoken")

        self.assertIn("Bearer", authorization)

        self.assertIn("beaRer", authorization)

        self.assertNotIn("beare", authorization)

        self.assertFalse(authorization == "Bearer")

        self.assertTrue(authorization == "bearer mysupersecrettoken")

        self.assertFalse(authorization == "basic mysupersecrettoken")

    def test_illegal_delitem_operation(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        with self.subTest("Forbid to remove non-valued attr using delitem"):
            with self.assertRaises(KeyError):
                del content_type["text/html"]

    def test_attrs_access_case_insensitive(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        with self.subTest("Verify that attrs can be accessed no matter case"):
            self.assertEqual("utf-8", content_type.charset)
            self.assertEqual("utf-8", content_type.charseT)
            self.assertEqual("utf-8", content_type.CHARSET)

        with self.subTest("Using del on attr using case insensitive key"):
            del content_type.CHARSET
            self.assertNotIn("charset", content_type)

    def test_remove_exclusively_none_attrs(self):
        content_type = Header(
            "Content-Type", 'text/html; charset="utf-8"; text/html=Ahah'
        )

        with self.subTest("Trying to subtract 'text/html' member ONLY."):
            content_type -= "text/html"
            self.assertEqual('charset="utf-8"; text/html="Ahah"', str(content_type))

    def test_remove_exclusively_valued_attrs(self):
        content_type = Header("Content-Type", 'text/html; charset="utf-8"; charset')

        with self.subTest("Trying to subtract 'charset' attrs ONLY."):
            del content_type.charset
            self.assertEqual("text/html; charset", str(content_type))


if __name__ == "__main__":
    unittest.main()
