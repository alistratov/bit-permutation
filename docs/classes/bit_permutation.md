## BitPermutation
The `BitPermutation` class handles various aspects of bit permutation, including generating random permutations, checking properties such as whether the permutation is an identity or an involution, and providing different representations (cycles, tuples, Lehmer codes).

### Constructors
#### \_\_init__
```python
__init__(self, permutation: Iterable[int] | None = None)
```
Initializes the `BitPermutation` object with a specified permutation.

- `permutation` (Iterable): a sequence of integers that represent the new positions of bits. 

The permutation is defined in one-line notation, where the index of the element corresponds to the original bit position, and the value at that index is the new position of the bit. For example, the permutation `(2, 0, 1)` means that the bit at position 0 moves to position 2, the bit at position 1 moves to position 0, and the bit at position 2 moves to position 1.

If no permutation is provided, the identity permutation is created, meaning no bits are moved.

Trailing elements of the permutation that match their index, i.e., bits that remain in their original positions, are ignored. For example, the permutation `(2, 0, 1, 3, 4)` is reduced to `(2, 0, 1)`. Consequently, all identity permutations reduce to an empty permutation.

The length of the permutation must be less than or equal to 1023.

#### generate_random
```python
BitPermutation.generate_random(length: int)
```
Generates a random permutation of a specified length.

#### generate_derangement
```python
BitPermutation.generate_derangement(length: int)
```
Generates a random derangement of a specified length. A derangement is a permutation where no fixed points exist, meaning that no bit remains in its original position.

#### generate_involution
```python
BitPermutation.generate_involution(length: int)
```
Generates a random involution permutation of the specified length. An involution is a permutation that is its own inverse, meaning applying the permutation twice returns the original sequence.

#### from_lehmer_code
```python
BitPermutation.from_lehmer_code(lehmer: Iterable)
```
Creates a permutation from a Lehmer code, which is a sequence of integers. See the [`as_lehmer_code()`](#as_lehmer_code) method for more details.

#### unpack
```python
BitPermutation.unpack(number: int)
```
Restores the permutation from a packed integer. The packed integer should be obtained using the [`pack()`](#pack) method.

### Properties
#### len
Returns the length of the permutation. For performance reasons, the maximum allowable length is 1023. The identity permutation has a length of zero. This also means the interesting fact that the length of a permutation is never equal to one.

#### is_identity
```python
is_identity() -> bool
```
Checks if the permutation is the identity permutation, where no bits are moved.

#### is_derangement
```python
is_derangement() -> bool
```
Checks if the permutation is a derangement, where no bits remain in their original positions (i.e., there are no fixed points).

#### is_involution
```python
is_involution() -> bool
```
Checks if the permutation is an involution, meaning that applying the permutation twice returns the original value.

#### get_number_of_fixed_points
```python
get_number_of_fixed_points() -> int
```
Returns the number of fixed points (elements that are mapped to themselves) in the permutation.

#### get_inversion_count
```python
get_inversion_count() -> int
```
Returns the inversion count, which is the number of pairs of elements that are out of order. A higher inversion count indicates a more complex permutation. The highest possible count is `(length - 1) * (length - 2) / 2`, corresponding to the reverse permutation.

### Transformations
#### permute
```python
permute(x: int) -> int
```
Applies the permutation to the input integer `x` and returns the result.

#### invert
```python
invert(x: int) -> int
```
Applies the inverse of the permutation to the input integer `x` and returns the result.

#### Generators 
```python
permute_iter(self, s: Iterable) -> Generator[int, int, None]
invert_iter(self, s: Iterable) -> Generator[int, int, None]
```
Applies the permutation or its inverse to each element in the input iterable `s`. The result is a generator that yields integers with permuted bits.

### Representations
#### as_tuple
```python
as_tuple() -> tuple[int, ...]
```
Returns the permutation as a tuple of integers, as defined in the constructor.

#### as_cycles
```python
as_cycles() -> list[list[int]]
```
Returns the permutation as a list of disjoint cycles. For example, the permutation `(2, 1, 0)` is represented as `[[0, 2], [1]]`, meaning the bits at positions 0 and 2 are swapped, while the bit at position 1 remains unchanged.

#### as_lehmer_code
```python
as_lehmer_code(self) -> tuple[int, ...]
```
Returns the permutation as a Lehmer code, a tuple of integers representing the number of elements smaller than the current element to the right. 

For example, the permutation `(2, 0, 1)` is represented as `(2, 0, 0)`.

For more details, see [Lehmer code](https://en.wikipedia.org/wiki/Lehmer_code) on Wikipedia.

#### pack
```python
pack() -> int
```
Packs the permutation into a single integer. The packed integer can be used to restore the permutation later using the `unpack` method.

**Caution**: the resulting number can be very large. Despite encoding the Lehmer code in the [factorial number system](https://en.wikipedia.org/wiki/Factorial_number_system), which offers a compact representation, the total number of possible permutations equals the factorial of the sequence length, and increases rapidly as the permutation length increases.

### Examples
Create a permutation and check its properties:
```python
bp = BitPermutation((2, 0, 3, 1))

assert bp.permute(0b1010) == 0b0011
assert bp.invert(0b0011) == 0b1010
assert bp.invert(bp.permute(0xDEADBEEF)) == 0xDEADBEEF

print(len(bp))  # 4
print(bp.get_number_of_fixed_points())  # 0
print(bp.get_inversion_count())  # 3
print(bp.is_identity())  # False
print(bp.is_derangement())  # True
print(bp.is_involution())  # False

print(bp.as_tuple())  # (2, 0, 3, 1)
print(bp.as_cycles())  # [[0, 2, 3, 1]]
print(bp.as_lehmer_code())  # (2, 0, 1, 0)
print(bp.pack())  # 13316

recovered = BitPermutation.unpack(13316)
print(recovered.as_tuple())  # (2, 0, 3, 1)
assert recovered == bp 
```

Generate random permutations:
```python
b1 = BitPermutation.generate_random(4)
print(b1.as_tuple())  # (2, 3, 1, 0)

b2 = BitPermutation.generate_derangement(4)
print(b2.as_tuple())  # (2, 0, 3, 1)

b3 = BitPermutation.generate_involution(4)
print(b3.as_tuple())  # (0, 1, 3, 2)
```

The involution: 
```python
bp = BitPermutation.generate_involution(32)
x = 0xDEADBEEF
assert bp.permute(bp.invert(x)) == x
assert bp.permute(bp.permute(x)) == x
assert bp.invert(bp.invert(x)) == x
```
