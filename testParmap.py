import nose
import time
from parmap import parmap


def process(x):
    return x + 1


def io_bound(x):
    '''
    io_bound simulates a io_bound computation, which parmap was initially
    designed to handle.
    '''
    time.sleep(1)
    return process(x)


def reference(count):
    return list(process(x) for x in range(0, count))


def test_small():
    result = list(parmap(range(0, 100), process, 1))
    assert result == reference(100)


def test_big():
    result = set(parmap(range(0, 800), io_bound, 500))
    assert result == set(reference(800))


def test_heterogeneous():
    pass # have to figure out a good way to test this.

