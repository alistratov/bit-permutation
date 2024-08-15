"""
The BitShuffle class acts as a container that combines both a permutation and an inversion operation.
"""
from collections.abc import Iterable, Generator

from .permutation import BitPermutation
from .xor import BitInversion


class BitShuffle:
    # --- Initialization ---
    def __init__(self,
                 permutation: BitPermutation | None = None,
                 inversion: BitInversion | None = None,
                 ):
        if permutation is None:
            permutation = BitPermutation()
        if inversion is None:
            inversion = BitInversion()
        self._bp = permutation
        self._bi = inversion

    # --- Special methods ---
    def __len__(self) -> int:
        return max(len(self._bp), len(self._bi))

    @property
    def _key(self) -> tuple:
        return self._bp._key, self._bi._key

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BitShuffle):
            return self._key == other._key
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key)

    def __repr__(self) -> str:
        if self._bp.is_identity() and self._bi.is_identity():
            return f'{self.__class__.__name__}()'
        if self._bi.is_identity():
            return f'{self.__class__.__name__}({self._bp!r})'
        if self._bp.is_identity():
            return f'{self.__class__.__name__}(None, {self._bi!r})'
        return f'{self.__class__.__name__}({self._bp!r}, {self._bi!r})'

    # --- Properties ---
    @property
    def permutation(self) -> BitPermutation:
        return self._bp

    @property
    def inversion(self) -> BitInversion:
        return self._bi

    def is_identity(self) -> bool:
        return self._bp.is_identity() and self._bi.is_identity()

    # --- Transformation ---
    def shuffle(self, x: int) -> int:
        return self._bi.apply(self._bp.permute(x))

    def unshuffle(self, x: int) -> int:
        return self._bp.invert(self._bi.apply(x))

    def shuffle_iter(self, s: Iterable[int]) -> Generator[int, int, None]:
        for x in s:
            yield self.shuffle(x)

    def unshuffle_iter(self, s: Iterable[int]) -> Generator[int, int, None]:
        for x in s:
            yield self.unshuffle(x)

    # --- Representation ---
    def as_tuple(self) -> tuple[int, ...]:
        return *self._bp.as_tuple(), int(self._bi)

    def pack(self) -> int:
        # From LSB to MSB:
        # - packed permutation
        # - inversion as int
        # - length of the inversion in 10 bits
        # - bit 1
        pp = self._bp.pack()
        pl = pp.bit_length()
        ii = int(self._bi)
        il = ii.bit_length()
        return 1 << (pl + il + 10) | il << (pl + il) | ii << pl | pp

    # --- Constructors ---
    @classmethod
    def generate_random(cls, length: int) -> 'BitShuffle':
        """
        Generate a random integer of length N.
        """
        if length < 0:
            raise ValueError('Negative length')
        if length == 0:
            return cls()
        if length == 1:
            return cls(None, BitInversion(1))

        return cls(
            BitPermutation.generate_derangement(length),
            BitInversion.generate_random(length, 0.5),
        )

    @classmethod
    def from_tuple(cls, data: tuple[int, ...]) -> 'BitShuffle':
        if not data:
            # The last number is XOR value. The permutation can be empty.
            raise ValueError('Not enough data to unpack')
        bp = BitPermutation(data[:-1])
        bi = BitInversion(data[-1])
        return cls(bp, bi)

    @classmethod
    def unpack(cls, number: int) -> 'BitShuffle':
        # From LSB to MSB:
        # - packed permutation
        # - inversion as int
        # - length of the inversion in 10 bits
        # - bit 1
        tl = number.bit_length()
        if tl < 11:
            raise ValueError('Not enough data to unpack')

        il = number >> (tl - 11) & 0x3FF
        pl = tl - 11 - il
        ii = number >> pl & ((1 << il) - 1)
        pp = number & ((1 << pl) - 1)
        return cls(BitPermutation.unpack(pp), BitInversion(ii))
