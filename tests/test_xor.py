import unittest

from bit_permutation import BitInversion


class TestBitInversion(unittest.TestCase):
    def test_empty_and_zero(self):
        for bi in (BitInversion(), BitInversion(0)):
            self.assertEqual(int(bi), 0)
            self.assertEqual(len(bi), 0)
            self.assertEqual(bi.is_identity(), True)
            self.assertEqual(bi.get_number_of_fixed_points(), -1)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            _ = BitInversion(-1)

        with self.assertRaises(ValueError):
            _ = BitInversion(2 ** 1023)

    def test_int(self):
        bi = BitInversion()
        self.assertEqual(int(bi), 0)

        bi = BitInversion(123)
        self.assertEqual(int(bi), 123)

        bi = BitInversion(0xDEADBEEF)
        self.assertEqual(int(bi), 0xDEADBEEF)
        self.assertEqual(hex(bi), '0xdeadbeef')  # test __index__

    def test_repr(self):
        bi = BitInversion()
        self.assertEqual(repr(bi), 'BitInversion()')

        bi = BitInversion(0)
        self.assertEqual(repr(bi), 'BitInversion()')

        bi = BitInversion(123)
        self.assertEqual(repr(bi), 'BitInversion(123)')

        bi = BitInversion(0xDEADBEEF)
        self.assertEqual(repr(bi), 'BitInversion(3735928559)')
        b2 = eval(repr(bi))  # noqa: S307
        self.assertTrue(bi == b2)

    def test_eq(self):
        self.assertTrue(BitInversion() == BitInversion())
        self.assertTrue(BitInversion() == BitInversion(0))
        self.assertTrue(BitInversion(1) == 1)

        self.assertFalse(BitInversion(1) == BitInversion(2))
        self.assertFalse(BitInversion(1) == 'foo')

    def test_hash(self):
        d = {
            BitInversion(): 'empty',
            BitInversion(0): 'zero',
            BitInversion(1): 'one',
            BitInversion(2): 'two',
        }
        self.assertEqual(d[BitInversion()], 'zero')
        self.assertEqual(len(d), 3)

    def test_length(self):
        self.assertEqual(len(BitInversion()), 0)
        self.assertEqual(len(BitInversion(0)), 0)
        self.assertEqual(len(BitInversion(1)), 1)
        self.assertEqual(len(BitInversion(2)), 2)
        self.assertEqual(len(BitInversion(3)), 2)
        self.assertEqual(len(BitInversion(4)), 3)
        self.assertEqual(len(BitInversion(0b10101010101010101010101010101010)), 32)
        self.assertEqual(len(BitInversion(0b00000000000000000000000010101010)), 8)

    def test_fixed_points(self):
        self.assertEqual(BitInversion().get_number_of_fixed_points(), -1)
        self.assertEqual(BitInversion(0).get_number_of_fixed_points(), -1)
        self.assertEqual(BitInversion(1).get_number_of_fixed_points(), 0)
        self.assertEqual(BitInversion(2).get_number_of_fixed_points(), 1)
        self.assertEqual(BitInversion(3).get_number_of_fixed_points(), 0)
        self.assertEqual(BitInversion(4).get_number_of_fixed_points(), 2)
        self.assertEqual(BitInversion(0b10101010101010101010101010101010).get_number_of_fixed_points(), 16)
        self.assertEqual(BitInversion(0b00000000000000000000000010101010).get_number_of_fixed_points(), 4)

    def test_application(self):
        bi = BitInversion()
        self.assertEqual(bi.apply(0), 0)
        self.assertEqual(bi.apply(2009), 2009)

        bi = BitInversion(1)
        self.assertEqual(bi.apply(0), 1)
        self.assertEqual(bi.apply(1), 0)
        self.assertEqual(bi.apply(2009), 2008)
        self.assertEqual(bi.apply(bi.apply(2009)), 2009)

        bi = BitInversion(0xDEADBEEF)
        self.assertEqual(bi.apply(0), 0xDEADBEEF)
        self.assertEqual(bi.apply(0xDEADBEEF), 0)
        self.assertEqual(bi.apply(0xCAFEBABE), 0x14530451)
        self.assertEqual(bi.apply(bi.apply(0xCAFEBABE)), 0xCAFEBABE)

    def test_random_constructor(self):
        with self.assertRaises(ValueError):
            _ = BitInversion.generate_random(-1)

        for n in range(256):
            bi = BitInversion.generate_random(n)
            self.assertEqual(len(bi), n)

        bi = BitInversion.generate_random(32, 0.0)
        self.assertEqual(bi, 0b11111111111111111111111111111111)
        bi = BitInversion.generate_random(32, 1.0)
        self.assertEqual(bi, 0b10000000000000000000000000000000)
