from __future__ import annotations

import unittest

from kiss_headers import Allow, ContentType, get_polymorphic, parse_it


class MyPolymorphicTestCase(unittest.TestCase):
    def test_get_polymorphic(self):
        headers = parse_it(
            """accept-ch: DPR
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
status: 200"""
        )

        content_type = get_polymorphic(headers, ContentType)

        self.assertEqual("UTF-8", content_type.get_charset())

        self.assertEqual("text/html", content_type.get_mime())

        content_type = get_polymorphic(headers.content_type, ContentType)

        self.assertEqual("UTF-8", content_type.get_charset())

        self.assertEqual("text/html", content_type.get_mime())

        with self.assertRaises(TypeError):
            content_type = get_polymorphic(headers.content_type, Allow)


if __name__ == "__main__":
    unittest.main()
