# bit-permutation
Shuffle bits in integer numbers.

![PyPI - Version](https://img.shields.io/pypi/v/bit-permutation) [![Documentation Status](https://readthedocs.org/projects/bit-permutation/badge/?version=latest)](https://bit-permutation.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/alistratov/bit-permutation/graph/badge.svg?token=MSJLFL8XFD)](https://codecov.io/gh/alistratov/bit-permutation) 


## Overview
The `bit-permutation` package provides tools for shuffling bits in 
integer numbers. It includes a set of classes designed to handle 
bit permutations and inversions.

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


## Disclaimer
1. **Not intended for cryptographic use**: this module is not designed or intended for use in cryptography. The algorithms and functions provided do not offer the security guarantees required for cryptographic applications.

2. **Not suitable for highly loaded applications**: The module is not optimized for performance in highly loaded or real-time environments. Users should avoid deploying this module in scenarios where performance and efficiency are critical. See also the [Performance overview](#performance-overview) section.

3. **Not for mathematical applications**: Although the module provides some functions for checking the properties of permutations, it is not intended for rigorous mathematical applications. The provided functionality may be useful for basic operations and educational purposes, but it should not be relied upon for advanced or formal studies in combinatorics or group theory.


## Installation
Requires Python version 3.10 or higher. To install the package, run the following command:
```bash
pip install bit-permutation
```


## Synopsis
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

# Prints 614290679212893317370896 or whatever, a number that contains 
# the permutation and inversion state and can be used 
# to restore it later with BitShuffle.unpack()
print(bs.pack())
```


## Classes
### BitPermutation
The `BitPermutation` class appears to handle various aspects of bit permutation, including generating random permutations, checking properties of permutation (like whether it is identity or involution), and providing different representations (cycles, tuples, Lehmer codes).

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

## License
Copyright 2024 Oleh Alistratov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
