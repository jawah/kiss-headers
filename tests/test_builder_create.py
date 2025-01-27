from __future__ import annotations

import unittest

from kiss_headers import (
    Accept,
    AcceptEncoding,
    AcceptLanguage,
    AltSvc,
    CacheControl,
    Connection,
    ContentEncoding,
    ContentLength,
    ContentType,
    Date,
    Expires,
    Header,
    Host,
    IfModifiedSince,
    IfNoneMatch,
    Referer,
    Server,
    SetCookie,
    StrictTransportSecurity,
    UpgradeInsecureRequests,
    UserAgent,
    XFrameOptions,
    XXssProtection,
    parse_it,
)

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


class MyBuilderCreationTestCase(unittest.TestCase):
    def test_replicate_raw_from_objects_request(self):
        headers = (
            Host("developer.mozilla.org")
            + UserAgent(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"
            )
            + Accept("text/html")
            + Accept("application/xhtml+xml")
            + Accept("application/xml", qualifier=0.9)
            + Accept(qualifier=0.8)
            + AcceptLanguage("en-US")
            + AcceptLanguage("en", qualifier=0.5)
            + AcceptEncoding("gzip")
            + AcceptEncoding("deflate")
            + AcceptEncoding("br")
            + Referer("https://developer.mozilla.org/testpage.html")
            + Connection(True)
            + UpgradeInsecureRequests()
            + IfModifiedSince("Mon, 18 Jul 2016 02:36:04 GMT")
            + IfNoneMatch("c561c68d0ba92bbeb8b0fff2a9199f722e3a621a")
            + CacheControl(max_age=0)
        )

        self.assertEqual(parse_it(RAW_HEADERS_MOZILLA), headers)

    def test_replicate_raw_from_objects(self):
        headers = (
            Header("Accept-Ch", "DPR")
            + Header("Accept-Ch-Lifetime", "2592000")
            + AltSvc("quic", ":443", max_age=2592000, versions=["46", "43"])
            + AltSvc("h3-Q050", ":443", max_age=2592000)
            + AltSvc("h3-Q049", ":443", max_age=2592000)
            + AltSvc("h3-Q048", ":443", max_age=2592000)
            + AltSvc("h3-Q046", ":443", max_age=2592000)
            + AltSvc("h3-Q043", ":443", max_age=2592000)
            + CacheControl("private")
            + CacheControl(max_age=0)
            + ContentEncoding("br")
            + ContentLength(64032)
            + ContentType("text/html", charset="utf-8")
            + Date("Mon, 16 Mar 2020 21:27:31 GMT")
            + Expires("-1")
            + Header(
                "P3P", 'CP="This is not a P3P policy! See g.co/p3phelp for more info."'
            )
            + Server("gws")
            + SetCookie(
                "1P_JAR",
                "2020-03-16-21",
                expires="Wed, 15-Apr-2020 21:27:31 GMT",
                path="/",
                domain=".google.fr",
                samesite="none",
                is_secure=True,
                is_httponly=False,
            )
            + SetCookie(
                "NID",
                "200=IGpBMMA3G7tki0niFFATFQ2BnsNceVP6XBtwOutoyw97AJ4_YFT5l1oLfLeX22xeI_STiP4omAB4rmMP3Sxgyo287ldQGwdZSdPOOZ_Md3roDOMAOtXEQ_hFbUvo0VPjS2gL1y00_6kQwpVxCghI2Ozrx-A4Xks3ZIXRj11RsWs",
                expires="Tue, 15-Sep-2020 21:27:31 GMT",
                path="/",
                domain=".google.fr",
                samesite="none",
                is_secure=True,
            )
            + SetCookie(
                "CONSENT",
                "WP.284b10",
                expires="Fri, 01-Jan-2038 00:00:00 GMT",
                path="/",
                domain=".google.fr",
                is_httponly=False,
            )
            + Header("Status", "200")
            + StrictTransportSecurity(max_age=31536000)
            + XFrameOptions("SAMEORIGIN")
            + XXssProtection(False)
        )

        self.assertEqual(parse_it(RAW_HEADERS), headers)


if __name__ == "__main__":
    unittest.main()
