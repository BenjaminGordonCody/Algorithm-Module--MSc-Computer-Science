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
between 0 and i.

My second function has O(2^n), because each instance of the function has to call
two further instances to get its return value. This renders the function
impractical very quickly.

I created a function (timetaken) to measure the actual time each
implementation took to find the 40th value of the sequence.

fibonacci performed 40 function calls in under 0.001 seconds
concise_fib performed 1,099,511,627,776 function calls in 27.83 seconds

My initial function is the more efficient one."""

# imports
import time  # used for testing time performance of functions


def fibonacci(i, fig_a=0, fig_b=0, count=0):
    """
    Returns the value of a position in the Fibonacci sequence.
    Figure A and Figure B are the values of the two previous positions.
    'i' is the position we are trying to discover.
    """
    # checking the input can be understood
    if i < 1:
        return "usage: only accepts positive integers"
    if i == 1:
        return 1

    # increment counter
    count += 1

    # Value of current position
    current_value = fig_a + fig_b

    # If we have calculated the desired number, print it
    if count == i:
        return current_value

    # special case for first value of sequence
    if count == 1:
        return fibonacci(i, 0, 1, count)
    else:
        return fibonacci(i, fig_b, current_value, count)


def concise_fib(i):
    """returns position i of Fibonacci sequence"""
    if i == 0:
        return 0
    if i == 1:
        return 1
    else:
        return concise_fib(i-1) + concise_fib(i-2)


if __name__ == "__main__":
    """Tests of functions"""

    def timetaken(func, arg):
        """Measures the time it takes for a single argument function to execute"""
        start = time.time()
        func(arg)
        end = time.time()
        return end - start

    if fibonacci(20) == 6765:
        print("'fibonacci' accurately identifies 20th position as 6765")
    if concise_fib(20) == 6765:
        print("'concise_fib' accurately identifies 20th position as 6765")

    # time tests for each function
    i_to_test = 40  # position in sequence to request from functions
    print(
        f"'fibonacci' took {timetaken(fibonacci, i_to_test)}s to find position {i_to_test}")
    print(
        f"'concise_fib' took {timetaken(concise_fib, i_to_test)}s to find position {i_to_test}")
