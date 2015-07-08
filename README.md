sparmap [![Build Status](https://travis-ci.org/gmega/sparmap.svg)](https://travis-ci.org/gmega/parmap)
======

A **S**imple **PAR**allel **MAP** implementation for Python based on the
multiprocessing package. 

Usage
-----
As an example, to sum 1 to all elements in the array `[1, 2, 3, 4, 5]` using two processes in parallel, 
and printing the output on the terminal, you'd write:

```python
from sparmap import parmap

for result in parmap([1, 2, 3, 4, 5], fun=lambda x: x + 1, workers=2):
    print result
```

Streaming
---------
*sparmap* uses a bounded queue internally, and streams results immediately as they 
become available. This means that in a situation like:

```python
for result in parmap(very_long_list, fun=expensive_computation, workers=8):
    print result
```

you will start seeing results as soon as the first computation inside any of the 
workers completes, without having to worry about running out of memory (unless you
have really big records in the input list, or returned as output from your map 
function).

