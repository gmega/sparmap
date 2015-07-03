parmap [![Build Status](https://travis-ci.org/gmega/parmap.svg)](https://travis-ci.org/gmega/parmap)
======

Very simple implementation of a parallel map for Python based on the
multiprocessing package. For example, to sum 1 to all elements in the
array `[1, 2, 3, 4, 5]` using two workers, you'd write:

```python
parmap([1, 2, 3, 4], fun=lambda x: x + 1, workers=2)
```

Streaming
---------
parmap uses a bounded queue internally, and streams results immediately
as they become available. This means that in a situation like:

```python
for result in parmap(very_long_list, fun=expensive_computation, workers=8):
    print result
```

you will start seeing results as soon as the computations inside of the 
workers complete.
 
Bound Functions
---------------
parmap will happily

