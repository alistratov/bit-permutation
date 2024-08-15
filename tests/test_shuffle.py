import unittest

from bit_permutation import BitShuffle, BitPermutation, BitInversion
from .sample_iters import test_list, test_tuple, TestIterator, test_gen


class TestBitShuffle(unittest.TestCase):
    def test_identity(self):
        bs1 = BitShuffle()
        self.assertEqual(len(bs1), 0)
        self.assertEqual(bs1.is_identity(), True)

        bs2 = BitShuffle(BitPermutation((0, 1)), BitInversion(0))
        self.assertEqual(len(bs2), 0)
        self.assertEqual(bs2.is_identity(), True)

        self.assertEqual(bs1, bs2)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            _ = BitShuffle(permutation=BitPermutation((1, 0, 1)))

        with self.assertRaises(ValueError):
            _ = BitShuffle(inversion=BitInversion(-1))

        with self.assertRaises(ValueError):
            _ = BitShuffle(permutation=BitPermutation((1, 0, 1)), inversion=BitInversion(-1))

        with self.assertRaises(ValueError):
            _ = BitShuffle.from_tuple(())

    def test_repr(self):
        cases = [
            (BitShuffle(), 'BitShuffle()'),
            (BitShuffle(BitPermutation((0, 1)), BitInversion(0)), 'BitShuffle()'),
            (
                BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209)),
                'BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209))',
            ),
            (
                BitShuffle(BitPermutation((3, 8, 2, 0, 7, 9, 6, 4, 1, 5)), BitInversion(123450)),
                'BitShuffle(BitPermutation((3, 8, 2, 0, 7, 9, 6, 4, 1, 5)), BitInversion(123450))',
            ),
            (
                BitShuffle(permutation=BitPermutation((3, 1, 2, 0))),
                'BitShuffle(BitPermutation((3, 1, 2, 0)))',
            ),
            (
                BitShuffle(inversion=BitInversion(209)),
                'BitShuffle(None, BitInversion(209))',
            ),
        ]

        for case in cases:
            bs = case[0]
            self.assertEqual(repr(bs), case[1])
            b2 = eval(case[1])  # noqa: S307
            self.assertTrue(bs == b2)

    def test_members(self):
        bs = BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209))
        self.assertEqual(bs.permutation, BitPermutation((3, 1, 2, 0)))
        self.assertEqual(bs.inversion, BitInversion(209))

    def test_eq(self):
        self.assertTrue(BitShuffle() == BitShuffle())
        self.assertTrue(BitShuffle() == BitShuffle(BitPermutation((0, 1)), BitInversion(0)))
        self.assertTrue(
            BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209)) ==
            BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209))
        )

        self.assertFalse(
            BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209)) ==
            BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(210))
        )
        self.assertFalse(BitShuffle() == 'foo')

    def test_hash(self):
        d = {
            BitShuffle(): 'empty',
            BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209)): 'alpha',
            BitShuffle(BitPermutation((2, 0, 1)), BitInversion(8)): 'beta',
            BitShuffle(BitPermutation((0, 1)), BitInversion(0)): 'ident',
        }
        self.assertEqual(d[BitShuffle()], 'ident')
        self.assertEqual(len(d), 3)

    def test_length(self):
        self.assertEqual(len(BitShuffle()), 0)
        self.assertEqual(len(BitShuffle(BitPermutation((0, 1)), BitInversion(0))), 0)
        self.assertEqual(len(BitShuffle(BitPermutation((0, 1)), BitInversion(2))), 2)
        self.assertEqual(len(BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(209))), 8)
        self.assertEqual(len(BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(0))), 4)
        self.assertEqual(len(BitShuffle(BitPermutation(), BitInversion(209))), 8)
        self.assertEqual(len(BitShuffle(BitPermutation(), BitInversion(15))), 4)
        self.assertEqual(len(BitShuffle(BitPermutation((3, 1, 2, 0)), BitInversion(15))), 4)

    def test_shuffle(self):
        bs = BitShuffle()
        self.assertEqual(bs.shuffle(0), 0)
        self.assertEqual(bs.unshuffle(2009), 2009)

        bs = BitShuffle.unpack(192658906865088603127525391421771642279671466717216)
        self.assertEqual(bs.shuffle(0xDEADBEEF), 0xCAFEBABE)
        self.assertEqual(bs.unshuffle(0xCAFEBABE), 0xDEADBEEF)

    def test_random_constructor(self):
        with self.assertRaises(ValueError):
            _ = BitShuffle.generate_random(-1)

        b0 = BitShuffle.generate_random(0)
        self.assertEqual(b0, BitShuffle())

        b1 = BitShuffle.generate_random(1)
        self.assertEqual(b1, BitShuffle.from_tuple((1,)))

        for n in range(2, 256, 7):
            bs = BitShuffle.generate_random(n)
            self.assertEqual(len(bs), n)
            self.assertEqual(bs.unshuffle(bs.shuffle(2009)), 2009)

    def test_representation(self):
        b0 = BitShuffle()
        self.assertEqual(b0.as_tuple(), (0,))
        self.assertEqual(BitShuffle.from_tuple((0,)), BitShuffle())
        # self.assertEqual(b0.as_numbers(), (0, 0, 0))
        self.assertEqual(b0.pack(), 1024)
        # self.assertEqual(BitShuffle.from_numbers(0, 0, 0), BitShuffle())

        r0 = BitShuffle.unpack(1024)
        self.assertEqual(r0, b0)

        t = (11, 0, 1, 4, 19, 20, 5, 23, 21, 31, 29, 7, 8, 26, 28, 30,
             15, 2, 17, 18, 16, 10, 12, 25, 3, 13, 14, 6, 24, 9, 22, 27)
        bs = BitShuffle(
            BitPermutation(t),
            BitInversion(0x2528574D),
        )
        self.assertEqual(bs.as_tuple(), (*t, 623400781))
        self.assertEqual(BitShuffle.from_tuple((*t, 623400781)), bs)
        # self.assertEqual(bs.as_numbers(), (32, 90452004396397327946375084361359772, 623400781))
        self.assertEqual(bs.pack(), 192658906865088603127525391421771642279671466717216)
        # self.assertEqual(BitShuffle.from_numbers(32, 90452004396397327946375084361359772, 623400781), bs)

        rs = BitShuffle.unpack(192658906865088603127525391421771642279671466717216)
        self.assertEqual(rs, bs)

    def test_unpack(self):
        with self.assertRaises(ValueError):
            _ = BitShuffle.unpack(20)

        big = BitShuffle.generate_random(1023)
        packed = big.pack()
        self.assertEqual(BitShuffle.unpack(packed), big)

    def test_iterable(self):
        bs = BitShuffle(BitPermutation((1, 0)), BitInversion(1))
        s = [1, 3, 0, 2]
        u = [2, 0, 3, 1]

        self.assertEqual(list(bs.shuffle_iter(test_list)), s)
        self.assertEqual(list(bs.shuffle_iter(test_tuple)), s)
        self.assertEqual(list(bs.shuffle_iter(TestIterator())), s)
        self.assertEqual(list(bs.shuffle_iter(test_gen())), s)

        self.assertEqual(list(bs.unshuffle_iter(test_list)), u)
        self.assertEqual(list(bs.unshuffle_iter(test_list)), u)
        self.assertEqual(list(bs.unshuffle_iter(test_list)), u)
        self.assertEqual(list(bs.unshuffle_iter(test_list)), u)
