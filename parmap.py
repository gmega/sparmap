"""
 This module contains a simple parallel map implementation based on the
 multiprocessing package. This was built mainly to overcome two limitations
 of the implementation supplied with multiprocessing (Pool.map):

 * the requirement of being able to pickle the processor function. With parmap
   you can use whatever you want;
 * input chunking - I wanted to stream records to worker processes and have
   control of what's going on.
"""
from multiprocessing import Queue, Process

TOMBSTONE = '7PE&YeDu5#ybgTf0rJgk9u!'
MAX_QUEUE_SIZE = 100

def parmap(source, fun, workers, max_queue_size=MAX_QUEUE_SIZE):

    """ Runs a parallel map operation over a source sequence.

    :param source: a sequence over which to run the parallel map.
    :param fun: function, or array of functions, to apply to elements. In case it's an array, it
                should be equal to the number of workers.
    :param workers: number of parallel workers to use.
    :param max_queue_size: the maximum size of (workers + 1) internal queues.

    :return: an iterator which gets lazily populated with results as they become
             available.
    """
    funs = __check_expand__(fun, workers)
    input_queue = Queue(max_queue_size)
    output_queue = Queue(max_queue_size)

    for fun in funs:
        Process(target=__worker__, args=(input_queue, output_queue, fun)).start()

    Process(target=__pusher__, args=(source, input_queue, workers)).start()

    return __result__(output_queue, workers)


def __check_expand__(funs, workers):

    try:
        if (len(funs) != workers):
            raise Exception("The number of worker functions has to match the number of workers.")
    except TypeError:
        # Assumes it's a function.
        return [funs for i in range(0, workers)]


def __pusher__(input, input_queue, n_workers):

    for task in input:
        input_queue.put(task)

    for i in range(0, n_workers):
        input_queue.put(TOMBSTONE)


def __worker__(input_queue, output_queue, fun):

    try:
        record = input_queue.get()
        while record != TOMBSTONE:
            output_queue.put(fun(record))
            record = input_queue.get()
    finally:
        # Bubbles up exceptions but reports death or
        # __result__ will never terminate.
        output_queue.put(TOMBSTONE)


def __result__(output_queue, n_workers):

    tombstones = 0
    while tombstones != n_workers:
        result = output_queue.get()
        if result == TOMBSTONE:
            tombstones += 1
        else:
            yield result
