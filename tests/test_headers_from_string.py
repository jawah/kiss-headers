import unittest
from kiss_headers import Headers, parse_it

RAW_HEADERS = """accept-ch: DPR
accept-ch-lifetime: 2592000
alt-svc: quic=":443"; ma=2592000; v="46,43",h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000
cache-control: private, max-age=0
content-encoding: br
content-length: 64032
content-type: text/html; charset=UTF-8
date: Mon, 16 Mar 2020 21:27:31 GMT
expires: -1
p3p: CP="This is not a P3P policy! See g.co/p3phelp for more info."
server: gws
set-cookie: 1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; SameSite=none
set-cookie: NID=200=IGpBMMA3G7tki0niFFATFQ2BnsNceVP6XBtwOutoyw97AJ4_YFT5l1oLfLeX22xeI_STiP4omAB4rmMP3Sxgyo287ldQGwdZSdPOOZ_Md3roDOMAOtXEQ_hFbUvo0VPjS2gL1y00_6kQwpVxCghI2Ozrx-A4Xks3ZIXRj11RsWs; expires=Tue, 15-Sep-2020 21:27:31 GMT; path=/; domain=.google.fr; Secure; HttpOnly; SameSite=none
set-cookie: CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr
status: 200
strict-transport-security: max-age=31536000
x-frame-options: SAMEORIGIN
x-xss-protection: 0"""

RAW_HEADERS_MOZILLA = """GET /home.html HTTP/1.1
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/testpage.html
Connection: keep-alive
Upgrade-Insecure-Requests: 1
If-Modified-Since: Mon, 18 Jul 2016 02:36:04 GMT
If-None-Match: "c561c68d0ba92bbeb8b0fff2a9199f722e3a621a"
Cache-Control: max-age=0"""


class MyKissHeadersFromStringTest(unittest.TestCase):

    headers: Headers

    def setUp(self) -> None:
        MyKissHeadersFromStringTest.headers = parse_it(RAW_HEADERS)

    def test_two_headers_eq(self):

        self.assertEqual(MyKissHeadersFromStringTest.headers, parse_it(RAW_HEADERS))

        self.assertNotEqual(
            MyKissHeadersFromStringTest.headers, parse_it(RAW_HEADERS_MOZILLA)
        )

    def test_headers_get_has(self):

        self.assertIsNone(MyKissHeadersFromStringTest.headers.get("received"))
        self.assertFalse(MyKissHeadersFromStringTest.headers.has("received"))

        self.assertEqual(
            "SAMEORIGIN", MyKissHeadersFromStringTest.headers.get("x-frame-options")
        )

    def test_repr_dict(self):

        dict_ = MyKissHeadersFromStringTest.headers.to_dict()

        self.assertIn("set-cookie", dict_)

        self.assertIn("p3p", dict_)

        self.assertTrue(
            dict_["set-cookie"].startswith(
                "1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT; path=/;"
            )
        )

        self.assertTrue(
            dict_["set-cookie"].endswith(
                "CONSENT=WP.284b10; expires=Fri, 01-Jan-2038 00:00:00 GMT; path=/; domain=.google.fr"
            )
        )

    def test_repr_str(self):

        self.assertEqual(RAW_HEADERS, repr(MyKissHeadersFromStringTest.headers))

        self.assertEqual(RAW_HEADERS, str(MyKissHeadersFromStringTest.headers))

        self.assertEqual(
            "SAMEORIGIN", str(MyKissHeadersFromStringTest.headers.x_frame_options)
        )

        self.assertEqual(
            "x-frame-options: SAMEORIGIN",
            repr(MyKissHeadersFromStringTest.headers.x_frame_options),
        )

    def test_control_basis_exist(self):

        self.assertEqual("DPR", MyKissHeadersFromStringTest.headers.accept_ch)

        self.assertEqual(3, len(MyKissHeadersFromStringTest.headers.set_cookie))

        self.assertIn("Secure", MyKissHeadersFromStringTest.headers.set_cookie[0])

        self.assertEqual(
            "This is not a P3P policy! See g.co/p3phelp for more info.",
            MyKissHeadersFromStringTest.headers.p3p.cp,
        )

        self.assertTrue(MyKissHeadersFromStringTest.headers.has("Cache-Control"))

        self.assertTrue(MyKissHeadersFromStringTest.headers.content_type.has("charset"))

        self.assertEqual(
            "UTF-8", MyKissHeadersFromStringTest.headers.content_type.get("charset")
        )

    def test_control_first_line_not_header(self):

        headers = parse_it(RAW_HEADERS_MOZILLA)

        self.assertEqual(11, len(headers))

        self.assertIn("host", headers)

        self.assertIn("Cache-Control", headers)


if __name__ == "__main__":
    unittest.main()