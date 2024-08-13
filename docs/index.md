The `bit-permutation` package provides tools for shuffling bits in 
integer numbers. It includes a set of classes designed to handle 
bit permutations and bit inversions.

The primary application of this module is to obscure monotonically
increasing numbers, such as auto-incrementing database identifiers, 
which can be vulnerable to exploitation through 
[Insecure Direct Object Reference](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) 
as described by OWASP. By rearranging and inverting bits 
within these integer identifiers, the sequential nature of them 
can be made less obvious, thereby adding an additional layer of security.

While this technique is an example of security through obscurity 
and should not be relied upon as a substitute for comprehensive
information hiding practices, it can still be valuable in various
scenarios. The module enables the creation of a defined or random
combination of bit permutation and inversion, resulting in a 
bijective transformation of a set of integers.

## Table of contents
- [Disclaimer](#disclaimer)
- [Installation](#installation)
- [Example](#example)
- [Performance overview](#performance-overview)
- Classes:
  - [BitPermutation](classes/bit_permutation.md)
  - [BitInversion](classes/bit_inversion.md)
  - [BitShuffle](classes/bit_shuffle.md)
- [References](references.md)
- [License](license.md)


## Disclaimer
!!! warning ""
    1. **Not intended for cryptographic use**: this module is not designed or intended for use in cryptography. The algorithms and functions provided do not offer the security guarantees required for cryptographic applications.
    1. **Not suitable for highly loaded applications**: the module is not optimized for performance in highly loaded or real-time environments. Users should avoid deploying this module in scenarios where performance and efficiency are critical. See also the [Performance overview](#performance-overview) section.
    1. **Not for mathematical applications**: although the module provides some functions for checking the properties of permutations, it is not intended for rigorous mathematical applications. The provided functionality may be useful for basic operations and educational purposes, but is insufficient for advanced or formal studies in combinatorics or group theory.


## Installation
Requires Python version 3.10 or higher. To install the package, run the following command:
```bash
pip install bit-permutation
```


## Example
```python
from bit_permutation import BitShuffle

# Create a random permutation for lower 16 bits.
# Higher bits will be left unchanged.
bs = BitShuffle.generate_random(16)

# Sequential numbers turn into a list, for example,
# [42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]
shuffled = [bs.shuffle(x) for x in range(10)]

# Back to [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
original = [bs.unshuffle(y) for y in shuffled]

# Prints 614290679212893317370896 or something like that,
# a number that contains the permutation and inversion state and 
# can be used to restore state later with BitShuffle.unpack()
print(bs.pack())
```


## Performance overview
The module leverages basic bitwise operations such as shifts and mask
applications to perform permutations, rather than employing advanced
algorithms optimized for speed, like Beneš transformation network 
or bytes swapping. While methods are not the most optimal, they are
straightforward and sufficient for many use cases.

It's important to note that Python, as an interpreted language, is
generally slower compared to compiled languages. The actual speed of
execution can vary depending on several factors, including the specific
permutation chosen and the number of bits set in the given argument.

However, composite tests have shown that on a modern processor core 
(as of 2024), the module is capable of performing approximately 
1 million operations per second for 16-bit numbers and 
100,000 operations per second for 128-bit numbers.
