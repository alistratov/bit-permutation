# bit-permutation
Shuffle bits in integer numbers.

[![PyPI - Version](https://img.shields.io/pypi/v/bit-permutation)](https://pypi.org/project/bit-permutation/) [![codecov](https://codecov.io/gh/alistratov/bit-permutation/graph/badge.svg?token=MSJLFL8XFD)](https://codecov.io/gh/alistratov/bit-permutation) [![Documentation Status](https://readthedocs.org/projects/bit-permutation/badge/?version=latest)](https://bit-permutation.readthedocs.io/en/latest/?badge=latest) [![PyPI - Downloads](https://img.shields.io/pypi/dm/bit-permutation)](https://pypistats.org/packages/bit-permutation)


## Synopsis
```bash
pip install bit-permutation
```

```python-repl
>>> from bit_permutation import BitShuffle

>>> bs = BitShuffle.generate_random(16)  # Permutation for lower 16 bits
>>> bs.shuffle(123)
41868
>>> bs.unshuffle(41868)
123

>>> shuffled = [bs.shuffle(x) for x in range(10)]
>>> shuffled
[42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]

>>> [bs.unshuffle(y) for y in shuffled]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```


## Overview
The pure-Python `bit-permutation` package provides tools for shuffling bits in integers, including classes designed for bit permutations and inversions.

This module is primarily useful for obscuring monotonically increasing numbers, such as auto-incrementing database identifiers, which can be vulnerable to [Insecure Direct Object Reference](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) as described by OWASP. By rearranging and inverting bits within these identifiers, the sequential nature of the numbers becomes less obvious, adding a layer of security.

While this technique is an example of security through obscurity and should not replace comprehensive information hiding practices, it can still be valuable in various scenarios. The module allows to create a defined or random combination of bit permutation and inversion, resulting in a bijective transformation of a set of integers.


## Disclaimer
1. **Not intended for cryptographic use**: this module is not designed or intended for use in cryptography. The algorithms and functions provided do not offer the security guarantees required for cryptographic applications.

2. **Not suitable for highly loaded applications**: the module is not optimized for performance in highly loaded or real-time environments. It should not be used in scenarios where performance and efficiency are critical.

3. **Not for mathematical applications**: although the module provides functions for checking permutation properties, it is not intended for rigorous mathematical applications. The functionality may be useful for basic operations and educational purposes but is insufficient for advanced combinatorics or group theory studies.

## Documentation
Read the full documentation at [Read the docs](https://bit-permutation.readthedocs.io/en/latest/).

The `bit-permutation` package provides three classes for export:
* [BitPermutation](https://bit-permutation.readthedocs.io/en/latest/classes/bit_permutation/): permutes bits in an integer
* [BitInversion](https://bit-permutation.readthedocs.io/en/latest/classes/bit_inversion/): inverts bits in an integer using XOR
* [BitShuffle](https://bit-permutation.readthedocs.io/en/latest/classes/bit_shuffle/): combines bit permutation and inversion to shuffle bits in an integer

All class instances are hashable and should be treated as immutable. Instances can be compared for equality within the same class.


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
