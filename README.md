# vigilant-robot
Remote Programming Test

## Problem Statement
You are given a function 'secret()' that accepts a single integer parameter and returns an integer. In your favorite programming language, write a command-line program that takes one command-line argument (a number) and determines if the secret() function is additive [secret(x+y) = secret(x) + secret(y)], for all combinations x and y, where x and y are all prime numbers less than the number passed via the command-line argument. Describe how to run your examples. Please generate the list of primes without using built-in functionality.


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

##Pypy Single Threaded Performance Comparison
![perf compare](https://raw.githubusercontent.com/RePeet13/vigilant-robot/master/pypy-perf-comparison.png)

##Pypy Multiprocessing Performance Comparison
![perf compare](https://raw.githubusercontent.com/RePeet13/vigilant-robot/master/pypy-perf-comparison-2-threads.png)

