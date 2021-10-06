"""
In this piece of coursework we had to think about complexity in recursive 
functions. We were asked to write a program that returned the nth position in 
the Fibonacci sequence. My initial attempt (fibonacci) starts from 0 and 
recursively calls itself until it has reached the nth position. This worked fine
but I wondered if there was a more elegant solution.

My second attempt(concise_fib) took the opposite approach and started by
defining the nth term by calling itself for the two previous positions. This 
code felt more elegant, but I suspected it would take more resources.

My first function has O(n), because it calls itself once for every position
between 0 and n.

My second function has O(2^n), because each instance of the function has to call
two further instances to get its return value. This renders the function
impractical very quickly.

I created a testing function (timetaken) to measure the actual time each 
implementation took to find the 40th value of the sequence.

fibonacci performed 40 function calls in under 0.001 seconds
concise_fib performed 1,099,511,627,776 function calls in 27.83 seconds

"""
# imports
import time


def timetaken(func, arg):
    """Measures the time it takes for a single argument function to execute"""
    start = time.time()
    func(arg)
    end = time.time()
    return end-start


def iterations_until_n_seconds(func, seconds):
    time_taken = 0
    i = 0
    while time_taken < seconds:
        i += 1
        time_taken = timetaken(func, i)
    return i


def fibonacci(int, fig_a=0, fig_b=0, count=0):
    """ 
    Returns the value of a position in the Fibonacci sequence.
    Figure A and Figure B are the values of the two previous positions.
    """
    # checking the input can be understood
    if int < 1:
        return "usage: only accepts positive integers"
    if int == 1:
        return 1

    # increment counter
    count += 1

    # Value of current position
    sum = fig_a + fig_b

    # If we have calculated the desired number, print it
    if count == int:
        return sum

    # special case for first value of sequence
    elif count == 1:
        return fibonacci(int, 0, 1, count)
    else:
        return fibonacci(int, fig_b, sum, count)


def concise_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return(concise_fib(n-1) + concise_fib(n-2))


if __name__ == "__main__":
    """Tests of functions"""
    print(fibonacci(20))  # if this returns 6765, the function works
    print(concise_fib(20))  # if this returns 6765, the function works

    # # time tests for each function
    # n = 40  # position in sequence to request from functions
    # print(timetaken(fibonacci, n))  # measured 0.0 seconds in test
    # print(timetaken(concise_fib, n))  # measured 27.83 seconds in test

    n = 0.001  # number of seconds to trial funcs against
    print(iterations_until_n_seconds(fibonacci, n))
    print(iterations_until_n_seconds(concise_fib, n))
