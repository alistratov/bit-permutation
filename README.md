# bit-permutation
Shuffle bits in integer numbers.

![PyPI - Version](https://img.shields.io/pypi/v/bit-permutation) [![codecov](https://codecov.io/gh/alistratov/bit-permutation/graph/badge.svg?token=MSJLFL8XFD)](https://codecov.io/gh/alistratov/bit-permutation) [![Documentation Status](https://readthedocs.org/projects/bit-permutation/badge/?version=latest)](https://bit-permutation.readthedocs.io/en/latest/?badge=latest) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bit-permutation) 


## Synopsis
```bash
pip install bit-permutation
```

```python
>>> from bit_permutation import BitShuffle

>>> bs = BitShuffle.generate_random(16) 
>>> shuffled = [bs.shuffle(x) for x in range(10)]
[42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]

>>> original = [bs.unshuffle(y) for y in shuffled]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```


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

2. **Not suitable for highly loaded applications**: The module is not optimized for performance in highly loaded or real-time environments. Users should avoid deploying this module in scenarios where performance and efficiency are critical.

3. **Not for mathematical applications**: Although the module provides some functions for checking the properties of permutations, it is not intended for rigorous mathematical applications. The provided functionality may be useful for basic operations and educational purposes, but is insufficient for advanced or formal studies in combinatorics or group theory.


## Documentation
Read the full documentation at [Read the docs](https://bit-permutation.readthedocs.io/en/latest/).

The package `bit-permutation` provides three classes for export:
* [BitPermutation](https://bit-permutation.readthedocs.io/en/latest/classes/bit_permutation/), which provides functionality to permute bits in an integer number
* [BitInversion](https://bit-permutation.readthedocs.io/en/latest/classes/bit_inversion/), which allows inverting bits in an integer number using the XOR operation
* [BitShuffle](https://bit-permutation.readthedocs.io/en/latest/classes/bit_shuffle/), which combines the functionality of the previous two classes to shuffle bits in an integer number

Instances of all classes are hashable and should be treated as immutable. Instances can be compared for equality within the class.


## License
Copyright 2024 Oleh Alistratov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
