from __future__ import annotations

import unittest

from kiss_headers import (
    AltSvc,
    CacheControl,
    ContentEncoding,
    ContentLength,
    ContentType,
    Date,
    Expires,
    Header,
    Server,
    SetCookie,
    StrictTransportSecurity,
    XFrameOptions,
    XXssProtection,
    explain,
)


class MyExplainTestCase(unittest.TestCase):
    def test_explain_from_objects(self):
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

        explanations = explain(headers)

        self.assertNotEqual("Unknown explanation.", explanations["Set-Cookie"])

        self.assertNotEqual("Missing docstring.", explanations["Set-Cookie"])

        self.assertEqual("Unknown explanation.", explanations["Accept-Ch"])

        self.assertEqual("Unknown explanation.", explanations["Accept_Ch"])

        self.assertEqual("Unknown explanation.", explanations["aCCept_Ch"])


if __name__ == "__main__":
    unittest.main()
