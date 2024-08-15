from collections.abc import Iterable, Iterator, Generator

__all__ = [
    'sample_list',
    'sample_tuple',
    'sample_gen',
    'SampleIterator'
]


sample_list = [0, 1, 2, 3]
assert isinstance(sample_list, Iterable)
assert not isinstance(sample_list, Iterator)
assert not isinstance(sample_list, Generator)

sample_tuple = (0, 1, 2, 3)
assert isinstance(sample_tuple, Iterable)
assert not isinstance(sample_tuple, Iterator)
assert not isinstance(sample_tuple, Generator)


def sample_gen():
    for i in range(4):
        yield i


assert isinstance(sample_gen(), Iterable)
assert isinstance(sample_gen(), Iterator)
assert isinstance(sample_gen(), Generator)


class SampleIterator:
    # Iterator, but not generator
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 4:
            raise StopIteration
        n, self.n = self.n, self.n + 1
        return n


sample_iterator = SampleIterator()
assert isinstance(sample_iterator, Iterable)
assert isinstance(sample_iterator, Iterator)
assert not isinstance(sample_iterator, Generator)
