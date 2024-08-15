from collections.abc import Iterable, Iterator, Generator

__all__ = [
    'test_list',
    'test_tuple',
    'test_gen',
    'TestIterator'
]


test_list = [0, 1, 2, 3]
assert isinstance(test_list, Iterable)
assert not isinstance(test_list, Iterator)
assert not isinstance(test_list, Generator)

test_tuple = (0, 1, 2, 3)
assert isinstance(test_tuple, Iterable)
assert not isinstance(test_tuple, Iterator)
assert not isinstance(test_tuple, Generator)


def test_gen():
    for i in range(4):
        yield i


assert isinstance(test_gen(), Iterable)
assert isinstance(test_gen(), Iterator)
assert isinstance(test_gen(), Generator)


class TestIterator:
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


test_iterator = TestIterator()
assert isinstance(test_iterator, Iterable)
assert isinstance(test_iterator, Iterator)
assert not isinstance(test_iterator, Generator)
