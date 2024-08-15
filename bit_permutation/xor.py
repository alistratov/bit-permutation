"""
The BitInversion class provides functionality to flip (or invert bits), using XOR operation.
"""
import random
from collections.abc import Iterable, Generator

from .constants import MAX_PERMUTATION_LENGTH


class BitInversion:
    # --- Initialization ---
    def __init__(self, pattern: int = 0):
        if pattern < 0:
            raise ValueError('Negative pattern')

        self._x = pattern
        self._n: int = self._x.bit_length()  # Length of the operand (up to the highest bit set)

        if self._n > MAX_PERMUTATION_LENGTH:
            raise ValueError('Too long pattern')

    # --- Special methods ---
    def __len__(self) -> int:
        return self._n

    @property
    def _key(self) -> int:
        return self._x

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BitInversion):
            return self._key == other._key
        if isinstance(other, int):
            return self._key == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key)

    def __repr__(self) -> str:
        if self._n == 0:
            return f'{self.__class__.__name__}()'
        return f'{self.__class__.__name__}({self._x})'

    def __int__(self) -> int:
        return self._x

    def __index__(self) -> int:
        return self._x

    # --- Properties ---
    def is_identity(self) -> bool:
        return self._x == 0

    def get_number_of_fixed_points(self) -> int:
        """
        Number of fixed points (zero bits).
        """
        if self._n == 0:
            return -1
        return self._n - self._x.bit_count()

    # --- Transformation ---
    def apply(self, x: int) -> int:
        """
        Apply the XOR to the given integer.
        """
        return x ^ self._x

    def apply_iter(self, s: Iterable) -> Generator[int, int, None]:
        """
        Apply the XOR to the given iterable, returning a generator.
        """
        for x in s:
            yield x ^ self._x

    # --- Constructors ---
    @classmethod
    def generate_random(cls, length: int, zero_probability: float = 0.5) -> 'BitInversion':
        """
        Generate a random integer of length N.
        """
        if length < 0:
            raise ValueError('Negative length')
        if length == 0:
            return cls(0)
        if length == 1:
            return cls(1)

        x = 1
        for _ in range(1, length):
            x <<= 1
            if random.random() > zero_probability:
                x |= 1
        return cls(x)
