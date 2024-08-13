## BitPermutation
The `BitPermutation` class appears to handle various aspects of bit permutation, including generating random permutations, checking properties of permutation (like whether it is identity or involution), and providing different representations (cycles, tuples, Lehmer codes).


### Constructors
#### \_\_init__
```python
__init__(self, permutation: Iterable[int] | None = None)
```
Initializes the `BitPermutation` object with a specified permutation.

- `permutation` (Iterable): a sequence of integers that represent the new positions of bits. 

The permutation is defined in one-line notation, where the index of the element corresponds to the original bit position, and the value at that index is the new position of the bit. For example, the permutation `(2, 0, 1)` means that the bit at position 0 moves to position 2, the bit at position 1 moves to position 0, and the bit at position 2 moves to position 1.

If there's no permutation provided, the identity permutation is created, which means that no bits are moved.

The last elements of the permutation are ignored if they are equal to their index, that is, if the bits in the corresponding positions are not moved. For example, the permutation `(2, 0, 1, 3, 4)` will be reduced to `(2, 0, 1)`. This also means that all identical permutations are reduced to an empty permutation, and their length is zero.

The length of the permutation must be less than or equal to 1023.

#### generate_random
```python
generate_random(cls, length: int) -> BitPermutation
```
Generates a random permutation of a specified length.

#### generate_derangement
```python
generate_derangement(cls, length: int) -> BitPermutation
```
Generates a random derangement of a specified length. A derangement is a permutation where no fixed points exist, meaning that no bit remains in its original position.

#### generate_involution
```python
generate_involution(cls, length: int) -> BitPermutation
```
Generates a random involution permutation of a specified length. An involution is a permutation that is its own inverse, meaning that applying the permutation twice returns the original sequence.

#### from_lehmer_code
```python
from_lehmer_code(cls, lehmer: Iterable) -> BitPermutation
```
Creates a permutation from a Lehmer code. The Lehmer code is a sequnce of integers described below in the [`as_lehmer_code()`](#as_lehmer_code) method.

#### unpack
```python
unpack(cls, number: int) -> BitPermutation
```
Restores the permutation from the integer. The packed integer should be obtained using the [`pack()`](#pack) method.


### Properties
#### len
Returns the length of the permutation. For performance reasons, the maximum allowable length is 1023. The identity permutation has a length of zero. 

#### is_identity
```python
is_identity() -> bool
```
Checks if the permutation is the identity permutation. The identity permutation is the one where no bits are moved.

#### is_derangement
```python
is_derangement() -> bool
```
Checks if the permutation is a derangement. A derangement is a permutation in which none of the elements appear in their original positions, meaning there are no fixed points.

#### is_involution
```python
is_involution() -> bool
```
Checks if the permutation is an involution. An involution is a permutation that is its own inverse, meaning that applying the permutation twice returns the original sequence.

#### get_number_of_fixed_points
```python
get_number_of_fixed_points() -> int
```
Returns the number of fixed points (elements that are mapped to themselves) in the permutation.

#### get_inversion_count
```python
get_inversion_count() -> int
```
The inversion count is the number of pairs of elements that are out of order. A higher sum indicates a more complex permutation. The highest possible sum is `(length - 1) * (length - 2) / 2` and corresponds to the reverse permutation.

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
Returns the permutation as a list of disjoint cycles. For example, the permutation `(2, 0, 1)` is represented as `[[0, 2], [1]]`.

#### as_lehmer_code
```python
as_lehmer_code(self) -> tuple[int, ...]
```
Returns the permutation as a Lehmer code, which is a tuple of integers representing the number of elements smaller than the current element to the right. 

For example, the permutation `(2, 0, 1)` is represented as `(2, 0, 0)`.

See details in [Wikipedia / Lehmer code](https://en.wikipedia.org/wiki/Lehmer_code).

#### pack
```python
pack() -> int
```
Packs the permutation into a single integer. The packed integer can be used to restore the permutation later using the `unpack` class method.

Caution, the resulting number can be very large. Despite the compact method of encoding the Lemaire code as a number in factorial notation, which means a compact notation, the total number of possible permutations is equal to a factorial of length.


### Examples
The operation of excluding or is well known and needs no explanation.

| Bit position           | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|------------------------|---|---|---|---|---|---|---|---|
| BitPermutation() pattern | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| apply() argument       | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| Result                 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 |

```python
inversion = BitPermutation(0b_1010_1010)

assert inversion.apply(0b_1100_1100) == 0b_0110_0110
assert inversion.apply(209) == 123
assert inversion.apply(-1) == -171
assert inversion.apply(inversion.apply(209)) == 209

print(len(inversion))  # 8
print(inversion.is_identity())  # False
print(inversion.get_number_of_fixed_points())  # 4
```

Generate random inversions with different densities of zero bits:
```python
r1 = BitPermutation.generate_random(32, zero_probability=0.1)
print(bin(r1))  # e.g., 0b11111111111011111111011111101111

r2 = BitPermutation.generate_random(32, zero_probability=0.9)
print(bin(r2))  # e.g., 0b10100000010000000000000001000000
```
