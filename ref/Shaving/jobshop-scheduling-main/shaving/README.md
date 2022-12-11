## Shaving
**Shaving** is a generic term of algorithm which adjusts heads and tails for the better.  
Currently, implemented shaving algorithm is only \[1\].

### What is heads and tails?
In the job-shop scheduling problem, each job has upper bound of processing start time and lower bound of it.  
Former is called _heads_ and difference between given upper bound of makespan and later is called _tails_.  
If we are able to increase their values, optimization time will decrease.  

## Testing
You can test shaving algorithm or its procudures by executing following commands.  

### Test shaving results
```
$ python -m unittest shaving.tests.test_shaving
```

### Test procedures
```
$ python -m unittest shaving.tests.<procedures name>
```

### Test everything
```
$ python -m unittest shaving.tests
```

## Implemented theses
1. Carlier, J., and Pinson, E. (1994), "Adjustments of heads and tails
for the job-shop problem', *European Journal of Operational
Research* 78, 146-161.