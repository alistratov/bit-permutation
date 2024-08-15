## BitInversion
The `BitInversion` class inverts bits using the XOR (exclusive or) operation. It is straightforward, containing a single bitmask—referred to as the inversion pattern—that specifies which bits to invert.

The length of the inversion pattern is determined by the position of its highest set bit. When the inversion is applied, only the bits within this length are affected; bits beyond this length remain unchanged. This approach ensures correct behavior for both positive and negative numbers.

### Constructors
#### \_\_init__
```python
__init__(self, pattern: int = 0)
```
Initializes the `BitInversion` object with a specified inversion pattern.

- `pattern` (int): bitmask used to determine which bits are inverted. The value must be in range [0, 2<sup>1023</sup> – 1].

#### generate_random
```python
BitInversion.generate_random(length: int, zero_probability: float = 0.5)
```
Generates a random inversion pattern with a specified length in bits and a given probability for zero bits.

### Properties
#### len
Returns the length of the inversion pattern in bits, equivalent to `int.bit_length()`.

For performance reasons, the maximum allowable length is 1023.

#### int
Returns the inversion pattern.

#### is_identity
```python
is_identity() -> bool
```
Checks if the inversion pattern is an identity operation, meaning no bits are inverted; i.e., the inversion pattern is zero.

#### get_number_of_fixed_points
```python
get_number_of_fixed_points() -> int
```
Returns the number of fixed points in the inversion pattern. A fixed point is a bit that remains unchanged after the inversion.

### Transformation
#### apply 
```python
apply(x: int) -> int
```
Applies the inversion pattern to the input integer `x`. The result is the integer with inverted bits. Because XOR operation is reversible, applying the same inversion pattern twice will return the original integer.

#### Generator 
```python
apply_iter(self, s: Iterable) -> Generator[int, int, None]
```
Applies the inversion pattern to each element in the input iterable `s`. The result is a generator that yields integers with inverted bits.

### Examples
The XOR operation is well-known and requires no further explanation.

| Bit position           | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|------------------------|---|---|---|---|---|---|---|---|
| BitInversion() pattern | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| apply() argument       | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| Result                 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 |

Apply the inversion:
```python
bi = BitInversion(0b_1010_1010)
assert bi == 0b_1010_1010

assert bi.apply(0b_1100_1100) == 0b_0110_0110
assert bi.apply(209) == 123
assert bi.apply(-1) == -171
assert bi.apply(bi.apply(209)) == 209

print(len(bi))  # 8
print(bi.is_identity())  # False
print(bi.get_number_of_fixed_points())  # 4
```

Generate random inversions with different densities of zero bits:
```python
b1 = BitInversion.generate_random(32, zero_probability=0.1)
print(bin(b1))  # e.g., 0b11111111111011111111011111101111

b2 = BitInversion.generate_random(32, zero_probability=0.9)
print(bin(b2))  # e.g., 0b10100000010000000000000001000000
```
