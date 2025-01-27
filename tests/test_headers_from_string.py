from __future__ import annotations

import unittest

from kiss_headers import Header, Headers, lock_output_type, parse_it
from kiss_headers.utils import decode_partials

RAW_HEADERS = """accept-ch: DPR
accept-ch-lifetime: 2592000
alt-svc: quic=":443"; ma=2592000; v="46,43", h3-Q050=":443"; ma=2592000, h3-Q049=":443"; ma=2592000, h3-Q048=":443"; ma=2592000, h3-Q046=":443"; ma=2592000, h3-Q043=":443"; ma=2592000
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
x-xss-protection: 0""".replace("\n", "\r\n")

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
Cache-Control: max-age=0""".replace("\n", "\r\n")

RAW_HEADERS_WITH_CONNECT = """HTTP/1.1 200 Connection established

HTTP/2 200
date: Tue, 28 Sep 2021 13:45:34 GMT
content-type: application/epub+zip
content-length: 3706401
content-disposition: filename=ipython-readthedocs-io-en-stable.epub
x-amz-id-2: 2PO2WHP4qGqkhyC1VbRE2KLN2g4uk38vYzaNJDU/OBSxh4lUtYgERD2FNAOPkKPD1a6rsNBMeKI=
x-amz-request-id: 21E21R71FAY4WQKT
last-modified: Sat, 25 Sep 2021 00:43:37 GMT
etag: "6f512f04591f7667486d044c54708448"
x-served: Nginx-Proxito-Sendfile
x-backend: web-i-078619706c1392c2c
x-rtd-project: ipython
x-rtd-version: stable
x-rtd-path: /proxito/epub/ipython/stable/ipython.epub
x-rtd-domain: ipython.readthedocs.io
x-rtd-version-method: path
x-rtd-project-method: subdomain
referrer-policy: no-referrer-when-downgrade
permissions-policy: interest-cohort=()
strict-transport-security: max-age=31536000; includeSubDomains; preload
cf-cache-status: HIT
age: 270
expires: Tue, 28 Sep 2021 15:45:34 GMT
cache-control: public, max-age=7200
accept-ranges: bytes
expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
server: cloudflare
cf-ray: 695d69b549330686-LHR""".replace("\n", "\r\n")


class MyKissHeadersFromStringTest(unittest.TestCase):
    headers: Headers

    def setUp(self) -> None:
        MyKissHeadersFromStringTest.headers = parse_it(RAW_HEADERS)

    def test_decode_partials(self):
        self.assertEqual(
            [("Subject", "pöstal")],
            decode_partials([("Subject", "=?iso-8859-1?q?p=F6stal?=")]),
        )

    def test_bytes_headers(self):
        self.assertEqual(
            MyKissHeadersFromStringTest.headers, parse_it(RAW_HEADERS.encode("utf-8"))
        )

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

        self.assertEqual(17, len(headers))

        self.assertIn("host", headers)

        self.assertIn("Cache-Control", headers)

    def test_headers_to_bytes(self):
        headers = parse_it(RAW_HEADERS_MOZILLA)

        self.assertEqual(headers, parse_it(bytes(headers)))

    def test_verify_autocompletion_capability(self):
        headers = parse_it(RAW_HEADERS_MOZILLA)

        self.assertIn("accept_encoding", dir(headers))

        self.assertIn("accept_language", dir(headers))

        self.assertTrue(headers.accept)

        self.assertIn("q", dir(headers.accept[-1]))

    def test_fixed_type_output(self):
        headers = parse_it(RAW_HEADERS_MOZILLA)

        self.assertEqual(Header, type(headers.host))

        lock_output_type()

        self.assertEqual(list, type(headers.host))

        self.assertEqual(1, len(headers.host))

        self.assertEqual(list, type(headers.accept[-1].q))

        lock_output_type(False)

        self.assertEqual(Header, type(headers.host))

        self.assertEqual(str, type(headers.accept[-1].q))

    def test_parse_with_extra_connect(self):
        headers: Headers = parse_it(RAW_HEADERS_WITH_CONNECT)

        self.assertTrue("Date" in headers)
        self.assertTrue("Server" in headers)


if __name__ == "__main__":
    unittest.main()
