import unittest
from kiss_headers import Header, parse_it


class KissHeadersOperationTest(unittest.TestCase):
    def test_isub(self):
        headers = parse_it("""X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisly\nReceived: outpost\nReceived: outpost""")

        self.assertEqual(
            5,
            len(headers)
        )

        headers -= 'X-My-Testing'

        self.assertEqual(
            4,
            len(headers)
        )

        self.assertNotIn(
            'X-My-Testing',
            headers
        )

        headers -= 'Received'

        self.assertEqual(
            2,
            len(headers)
        )

        self.assertNotIn(
            'Received',
            headers
        )

        headers -= Header('X-My-Second-Test', 'Precisly')

        self.assertEqual(
            1,
            len(headers)
        )

        self.assertIn(
            'X-My-Second-Test',
            headers
        )

    def test_sub(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisly\nReceived: outpost\nReceived: outpost""")

        self.assertEqual(
            5,
            len(headers)
        )

        headers_two = headers - 'X-My-Testing'

        self.assertEqual(
            5,
            len(headers)
        )

        self.assertEqual(
            4,
            len(headers_two)
        )

    def test_add(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisly\nReceived: outpost\nReceived: outpost""")

        self.assertEqual(
            5,
            len(headers)
        )

        headers_ = headers + Header('content-type', 'application/json')

        self.assertEqual(
            6,
            len(headers_)
        )

        self.assertIn(
            'content-type',
            headers_
        )

        self.assertNotIn(
            'content-type',
            headers
        )



if __name__ == '__main__':
    unittest.main()
