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


class MyKissHeadersFromStringTest(unittest.TestCase):

    headers: Headers

    def setUp(self) -> None:
        MyKissHeadersFromStringTest.headers = parse_it(RAW_HEADERS)

    def test_control_basis_exist(self):

        self.assertEqual(
            'DPR',
            MyKissHeadersFromStringTest.headers.accept_ch
        )

        self.assertEqual(
            3,
            len(MyKissHeadersFromStringTest.headers.set_cookie)
        )

        self.assertIn(
            'Secure',
            MyKissHeadersFromStringTest.headers.set_cookie[0]
        )

        self.assertEqual(
            'This is not a P3P policy! See g.co/p3phelp for more info.',
            MyKissHeadersFromStringTest.headers.p3p.cp
        )


if __name__ == '__main__':
    unittest.main()
