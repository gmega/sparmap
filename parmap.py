"""This module contains a simple parallel map implementation based on
 the multiprocessing package. It allows the use of bounded functions
 as processing functions, and maintains memory usage under control by
 using bounded queues internally.
"""
from multiprocessing import Queue, Process
import sys

TOMBSTONE = '7PE&YeDu5#ybgTf0rJgk9u!'
_MAX_QUEUE_SIZE = 100


def parmap(source, fun, workers, max_queue_size=_MAX_QUEUE_SIZE):
    """Runs a parallel map operation over a source sequence.

    :param source: a sequence over which to run the parallel map.

    :param fun: a function which will be applied once for each
                element. The function takes a single parameter.

    :param workers: number of parallel workers to use.

    :param max_queue_size: the maximum size of (workers + 1) internal queues.

    :return: an iterator which gets lazily populated with results as they become
             available.

    """
    return parflatmap(source, _mapper(fun), workers, max_queue_size)


def parflatmap(source, fun, workers, max_queue_size=_MAX_QUEUE_SIZE):
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
    processes = [_started(Process(target=_worker, args=(input_queue, output_queue, fun)))for i in range(0, workers)]

    # Pusher (pushes data items into work queue).
    pusher = _started(Process(target=_pusher, args=(source, input_queue, workers)))

    return _result(output_queue, processes, pusher)


def _started(process):
    process.start()
    return process


def _pusher(input, input_queue, n_workers):
    for task in input:
        input_queue.put(task)

    for i in range(0, n_workers):
        input_queue.put(TOMBSTONE)


def _worker(input_queue, output_queue, fun):
    try:
        record = input_queue.get()
        while record != TOMBSTONE:
            fun(record, lambda x: output_queue.put(x))
            sys.stderr.flush()
            record = input_queue.get()
    finally:
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

    # Waits for pusher to die.
    pusher.join()

    # Waits for children to die.
    for worker in workers:
        worker.join()
