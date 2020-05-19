import unittest
from kiss_headers import Attributes


class AttributesTestCase(unittest.TestCase):
    def test_eq(self):
        attr_a = Attributes(["a", "p=8a", "a", "XX"])
        attr_b = Attributes(["p=8a", "a", "a", "XX"])
        attr_c = Attributes(["p=8a", "a", "A", "Xx"])
        attr_d = Attributes(["p=8a", "a", "A", "Xx", "XX=a"])
        attr_e = Attributes(["p=8A", "a", "A", "Xx"])

        self.assertEqual(
            attr_a,
            attr_b
        )

        self.assertEqual(
            attr_a,
            attr_c
        )

        self.assertNotEqual(
            attr_a,
            attr_d
        )

        self.assertNotEqual(
            attr_a,
            attr_e
        )


if __name__ == '__main__':
    unittest.main()
