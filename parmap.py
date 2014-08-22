""" parmap: a simple parallel map implementation based on the multiprocessing package.
    This was built to overcome the limitations of Pool.map in my specific contect; namely:
     * input chunking - I wanted to process things in a stream;
     * the requirement of being able to pickle the processor function. With parmap you can use whatever you want.

"""
from multiprocessing import Queue, Process

__author__ = 'giuliano'

TOMBSTONE = '7PE&YeDu5#ybgTf0rJgk9u!'
MAX_QUEUE_SIZE = 100

def parmap(source, fun, workers, max_queue_size=MAX_QUEUE_SIZE):
    """
    Runs a parallel map operation over a source iterator.

    :param source: iterator over which to run the parallel map.
    :param fun: function to apply to each element.
    :param workers: parallelism degree.
    :param max_queue_size: the maximum size of (workers + 1) internal queues.

    :return: an iterator which gets lazily populated with results as they become available.
    """
    output_queue = Queue(max_queue_size)
    input_queue = Queue(max_queue_size)

    for i in range(0, workers):
        Process(target=__worker__, args=(input_queue, output_queue, fun)).start()

    Process(target=__pusher__, args=(source, input_queue, workers)).start()

    return __result__(output_queue, workers)


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

    poison_pills = 0
    while poison_pills != n_workers:
        result = output_queue.get()
        if result == TOMBSTONE:
            poison_pills += 1
        else:
            yield result
