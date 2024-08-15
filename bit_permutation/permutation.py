"""
The BitPermutation class handles the creation and manipulation of bit permutations.
It offers methods for generating permutations, checking permutation properties, and converting
between different permutation representations.
"""
import random
from collections.abc import Iterable, Generator, Callable

from .constants import MAX_PERMUTATION_LENGTH, PERM_2, PERM_3_NOFP, PERM_3_INVOL


class BitPermutation:
    # --- Helpers ---
    factorials: list[int] = []

    @classmethod
    def _factorial(cls, n: int) -> int:
        if not cls.factorials:
            cls.factorials = [1]
        while n >= len(cls.factorials):
            cls.factorials.append(cls.factorials[-1] * len(cls.factorials))
        return cls.factorials[n]

    @staticmethod
    def _truncate(p: list[int]) -> tuple[int, tuple[int, ...]]:
        # Remove most significant elements if they are equal to their index
        i = len(p) - 1
        while 0 <= i == p[i]:  # i >= 0 and p[i] == i:
            i -= 1

        if i < 0:
            return 0, ()
        else:
            return i + 1, tuple(p[:i + 1])

    @staticmethod
    def _num_of_fixed_points(p: tuple[int, ...] | list[int]) -> int:
        # Calculate number of fixed points (elements that are mapped to themselves)
        return sum(1 for i, v in enumerate(p) if i == v)

    @staticmethod
    def _random_list(length: int) -> list[int]:
        s = list(range(length))
        random.shuffle(s)
        return s

    # --- Initialization ---
    def __init__(self, permutation: Iterable[int] | None = None):
        if permutation is None:
            p = []
        else:
            p = list(permutation)

        # Members
        self._n: int  # Length of the permutation
        self._p: tuple[int, ...]  # List of target positions of elements
        self._num_fixed_points: int  # Number of fixed points (elements that are mapped to themselves)
        self._is_involution: bool  # Is the permutation an involution?

        self._n, self._p = self._truncate(p)
        if self._n > MAX_PERMUTATION_LENGTH:
            raise ValueError(f'Maximum length of a permutation is {MAX_PERMUTATION_LENGTH}')

        # Check validity
        if not self._is_valid():
            raise ValueError('Invalid permutation')

        # Determine number of fixed points
        self._num_fixed_points = self._num_of_fixed_points(self._p)

        # Inverted permutation
        inv = [0] * self._n
        for i, v in enumerate(self._p):
            inv[v] = i
        self._inv = tuple(inv)

        # Determine if the permutation is an involution
        self._is_involution = self._p == self._inv

        # Masks for the lowest N bits
        self._lowest_mask = (1 << self._n) - 1
        self._neg_lowest_mask = ~self._lowest_mask

        # Generate code
        # Sure, I could choose not to generate code for identical permutations,
        # but who in their right mind would really use identical permutations?
        # Let the behaviour remain common to them, even if it's inefficient.
        self._fn_permute = self._gen_code(self._p)
        if self._is_involution:
            self._fn_inverse = self._fn_permute
        else:
            self._fn_inverse = self._gen_code(self._inv)

    def _is_valid(self) -> bool:
        """
        Ensure that each number from 0 to N - 1 appears exactly once in the permutation.
        In other words, all numbers must be in range [0, N) and unique.
        This method should be called only once during the initialization.
        """
        return all(0 <= x < self._n for x in self._p) and len(self._p) == self._n and len(set(self._p)) == self._n

    @staticmethod
    def _gen_code(permutation: tuple[int, ...]) -> Callable[[int], int]:
        # Group bits by their distance from the original position
        distances: dict[int, int] = {}
        for i, v in enumerate(permutation):
            distances[v - i] = distances.get(v - i, 0) | (1 << i)
        table = [(mask, distance) for distance, mask in distances.items()]

        # Generate code
        terms = []
        for mask, distance in table:
            if distance > 0:
                terms.append(f"((x & {mask}) << {distance})")
            elif distance < 0:
                terms.append(f"((x & {mask}) >> {-distance})")
            else:
                terms.append(f"(x & {mask})")

        if not terms:
            code = 'x'
        else:
            code = '|'.join(terms)

        return eval(f'lambda x: {code}')  # noqa: S307

    # --- Special methods ---
    def __len__(self) -> int:
        # Interesting fact: in this implementation, the length is never equal to one
        return self._n

    @property
    def _key(self) -> tuple[int, ...]:
        return self._p

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BitPermutation):
            return self._key == other._key
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._key)

    def __repr__(self) -> str:
        if self._n == 0:
            return f'{self.__class__.__name__}()'
        return f'{self.__class__.__name__}({self._p})'

    # --- Properties ---
    def is_identity(self) -> bool:
        """
        Permutation is identity if it maps each element to itself.
        """
        return self._n == 0

    def is_derangement(self) -> bool:
        """
        A derangement is a permutation in which none of the elements appear in their original positions,
        meaning there are no fixed points.
        """
        return self._n != 0 and self._num_fixed_points == 0

    def is_involution(self) -> bool:
        """
        An involution is a permutation that is its own inverse.
        Applying the permutation twice produces the original value.
        """
        return self._is_involution

    def get_number_of_fixed_points(self) -> int:
        """
        Number of fixed points (elements that are mapped to themselves).
        """
        return self._num_fixed_points if self._n != 0 else -1

    def get_inversion_count(self) -> int:
        """
        The inversion count is the number of pairs of elements that are out of order.
        The inversion count is equal to the sum of the Lehmer code.
        A higher sum indicates a more complex permutation.
        The highest possible sum is (N - 1) * (N - 2) / 2 and corresponds to the reverse permutation.
        """
        return sum(self.as_lehmer_code())

    # --- Transformation ---
    def _apply_function(self, x: int, fun: Callable[[int], int]) -> int:
        return x & self._neg_lowest_mask | fun(x & self._lowest_mask)

    def permute(self, x: int) -> int:
        """
        Apply the permutation to the given integer.
        """
        return self._apply_function(x, self._fn_permute)

    def invert(self, x: int) -> int:
        """
        Apply the inverse of permutation to the given integer.
        """
        return self._apply_function(x, self._fn_inverse)

    def permute_iter(self, s: Iterable) -> Generator[int, int, None]:
        """
        Apply the permutation to the given iterable, returning a generator.
        """
        for x in s:
            yield self.permute(x)

    def invert_iter(self, s: Iterable) -> Generator[int, int, None]:
        """
        Apply the inverse of permutation to the given iterable, returning a generator.
        """
        for x in s:
            yield self.invert(x)

    # --- Representation ---
    def as_tuple(self) -> tuple[int, ...]:
        return self._p

    def as_cycles(self) -> list[list[int]]:
        """
        Returns a list of disjoint cycles.
        """
        visited = [False] * self._n
        cycles = []
        for i in range(self._n):
            if visited[i]:
                continue
            cycle = [i]
            visited[i] = True
            j = self._p[i]
            while j != i:
                cycle.append(j)
                visited[j] = True
                j = self._p[j]
            cycles.append(cycle)
        return cycles

    def as_lehmer_code(self) -> tuple[int, ...]:
        """
        https://en.wikipedia.org/wiki/Lehmer_code
        """
        lehmer = [0] * self._n
        for i in range(self._n):
            c = 0
            for j in range(i + 1, self._n):
                if self._p[j] < self._p[i]:
                    c += 1
            lehmer[i] = c
        return tuple(lehmer)

    def pack(self) -> int:
        """
        Represent permutation as an integer: encode its Lehmer code in factoradic and add the length.
        """
        lehmer = reversed(self.as_lehmer_code())
        number = 0
        for i, v in enumerate(lehmer):
            number += v * self._factorial(i)

        # Max length is 1023, so we can pack it in 10 bits
        return (number << 10) | self._n

    # --- Constructors ---
    @classmethod
    def generate_random(cls, length: int) -> 'BitPermutation':
        """
        Generate a random permutation of length N.
        Raises exception if N less than 2, because permutations of length 0 and 1 are identity.

        If we encounter a permutation with an ordered tail, we keep trying.
        I really hate algorithms with non-guaranteed execution time, but let it be, it's fast enough to keep it simple.
        """
        if length <= 1:
            raise ValueError(f'Permutation of length {length} cannot be random')
        if length == 2:
            return cls(PERM_2)

        while True:
            s = cls._random_list(length)
            sn, sp = cls._truncate(s)
            if sn == length:
                return cls(sp)

    @classmethod
    def generate_derangement(cls, length: int) -> 'BitPermutation':
        """
        Generate a random derangement of length N.
        Raises exception if N less than 2.

        This function is even worse.
        But since the probability of getting a permutation without fixed points is 1 / e ≈ 0.367879,
        we have to wait for a relatively short time.
        """
        if length <= 1:
            raise ValueError(f'Permutation of length {length} cannot be a derangement')
        if length == 2:
            return cls(PERM_2)
        if length == 3:
            return cls(random.choice(PERM_3_NOFP))

        while True:
            s = cls._random_list(length)
            sn, sp = cls._truncate(s)
            if sn == length:
                fp = cls._num_of_fixed_points(sp)
                if fp == 0:
                    return cls(sp)

    @classmethod
    def generate_involution(cls, length: int, fixed_point_probability: float = 0.5) -> 'BitPermutation':
        """
        Generate a random involution of length N.
        Raises exception if N less than 2.

        The probability of a permutation being an involution is 1/2.
        """
        if length <= 1:
            raise ValueError(f'Permutation of length {length} cannot be an involution')
        if length == 2:
            return cls(PERM_2)
        if length == 3:
            return cls(random.choice(PERM_3_INVOL))

        if fixed_point_probability < 0 or fixed_point_probability >= 1:
            raise ValueError('Fixed point probability must be in range [0, 1)')
        if fixed_point_probability > 0.99:
            fixed_point_probability = 0.99  # Avoid very long loops

        while True:
            p: list[int] = list(range(length))
            visited: list[bool] = [False] * length

            for i in range(length):
                if not visited[i]:
                    is_fixed = random.random() <= fixed_point_probability
                    if not is_fixed and i < length - 1:
                        # Find an element to swap with that hasn't been visited yet
                        available_indices = [j for j in range(i + 1, length) if not visited[j]]
                        if available_indices:
                            j = random.choice(available_indices)
                            p[i], p[j] = p[j], p[i]
                            visited[j] = True
                    # Mark the current element as visited
                    visited[i] = True

            sn, sp = cls._truncate(p)
            if sn == length:
                return cls(p)

    @classmethod
    def from_lehmer_code(cls, lehmer: Iterable) -> 'BitPermutation':
        lehmer = list(lehmer)
        elements = list(range(len(lehmer)))
        perm = []

        for val in lehmer:
            elem = elements.pop(val)
            perm.append(elem)

        return cls(perm)

    @classmethod
    def unpack(cls, number: int) -> 'BitPermutation':
        """
        Convert the integer to permutation: extract the length and decode its Lehmer code from factorial number system.
        """
        length = number & 0x3FF
        number >>= 10
        lehmer = [0] * length
        for i in range(length):
            f = cls._factorial(length - i - 1)
            lehmer[i] = number // f
            number %= f

        return cls.from_lehmer_code(lehmer)
