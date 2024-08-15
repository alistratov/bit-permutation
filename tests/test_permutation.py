import unittest

from bit_permutation import BitPermutation
from .sample_iters import test_list, test_tuple, TestIterator, test_gen


class TestBitPermutation(unittest.TestCase):
    SAMPLES = (
        1,
        209,
        703,
        1978,
        19780920,
        4945012371837,
    )

    def test_empty(self):
        bp = BitPermutation()
        self.assertEqual(bp.as_tuple(), ())
        self.assertEqual(len(bp), 0)
        self.assertEqual(bp.is_identity(), True)
        self.assertEqual(bp.is_derangement(), False)

    def test_reducing(self):
        for p in (
            (2, 1, 0),
            (2, 1, 0, 3, 4),
            (2, 1, 0, 3, 4, 5, 6, 7, 8, 9),
        ):
            bp = BitPermutation(p)
            self.assertEqual(len(bp), 3)
            self.assertTrue(bp == BitPermutation((2, 1, 0)))
            self.assertEqual(bp.as_tuple(), (2, 1, 0))

    def test_identical(self):
        for p in (
            (),
            (0,),
            (0, 1),
            (0, 1, 2),
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        ):
            bp = BitPermutation(p)
            self.assertTrue(bp == BitPermutation())
            self.assertEqual(bp.as_tuple(), ())
            self.assertEqual(bp.is_identity(), True)
            self.assertEqual(bp.is_involution(), True)  # each identical permutation is an involution
            self.assertEqual(bp.is_derangement(), False)
            self.assertEqual(bp.get_number_of_fixed_points(), -1)

    def test_invalid(self):
        for p in (
            (1,),
            (-1,),
            (2, 1),
            (1, 12),
            (0, 0),
            (1, 0, 1),
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -2),
            (1, 2, 0, 1),
        ):
            with self.assertRaisesRegex(ValueError, 'Invalid permutation'):
                _ = BitPermutation(p)

        with self.assertRaises(TypeError):
            _ = BitPermutation(1)  # not iterable

        with self.assertRaises(TypeError):
            _ = BitPermutation(1.0)  # not iterable

        with self.assertRaises(TypeError):
            _ = BitPermutation('123')  # type mismatch in comparison

        # Lists are valid
        bp = BitPermutation([3, 1, 2, 0])
        self.assertEqual(bp.as_tuple(), (3, 1, 2, 0))

        # Sets are theoretically valid, but usually are converted to sorted list and then to identity
        # bp = BitPermutation({3, 1, 2, 0})
        # self.assertEqual(bp.as_tuple(), ())

        with self.assertRaises(ValueError):
            # Too long
            _ = BitPermutation(list(reversed(range(1024))))

    def test_repr(self):
        bp = BitPermutation()
        self.assertEqual(repr(bp), 'BitPermutation()')

        bp = BitPermutation()
        self.assertEqual(repr(bp), 'BitPermutation()')

        bp = BitPermutation((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(repr(bp), 'BitPermutation()')

        bp = BitPermutation((3, 8, 2, 0, 7, 9, 6, 4, 1, 5))
        self.assertEqual(repr(bp), 'BitPermutation((3, 8, 2, 0, 7, 9, 6, 4, 1, 5))')
        b2 = eval(repr(bp))  # noqa: S307
        self.assertTrue(bp == b2)

    def test_eq(self):
        self.assertTrue(BitPermutation() == BitPermutation())
        self.assertTrue(BitPermutation((2, 0, 1)) == BitPermutation((2, 0, 1)))

        self.assertFalse(BitPermutation((2, 0, 1)) == BitPermutation((1, 2, 0)))
        self.assertFalse(BitPermutation((2, 0, 1)) == 0)
        self.assertFalse(BitPermutation((2, 0, 1)) == 'foo')

    def test_hash(self):
        d = {
            BitPermutation(): 'identity',
            BitPermutation((2, 0, 1)): '3, 1, 2',
            BitPermutation((3, 1, 2, 0)): '4, 2, 3, 1',
            BitPermutation((0, 1)): 'identity',
        }
        self.assertEqual(d[BitPermutation((0, 1, 2))], 'identity')
        self.assertEqual(len(d), 3)

    def test_fixed_points(self):
        bp = BitPermutation((0, 1, 2))
        self.assertEqual(bp.get_number_of_fixed_points(), -1)
        self.assertEqual(bp.is_derangement(), False)

        bp = BitPermutation((1, 0))
        self.assertEqual(bp.get_number_of_fixed_points(), 0)
        self.assertEqual(bp.is_derangement(), True)

        bp = BitPermutation((3, 2, 1, 0))
        self.assertEqual(bp.get_number_of_fixed_points(), 0)
        self.assertEqual(bp.is_derangement(), True)

        bp = BitPermutation((0, 1, 3, 2))
        self.assertEqual(bp.get_number_of_fixed_points(), 2)
        self.assertEqual(bp.is_derangement(), False)

        bp = BitPermutation((1, 0, 2, 4, 3))
        self.assertEqual(bp.get_number_of_fixed_points(), 1)
        self.assertEqual(bp.is_derangement(), False)

        bp = BitPermutation((3, 8, 2, 0, 7, 9, 6, 4, 1, 5))
        self.assertEqual(bp.get_number_of_fixed_points(), 2)
        self.assertEqual(bp.is_derangement(), False)

    def test_involution(self):
        # Involutions
        for p in (
            (1, 0),
            (0, 2, 1),
            (2, 1, 0),
            (3, 1, 2, 0),
            (2, 5, 0, 4, 3, 1),
            (2, 1, 0, 3, 4, 5, 6, 7, 8, 9),
            (3, 8, 2, 0, 7, 9, 6, 4, 1, 5),
        ):
            bp = BitPermutation(p)
            self.assertEqual(bp.is_involution(), True)
            for sample in self.SAMPLES:
                self.assertEqual(bp.invert(bp.permute(sample)), sample)
                self.assertEqual(bp.permute(bp.invert(sample)), sample)
                self.assertEqual(bp.permute(bp.permute(sample)), sample)
                self.assertEqual(bp.invert(bp.invert(sample)), sample)

        # Not involutions
        for p in (
            (2, 0, 1),
            (2, 3, 1, 0),
            (4, 6, 1, 0, 5, 3, 2),
            (6, 4, 1, 3, 0, 8, 2, 7, 9, 5),
            (3, 16, 1, 6, 0, 10, 19, 18, 11, 4, 7, 12, 13, 2, 15, 5, 17, 8, 14, 9),
        ):
            bp = BitPermutation(p)
            self.assertEqual(bp.is_involution(), False)
            for sample in self.SAMPLES:
                self.assertEqual(bp.invert(bp.permute(sample)), sample)
                self.assertEqual(bp.permute(bp.invert(sample)), sample)

    def test_permute(self):
        bp = BitPermutation((2, 1, 0))  # bits 0 and 2 are swapped
        self.assertEqual(bp.permute(0b000), 0b000)
        self.assertEqual(bp.permute(0b001), 0b100)
        self.assertEqual(bp.permute(0b010), 0b010)
        self.assertEqual(bp.permute(0b011), 0b110)
        self.assertEqual(bp.permute(0b100), 0b001)
        self.assertEqual(bp.permute(0b101), 0b101)
        self.assertEqual(bp.permute(0b110), 0b011)
        self.assertEqual(bp.permute(0b111), 0b111)
        # Higher bits are unchanged
        self.assertEqual(bp.permute(0b10101010101010101010101010101010), 0b10101010101010101010101010101010)
        self.assertEqual(bp.permute(0b01010101010101010101010101010001), 0b01010101010101010101010101010100)
        self.assertEqual(bp.permute(0b11111111111111111111111111111100), 0b11111111111111111111111111111001)

        bp = BitPermutation((1, 0, 2, 4, 3))  # it's involution btw
        self.assertEqual(bp.permute(0b00001010), 0b00010001)  # 10 -> 17
        self.assertEqual(bp.permute(0b00001011), 0b00010011)  # 11 -> 19
        self.assertEqual(bp.permute(0b00010010), 0b00001001)  # 18 -> 9
        self.assertEqual(bp.permute(0b00000110), 0b00000101)  # 6 -> 5
        self.assertEqual(bp.permute(0b11000110), 0b11000101)  # 192 + 6 -> 192 + 5

    def test_inverse(self):
        bp = BitPermutation((1, 0, 2, 4, 3))
        self.assertEqual(bp.is_involution(), True)

        for x in range(32 + 8):
            y = bp.permute(x)
            z = bp.invert(y)
            y2 = bp.permute(y)
            self.assertEqual(z, x)
            self.assertEqual(z, y2)

        bp = BitPermutation((1, 0, 4, 2, 3))
        self.assertEqual(bp.is_involution(), False)

        for x in range(32 + 8):
            y = bp.permute(x)
            z = bp.invert(y)
            self.assertEqual(z, x)

    def test_permute_and_back(self):
        for n in (4, 8, 16, 32, 64, 128):
            bp = BitPermutation.generate_derangement(n)
            for x in (-1978, -209, -2, -1, 0, 1, 209, 0xDEADBEEF, 2 ** 63 - 1, 2 ** 65):
                y = bp.permute(x)
                z = bp.invert(y)
                self.assertEqual(x, z)

    def test_random_constructors(self):
        for n in (-2, 0, 1):
            with self.assertRaises(ValueError):
                _ = BitPermutation.generate_random(n)

            with self.assertRaises(ValueError):
                _ = BitPermutation.generate_derangement(n)

            with self.assertRaises(ValueError):
                _ = BitPermutation.generate_involution(n)

        for n in (2, 3, 5, 10, 16, 32):
            for _ in range(10):
                bp = BitPermutation.generate_random(n)
                self.assertEqual(len(bp), n)

                bp = BitPermutation.generate_derangement(n)
                self.assertEqual(len(bp), n)
                self.assertEqual(bp.is_derangement(), True)

                bp = BitPermutation.generate_involution(n)
                self.assertEqual(len(bp), n)
                self.assertEqual(bp.is_involution(), True)

        # Some short derangements
        bp = BitPermutation.generate_derangement(2)
        self.assertEqual(bp.as_tuple(), (1, 0))  # the only possible derangement of 2 elements

        bp = BitPermutation.generate_derangement(3)
        self.assertTrue((bp.as_tuple() == (1, 2, 0)) or (bp.as_tuple() == (2, 0, 1)))  # not so many options

        # Some short involutions
        bp = BitPermutation.generate_involution(2)
        self.assertEqual(bp.as_tuple(), (1, 0))  # the only possible involution of 2 elements

        bp = BitPermutation.generate_involution(3)
        # There are two possible involutions of length 3: (0, 2, 1) and (2, 1, 0),
        # because (0, 1, 2) is the identity permutation,
        # and (1, 0, 2) is truncated to (1, 0).
        self.assertTrue((bp.as_tuple() == (0, 2, 1)) or (bp.as_tuple() == (2, 1, 0)))

        # Check different probabilities
        bp = BitPermutation.generate_involution(8, 0.0)
        bp = BitPermutation.generate_involution(8, 0.3)
        bp = BitPermutation.generate_involution(8, 0.999999)  # will be limited to 0.99

        with self.assertRaises(ValueError):
            _ = BitPermutation.generate_involution(8, 1.0)

        with self.assertRaises(ValueError):
            _ = BitPermutation.generate_involution(8, -0.5)

    def test_lehmer_and_pack(self):
        cases = [
            {
                'p': (),
                'lehmer': (),
                'packed': 0,
                'inversions': 0,
            },
            {
                # The Lehmer code for the permutation (3, 1, 4, 2) is (2, 0, 1, 0)
                'p': (2, 0, 3, 1),
                'lehmer': (2, 0, 1, 0),
                'packed': 0b11010000000100,
                'inversions': 3,
            },
            {
                # ResourceFunction["LehmerCodeFromPermutation"][{1, 2, 9, 5, 4, 12, 7, 6, 3, 11, 10, 8}]
                # Out=[0, 0, 6, 2, 1, 6, 2, 1, 0, 2, 1, 0]
                'p': (0, 1, 8, 4, 3, 11, 6, 5, 2, 10, 9, 7),
                'lehmer': (0, 0, 6, 2, 1, 6, 2, 1, 0, 2, 1, 0),
                'packed': 2321970188,
                'inversions': 21,
            },
            {
                'p': (40, 4, 9, 46, 32, 49, 38, 43, 15, 25, 6, 51, 42, 50, 34, 60, 8, 37, 22, 20, 48, 44, 3,
                      56, 27, 16, 41, 36, 33, 45, 14, 39, 12, 61, 58, 52, 47, 24, 18, 62, 35, 0, 30, 57, 19,
                      2, 59, 5, 11, 63, 26, 23, 54, 55, 29, 7, 21, 1, 53, 28, 31, 17, 13, 10),
                'lehmer': (40, 4, 8, 43, 30, 44, 35, 38, 13, 22, 5, 40, 34, 38, 28, 45, 6, 29, 17, 15, 32, 29,
                           3, 34, 18, 10, 25, 23, 21, 23, 9, 21, 7, 28, 26, 21, 20, 13, 9, 23, 17, 0, 14, 18,
                           8, 1, 16, 1, 3, 14, 7, 6, 10, 10, 7, 1, 4, 0, 5, 3, 3, 2, 1, 0),
                'packed': 81341066463989662950936270920469806268596711232567738656487394095083725730493736861738327104,
                'inversions': 1080,
            },
        ]

        for c in cases:
            bp = BitPermutation(c['p'])
            self.assertEqual(bp.as_lehmer_code(), c['lehmer'])
            self.assertEqual(bp.pack(), c['packed'])
            self.assertEqual(bp.get_inversion_count(), c['inversions'])

            q = BitPermutation.from_lehmer_code(c['lehmer'])
            self.assertEqual(q, bp)

            r = BitPermutation.unpack(c['packed'])
            self.assertEqual(r, bp)

    def test_cycles(self):
        cases = [
            {
                'p': (),
                'cycles': [],
            },
            {
                'p': (1, 0),
                'cycles': [[0, 1]],
            },
            {
                'p': [2, 1, 0],
                'cycles': [[0, 2], [1]],
            },
            {
                'p': (2, 0, 3, 1),
                'cycles': [[0, 2, 3, 1]],
            },
            {
                'p': (3, 0, 2, 1),
                'cycles': [[0, 3, 1], [2]],
            },
            {
                'p': (0, 1, 8, 4, 3, 11, 6, 5, 2, 10, 9, 7),
                'cycles': [[0], [1], [2, 8], [3, 4], [5, 11, 7], [6], [9, 10]],
            },
        ]

        for c in cases:
            bp = BitPermutation(c['p'])
            self.assertEqual(bp.as_cycles(), c['cycles'])

    def test_iterable(self):
        bp = BitPermutation((1, 0))
        expected = [0, 2, 1, 3]

        self.assertEqual(list(bp.permute_iter(test_list)), expected)
        self.assertEqual(list(bp.permute_iter(test_tuple)), expected)
        self.assertEqual(list(bp.permute_iter(TestIterator())), expected)
        self.assertEqual(list(bp.permute_iter(test_gen())), expected)

        self.assertEqual(list(bp.invert_iter(test_list)), expected)
        self.assertEqual(list(bp.invert_iter(test_list)), expected)
        self.assertEqual(list(bp.invert_iter(test_list)), expected)
        self.assertEqual(list(bp.invert_iter(test_list)), expected)
