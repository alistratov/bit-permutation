import unittest
import random
import time

from bit_permutation import BitPermutation
from .decorators import loading_tests_enabled

"""
Length 2: 0.221s 4519641.2 ops/s
Length 3: 0.238s 4200497.4 ops/s
Length 4: 0.281s 3555349.6 ops/s
Length 8: 0.451s 2217078.8 ops/s
Length 16: 1.051s 951358.1 ops/s
Length 32: 2.444s 409106.7 ops/s
Length 51: 4.024s 248520.2 ops/s
Length 64: 5.175s 193253.3 ops/s
Length 128: 10.674s 93686.0 ops/s
Length 256: 22.845s 43773.7 ops/s
Length 512: 50.861s 19661.5 ops/s
Length 1023: 118.617s 8430.5 ops/s
"""


class LiveRandomPermutations(unittest.TestCase):
    @loading_tests_enabled
    def test_random(self):
        PASSES = 10
        LENGTHS = (2, 3, 4, 8, 16, 32, 51, 64, 128, 256, 512, 1023)
        SAMPLES = 100

        n_total = 0
        n_ident = 0
        n_involution = 0
        n_derangement = 0

        for _p in range(PASSES):
            for n in LENGTHS:
                bp = BitPermutation.generate_random(n)
                n_total += 1
                n_ident += int(bp.is_identity())
                n_involution += int(bp.is_involution())
                n_derangement += int(bp.is_derangement())

                # Check permutation properties
                self.assertEqual(len(bp), n)
                fp = bp.get_number_of_fixed_points()

                if bp.is_derangement():
                    self.assertEqual(fp, 0)

                cycles = bp.as_cycles()
                cn1 = 0
                for c in cycles:
                    if len(c) == 1:
                        cn1 += 1
                self.assertEqual(fp, cn1)

                tuples = bp.as_tuple()
                from_tuples = BitPermutation(tuples)
                self.assertEqual(bp, from_tuples)

                lehmer = bp.as_lehmer_code()
                from_lehmer = BitPermutation.from_lehmer_code(lehmer)
                self.assertEqual(bp, from_lehmer)

                packed = bp.pack()
                unpacked = BitPermutation.unpack(packed)
                self.assertEqual(bp, unpacked)

                # Test different values
                sample_range = 1 << (n + 1)  # make it 1 bit longer
                for _s in range(SAMPLES):
                    x = random.randrange(sample_range)
                    y = bp.permute(x)

                    if bp.is_identity():
                        self.assertEqual(y, x)
                    elif bp.is_involution():
                        self.assertEqual(bp.invert(y), x)
                        self.assertEqual(bp.permute(y), x)
                    else:
                        self.assertEqual(bp.invert(y), x)

        print('Total:', n_total)
        print('Identity:', n_ident)
        print('Involution:', n_involution)
        print('Derangement:', n_derangement)

        PERMS = 10
        LENGTHS = (2, 3, 4, 8, 16, 32, 51, 64, 128, 256, 512, 1023)
        SAMPLES = 10_000

        print(f'Load testing... {PERMS * SAMPLES} samples')
        for n in LENGTHS:
            val = (1 << (n + 1)) - 1
            t1 = time.perf_counter()

            for _p in range(PERMS):
                bp = BitPermutation.generate_derangement(n)

                for _s in range(SAMPLES):
                    bp.permute(val)

            t2 = time.perf_counter()
            print(f'Length {n}: {t2 - t1:.3f}s {PERMS * SAMPLES / (t2 - t1):.1f} ops/s')
