from __future__ import annotations

import unittest

from kiss_headers import Header


class MyKissHeaderTest(unittest.TestCase):
    def test_json_header(self):
        header = Header(
            "Report-To",
            '{"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v3?s=zhnRFonTa%2FAOS8x%2BTZXZBDr5B0k7E7rziICyCRD5SVCtz106%2FlbzKGHKLwXpAC1XUZ5Nb5SQBuoI336MkB%2BzhxjictL4oc6wjku7aFfGBCi5rMi5Z5LPYVMDPUnhFDymbNiE7wc9"}],"group":"cf-nel","max_age":604800}',
        )

        assert "endpoints" in header
        assert "group" in header
        assert header.group == "cf-nel"

    def test_invalid_eq(self):
        header = Header(
            "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
        )

        with self.assertRaises(NotImplementedError):
            k = header == 1  # noqa

    def test_simple_eq(self):
        self.assertEqual(
            Header(
                "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
            ).content,
            "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>",
        )

        self.assertEqual(
            Header(
                "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
            ),
            "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>",
        )

        self.assertNotEqual(
            Header(
                "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
            ),
            Header(
                "Message-ID-Dummy",
                "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>",
            ),
        )

        self.assertEqual(
            Header(
                "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
            ),
            Header(
                "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
            ),
        )

    def test_attribute_access_exist(self):
        self.assertIn(
            "charset",
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            ),
        )

        self.assertIn(
            "boundary",
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            ),
        )

    def test_attribute_not_in(self):
        self.assertNotIn(
            "format",
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            ),
        )

        self.assertNotIn(
            "secret",
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            ),
        )

    def test_access_attribute(self):
        self.assertEqual(
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            ).charset,
            "utf-8",
        )

        self.assertEqual(
            Header(
                "Content-Type",
                'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
            )["charset"],
            "utf-8",
        )

    def test_single_header_iterator(self):
        header = Header(
            "Content-Type",
            'multipart/alternative; boundary="_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_"; charset=utf-8',
        )

        self.assertEqual(
            {
                "multipart/alternative": None,
                "boundary": "_000_455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94Fswexch1sesaml_",
                "charset": "utf-8",
            },
            dict(header),
        )


if __name__ == "__main__":
    unittest.main()
