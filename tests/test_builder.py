import unittest
from kiss_headers.builder import *
from email import utils


class MyBuilderTestCase(unittest.TestCase):
    def test_custom_header_expect(self):

        with self.assertRaises(NotImplementedError):
            k = CustomHeader("Should absolutely not work !")

    def test_content_type(self):

        self.assertEqual(
            repr(ContentType("application/json", charset="utf-8")),
            'Content-Type: application/json; charset="utf-8"',
        )

    def test_set_cookie(self):

        dt = datetime.now()

        self.assertEqual(
            repr(SetCookie("MACHINE_IDENTIFIANT", "ABCDEFGHI", expires=dt)),
            'Set-Cookie: MACHINE_IDENTIFIANT="ABCDEFGHI"; expires="{dt}"; HttpOnly'.format(
                dt=utils.format_datetime(dt)
            ),
        )

    def test_content_length(self):

        self.assertEqual(repr(ContentLength(1881)), "Content-Length: 1881")

    def test_content_disposition(self):

        self.assertEqual(
            repr(ContentDisposition(is_attachment=True, filename="test-file.json")),
            'Content-Disposition: attachment; filename="test-file.json"',
        )


if __name__ == "__main__":
    unittest.main()
