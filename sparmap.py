"""This module contains a simple parallel map implementation based on
 the multiprocessing package. It allows the use of bounded functions
 as processing functions, and maintains memory usage under control by
 using bounded queues internally.
"""
from multiprocessing import Queue, Process
from collections import namedtuple
import sys
import traceback

TOMBSTONE = '7PE&YeDu5#ybgTf0rJgk9u!'
_MAX_QUEUE_SIZE = 100

_Signal = namedtuple('Signal', ['termination', 'exceptions'])


class Signal(_Signal):
    """Controls the signaling behavior of sparmap.

    If termination is set to True, workers will receive sparmap.TOMBSTONE
    when there is no more work to be done. Otherwise they will be simply
    shut down.

    If exceptions is set to True, sparmap will put place a tuple containing the
    (input element, exception generated) in the results whenever some input causes
    a worker to crash with an exception. Otherwise, such exceptions will simply
    cause the worker to die and generate no other apparent behavior to clients.
    """
    pass


SIGNAL_ALL = Signal(True, True)
SIGNAL_NONE = Signal(False, False)


def parmap(source, fun, workers, max_queue_size=_MAX_QUEUE_SIZE, signal=SIGNAL_NONE):
    """Runs a parallel map operation over a source sequence.

    :param source: a sequence over which to run the parallel map.

    :param fun: a function which will be applied once for each
                element. The function takes a single parameter.

    :param workers: number of parallel workers to use.

    :param max_queue_size: the maximum size of (workers + 1) internal queues.

    :return: an iterator which gets lazily populated with results as they become
             available.

    """
    return parflatmap(source, _mapper(fun), workers, max_queue_size, signal)


def parflatmap(source, fun, workers, max_queue_size=_MAX_QUEUE_SIZE, signal=SIGNAL_NONE):
    """Runs a flat parallel map over a source sequence. The main
    difference of flatmap with respect to a 'regular' parallel map is
    that in flatmap the function 'fun' is supplied an extra parameter
    -- an emitter -- which 'fun' can call to output as many records as
    it wants in response to a single record being input.

    :param source: a sequence over which to run the parallel flat map.

    :param fun: a function which will be applied once for each
           element. The function takes two parameters - one for the
           element, another for an emitter function.

    :param workers: number of parallel workers to use.

    :param max_queue_size: the maximum size of (workers + 1) internal
                           queues.

    :return: an iterator which gets lazily populated with results as
             they become available.

    """
    input_queue = Queue(max_queue_size)
    output_queue = Queue(max_queue_size)

    # Workers (process data).
    processes = [_started(
        Process(target=_worker, args=(input_queue, output_queue, fun, signal))
    ) for i in range(0, workers)]

    # Pusher (pushes data items into work queue).
    pusher = _started(Process(target=_pusher, args=(source, input_queue, workers)))

    return _result(output_queue, processes, pusher)


def _started(process):
    process.daemon = 1
    process.start()
    return process


def _pusher(input, input_queue, n_workers):
    try:
        for task in input:
            input_queue.put(task)
    finally:
        for i in range(0, n_workers):
            input_queue.put(TOMBSTONE)


def _worker(input_queue, output_queue, fun, signal):
    emit = lambda x: output_queue.put(x)
    record = 'if you see this, it is a bug in sparmap'
    try:
        record = input_queue.get()
        while record != TOMBSTONE:
            fun(record, emit)
            sys.stderr.flush()
            record = input_queue.get()

    except Exception:
        ex_type, value = sys.exc_info()[:2]
        if signal.exceptions:
            output_queue.put((record, ex_type, value))

    finally:
        if signal.termination:
            try:
                # tries to dispatch tombstone...
                fun(TOMBSTONE, emit)
            except:
                # ... and if it fails we don't care. Just
                # log the thing.
                traceback.print_exc()

        # Bubbles up exceptions but reports death or
        # __result__ will never terminate.
        sys.stderr.flush()
        output_queue.put(TOMBSTONE)

    sys.stderr.flush()


def _mapper(fun):
    return lambda record, emit: emit(fun(record))


def _result(output_queue, workers, pusher):
    tombstones = 0
    n_workers = len(workers)
    while tombstones != n_workers:
        result = output_queue.get()
        if result == TOMBSTONE:
            tombstones += 1
        else:
            yield result

    # There are no more workers alive, no sense
    # in having a pusher.
    pusher.terminate()
    pusher.join()

    # Waits for children to die.
    for worker in workers:
        worker.join()
