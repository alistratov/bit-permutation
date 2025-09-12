`bit-permutation` is a pure-Python library for **permuting, shuffling, and inverting bits** in integers.  

It provides reversible (bijective) integer transforms, allowing you to hide sequential patterns in numbers, reorder binary digits, and create deterministic yet non-cryptographic mappings.  

This module is especially useful for **obfuscating monotonically increasing identifiers** (e.g. auto-incrementing database IDs), where exposing predictable values can lead to [Insecure Direct Object Reference](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) vulnerabilities.  
By shuffling and inverting bits, the sequential nature of these numbers becomes less obvious, while the mapping remains fully reversible.  

While this technique is an example of security through obscurity and should not replace comprehensive information hiding practices, it can still be valuable in various scenarios.

---

## Table of contents
* [Use cases](#use-cases)
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

---

## Use cases

Typical scenarios where **bit-permutation** is helpful:

- **Obfuscating database IDs**  
  Hide predictable, auto-incrementing identifiers by mapping them through a reversible permutation of bits. This prevents outsiders from easily inferring how many records exist or guessing other valid IDs.

- **Generating deterministic pseudo-random IDs**  
  Create identifiers that look random but are always reversible to their original values. Useful for lightweight obfuscation where cryptographic strength is not required.

- **Reversible integer encoding**  
  Transform integers into new bit patterns for educational demos, reversible hashing, or simple obfuscation in data pipelines.

---

## Disclaimer
!!! warning ""
    1. **Not intended for cryptographic use**: this module does not provide the guarantees required for cryptographic applications.  
    2. **Not suitable for highly loaded applications**: performance is acceptable for many tasks but not optimized for real-time or heavy workloads. See [Performance considerations](#performance-considerations).
    3. **Not for advanced mathematics**: while basic checks of permutation properties are included, the module is not a substitute for advanced combinatorics or group theory tools.

---

## Installation
Requires Python version 3.10 or higher. To install:
```bash
pip install bit-permutation
```


## Example
```python
from bit_permutation import BitShuffle

# Generate a random permutation for the lower 16 bits of an integer.
# Bits above the 16th remain unaffected.
bs = BitShuffle.generate_random(16)

# Sequential numbers turn into a list, for example,
# [42525, 42517, 9757, 9749, 42509, 42501, 9741, 9733, 34333, 34325]
shuffled = [bs.shuffle(x) for x in range(10)]

# Reverse the shuffling process to retrieve the original numbers:
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
original = [bs.unshuffle(y) for y in shuffled]

# Serialize the BitShuffle object into a single integer, 
# which can later be restored using BitShuffle.unpack().
# Example output: a large integer like 614290679212893317370896
print(bs.pack())
```

---

## Package contents
The  `bit-permutation` package exports three core classes:

* [BitPermutation](classes/bit_permutation.md): permutes bits in an integer
* [BitInversion](classes/bit_inversion.md): inverts bits in an integer using XOR
* [BitShuffle](classes/bit_shuffle.md): combines bit permutation and inversion to shuffle bits in an integer

All instances are hashable, comparable for equality within the same class, and should be treated as immutable.

---

## Performance considerations
The module uses basic bitwise operations such as shifts and mask applications to perform permutations, rather than advanced algorithms optimized for speed, like the Beneš network or byte swapping. While these methods are not the most efficient, they are straightforward and adequate for many use cases.

As Python is an interpreted language, it is generally slower than compiled languages. The speed of execution can vary depending on several factors, including the specific permutation chosen and the number of bits involved.

However, benchmarks indicate that on a modern processor core (as of 2024), the module can perform approximately 1 million operations per second for 16-bit numbers and 100,000 operations per second for 128-bit numbers.

---

## Related terms

bit permutation · bit shuffle · bit reordering · permute bits in Python · invert bits · reversible mapping · bijective integer transform · ID obfuscation · integer obfuscation · non-cryptographic transform · fast bit operations · bitwise manipulation
