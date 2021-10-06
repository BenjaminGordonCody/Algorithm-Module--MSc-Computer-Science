""" Functions that measure how time efficient other functions are"""

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


if __name__ == "__main__":

    def print_i(i):
        print(f"iteration {i}")

    print(iterations_until_n_seconds(print_i, 0.01))
