import time
from sparmap import parmap, parflatmap, SIGNAL_ALL, TOMBSTONE


def process(x):
    return x + 1


def process_with_termination(x):
    if x == TOMBSTONE:
        return 'CLEANUP'

    return process(x)


def faulty(x, lives=[1, 2, 3, 4, 5]):
    lives.pop()
    if not lives:
        raise Exception("Ran out of lives!")

    return process(x)


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


def test_signals_termination():
    result = list(parmap(range(0, 100), process_with_termination, 5, signal=SIGNAL_ALL))
    assert len([x for x in result if x == 'CLEANUP']) == 5
    assert set(x for x in result if x != 'CLEANUP') == set(reference(100))


def test_signals_exceptions():
    result = list(parmap(range(0, 100), faulty, 5, signal=SIGNAL_ALL))
    result.sort()
    print result
    assert len([x for x in result if isinstance(x, tuple)]) == 5

    # can't assert which elements as we never know which ones are missing, we just know
    # the number we expect to have been processed successfully.
    assert len([x for x in result if not isinstance(x, tuple)]) == 20
