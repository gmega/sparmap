import time
from parmap import parmap, parflatmap


def process(x):
    return x + 1


def io_bound(x):
    '''
    io_bound simulates a io_bound (or otherwise longer-running) computation,
    which parmap was initially designed to handle.
    '''
    time.sleep(1)
    return process(x)


def process_flat(x, emit):
    for i in range(0, 100):
        emit(i)


def reference(count):
    return list(process(x) for x in range(0, count))


def test_small():
    result = list(parmap(range(0, 100), process, 1))
    assert result == reference(100)


def test_big():
    result = set(parmap(range(0, 800), io_bound, 500))
    assert result == set(reference(800))


def test_parflat():
    result = [i for i in parflatmap([1, 2, 3, 4], process_flat, 4)]
    result.sort()
    ref = range(0, 100) * 4
    ref.sort()

    print len(result), len(ref)
    assert result == ref
