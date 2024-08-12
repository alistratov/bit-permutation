# bit-permutation
Shuffle bits in integer numbers.

## Overview
The `bit-permutation` package provides tools for shuffling bits in 
integer numbers. It includes a set of classes designed to handle 
bit permutations.

## Installation
To install the package, run the following command:
```bash
pip install bit-permutation
```

## Usage
The package provides the following classes:
- `BitPermutation` - a class for bit permutations.
- `BitInversion` - a class for bit flipping via XOR.
- `BitShuffle` - a class combining bit permutation and inversion.

### Synopsis
```python
>>> from bit_permutation import BitShuffle
>>> bs = BitShuffle.generate_random(16)
>>> shuffled = [bs.shuffle(x) for x in range(10)]
[42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]

>>> original = [bs.unshuffle(y) for y in shuffled]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> bs.pack()
614290679212893317370896
```

## Classes
### BitPermutation
The `BitPermutation` class appears to handle various aspects of bit permutation, including generating random permutations, checking properties of permutation (like whether it is identity or involution), and providing different representations (cycles, tuples, Lehmer codes).


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
