import unittest

from kiss_headers import Header


class MyKissHeaderTest(unittest.TestCase):
    def test_invalid_eq(self):

        header = Header(
            "Message-ID", "<455DADE4FB733C4C8F62EB4CEB36D8DE05037EA94F@johndoe>"
        )

        with self.assertRaises(NotImplementedError):
            k = header == 1

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
