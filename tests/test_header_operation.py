import unittest
from kiss_headers import Header


class MyKissHeaderOperation(unittest.TestCase):
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

    def test_complex_second_attr_removal(self):
        content_type = Header(
            "Content-Type",
            'text/html; format=flowed; charset="utf-8"; format=flowed; format="origin";',
        )

        del content_type.format

        self.assertEqual('text/html;  charset="utf-8"', str(content_type))

    def test_simple_attr_add(self):

        content_type = Header("Content-Type", 'text/html; charset="utf-8"')

        self.assertNotIn("format", content_type)

        content_type.format = "flowed"

        self.assertIn("format", content_type)

        self.assertEqual("flowed", content_type.format)

        self.assertEqual('text/html; charset="utf-8"; format="flowed"', content_type)


if __name__ == "__main__":
    unittest.main()
