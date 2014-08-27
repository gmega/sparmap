parmap
======

Very simple implementation of parallel map for Python based on the multiprocessing
package. For example, to sum 1 to all elements in the array [1,2,3,4,5] using two 
workers, you'd do:
```
parmap([1,2,3,4], lambda x: x + 1, 2)
```

parmap supports using different functions per worker:

```
parmap([1,2,3,4], [lambda x: x + 1, lambda y: y + 1], 2)
```

and the use of bound functions:
```
def query_server(client, querystring):
    
    def __query_server__(x):
        return client.query(querystring % x)

    return __query_server__
```

