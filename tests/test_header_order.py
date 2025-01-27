from __future__ import annotations

import unittest

from kiss_headers import Header


class HeaderOrderingTest(unittest.TestCase):
    def test_keep_initial_order(self):
        header = Header("Content-Type", "a; b=k; h; h; z=0")

        self.assertEqual(["a", "b", "h", "h", "z"], header.attrs)

    def test_insertion_in_ordered_header(self):
        header = Header("Content-Type", "a; b=k; h; h; z=0")

        header.insert(2, ppp="nt")

        self.assertEqual(["a", "b", "ppp", "h", "h", "z"], header.attrs)

    def test_pop_in_ordered_header(self):
        header = Header("Content-Type", "a; b=k; h; h; z=0")

        key, value = header.pop(2)

        self.assertEqual(key, "h")

        self.assertIsNone(value)

        self.assertEqual(["a", "b", "h", "z"], header.attrs)

    def test_pop_negative_index(self):
        header = Header("Content-Type", "a; b=k; h; h; z=0")

        key, value = header.pop(-1)

        self.assertEqual(key, "z")

        self.assertEqual(value, "0")

        self.assertEqual(["a", "b", "h", "h"], header.attrs)

    def test_attrs_original_case(self):
        header = Header("Content-Type", "aA; bc=k; hA; h; zZzZ=0")

        with self.subTest(
            "Ensure that attrs and valued_attrs properties keep the original case."
        ):
            self.assertEqual(["aA", "bc", "hA", "h", "zZzZ"], header.attrs)

            self.assertEqual(["bc", "zZzZ"], header.valued_attrs)


if __name__ == "__main__":
    unittest.main()
