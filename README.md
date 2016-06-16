# vigilant-robot
Remote Programming Test

## Usage
Warning: Setting max prime to over 1,000 is where you'll start to see your machine doing a lot of work.

Pro Tip: Use pypy in place of python (the binary is a drop in optimized replacement) to run executions much faster.


###Run program with max prime set to 20
```
python vigilant-robot.py 20
```
or
```
pypy vigilant-robot.py 20
```

###Run program tests (number will be ignored)
```
python vigilant-robot.py 20 -t
```

###(Linux/Mac) Time the execution of the program
```
time python vigilant-robot.py 1000
```

Pypy Performance Comparison
![perf compare](https://raw.githubusercontent.com/RePeet13/vigilant-robot/master/pypy-perf-comparison.png)