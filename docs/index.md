The pure-Python `bit-permutation` package provides tools for shuffling bits in integers, including classes designed for bit permutations and inversions.

This module is primarily useful for obscuring monotonically increasing numbers, such as auto-incrementing database identifiers, which can be vulnerable to [Insecure Direct Object Reference](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) as described by OWASP. By rearranging and inverting bits within these identifiers, the sequential nature of the numbers becomes less obvious, adding a layer of security.

While this technique is an example of security through obscurity and should not replace comprehensive information hiding practices, it can still be valuable in various scenarios. The module allows to create a defined or random combination of bit permutation and inversion, resulting in a bijective transformation of a set of integers.

## Table of contents
* [Disclaimer](#disclaimer)
* [Installation](#installation)
* [Example](#example)
* [Package contents](#package-contents)
    * [BitPermutation](classes/bit_permutation.md)
    * [BitInversion](classes/bit_inversion.md)
    * [BitShuffle](classes/bit_shuffle.md)
* [Performance considerations](#performance-considerations)
* [References](references.md)
* [License](license.md)


## Disclaimer
!!! warning ""
    1. **Not intended for cryptographic use**: this module is not designed or intended for use in cryptography. The algorithms and functions provided do not offer the security guarantees required for cryptographic applications.
    1. **Not suitable for highly loaded applications**: the module is not optimized for performance in highly loaded or real-time environments. It should not be used in scenarios where performance and efficiency are critical. See also the [Performance considerations](#performance-considerations) section.
    1. **Not for mathematical applications**: although the module provides functions for checking permutation properties, it is not intended for rigorous mathematical applications. The functionality may be useful for basic operations and educational purposes but is insufficient for advanced combinatorics or group theory studies.


## Installation
Requires Python version 3.10 or higher. To install the package, run:
```bash
pip install bit-permutation
```


## Example
```python
from bit_permutation import BitShuffle

# Generate a random permutation for the lower 16 bits of an integer.
# Any bits higher than the 16th bit remain unaffected.
bs = BitShuffle.generate_random(16)

# Sequential numbers turn into a list, for example,
# [42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]
shuffled = [bs.shuffle(x) for x in range(10)]

# Reverse the shuffling process to retrieve the original numbers:
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
original = [bs.unshuffle(y) for y in shuffled]

# Serialize the BitShuffle object into a single integer, allowing
# the object to be restored later using BitShuffle.unpack().
# Example output: a large integer like 614290679212893317370896
print(bs.pack())
```

## Package contents
The  `bit-permutation` package provides three classes for export:

* [BitPermutation](classes/bit_permutation.md): permutes bits in an integer
* [BitInversion](classes/bit_inversion.md): inverts bits in an integer using XOR
* [BitShuffle](classes/bit_shuffle.md): combines bit permutation and inversion to shuffle bits in an integer

All class instances are hashable and should be treated as immutable. Instances can be compared for equality within the same class.


## Performance considerations
The module uses basic bitwise operations such as shifts and mask applications to perform permutations, rather than advanced algorithms optimized for speed, like the Beneš network or byte swapping. While these methods are not the most efficient, they are straightforward and adequate for many use cases.

As Python is an interpreted language, it is generally slower than compiled languages. The speed of execution can vary depending on several factors, including the specific permutation chosen and the number of bits involved.

However, composite tests indicate that on a modern processor core (as of 2024), the module can perform approximately 1 million operations per second for 16-bit numbers and 100,000 operations per second for 128-bit numbers.
