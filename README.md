parmap
======

Very simple implementation of a parallel map for Python based on the
multiprocessing package. For example, to sum 1 to all elements in the
array [1,2,3,4,5] using two workers, you'd write:

```python
parmap([1,2,3,4], lambda x: x + 1, 2)
```

parmap supports bound functions:

```python
def query_server(client, querystring):
    
    def __query_server__(x):
        return client.query(querystring % x)

    return __query_server__

parmap(["apples", "oranges", "bananas"], query_server("SELECT * FROM fruit WHERE type = '%s'"), 5)

```

