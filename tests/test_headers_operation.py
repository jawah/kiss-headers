from __future__ import annotations

import unittest

from kiss_headers import Header, Headers, parse_it


class KissHeadersOperationTest(unittest.TestCase):
    def test_eq_with_other_object(self):
        class HasTestHeader:
            def __eq__(self, other):
                return other.get("X-Test") == "1"

        expected = HasTestHeader()
        for value, matches in [("1", True), ("2", False)]:
            with self.subTest(value=value):
                headers = Headers(Header("X-Test", value), Header("Extra", "2"))
                self.assertIs(headers == expected, matches)
                self.assertIs(expected == headers, matches)
                self.assertIs(headers != expected, not matches)
                self.assertIs(expected != headers, not matches)

    def test_eq_with_unknown_type(self):
        headers = Headers(Header("X-Test", "1"))
        other = object()

        self.assertIs(headers == other, False)
        self.assertIs(other == headers, False)
        self.assertIs(headers != other, True)
        self.assertIs(other != headers, True)

    def test_isub(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        headers -= "X-My-Testing"

        self.assertEqual(4, len(headers))

        self.assertNotIn("X-My-Testing", headers)

        headers -= "Received"

        self.assertEqual(2, len(headers))

        self.assertNotIn("Received", headers)

        headers -= Header("X-My-Second-Test", "Precisely")

        self.assertEqual(1, len(headers))

        self.assertIn("X-My-Second-Test", headers)

    def test_sub(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        headers_two = headers - "X-My-Testing"

        self.assertEqual(5, len(headers))

        self.assertEqual(4, len(headers_two))

    def test_add(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        headers_ = headers + Header("content-type", "application/json")

        self.assertEqual(6, len(headers_))

        self.assertIn("content-type", headers_)

        self.assertNotIn("content-type", headers)

    def test_remove_by_del(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        del headers["X-My-Second-Test"]

        self.assertEqual(3, len(headers))

        self.assertNotIn("X-My-Second-Test", headers)

    def test_remove_by_del_attr(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        del headers.x_my_second_test

        self.assertEqual(3, len(headers))

        self.assertNotIn("X-My-Second-Test", headers)

    def test_by_setitem(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        headers["content-type"] = "application/json; charset=utf-8"

        self.assertEqual(6, len(headers))

        self.assertEqual("utf-8", headers.content_type.charset)

    def test_by_setattr(self):
        headers = parse_it(
            """X-My-Testing: 1\nX-My-Second-Test: 1\nX-My-Second-Test: Precisely\nReceived: outpost\nReceived: outpost"""
        )

        self.assertEqual(5, len(headers))

        headers.content_type = "application/json; charset=utf-8"

        self.assertEqual(6, len(headers))

        self.assertEqual("utf-8", headers.content_type.charset)


if __name__ == "__main__":
    unittest.main()
