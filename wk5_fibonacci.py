def fibonacci(int, fig_a=0, fig_b=0, count=0):
    """ 
    Returns the value of a position in the Fibonacci sequence.
    For the purpose 
    Figure A and Figure B are the values of the two previous positions.
    The first value of the sequence (n1) doesn't quite follow the sa

    """
    # checking the input can be understood
    if int < 1:
        print("usage: only accepts positive integers")
        return 1
    if int == 1:
        print(1)
        return None

    # increment counter
    count += 1

    # Value of current position
    sum = fig_a + fig_b

    # If we have calculated the desired number, print it
    if count == int:
        print(sum)
        return None

    #
    elif count == 1:
        fibonacci(int, 0, 1, count)

    else:
        fibonacci(int, fig_b, sum, count)
        return None


if __name__ == "__main__":
    for i in range(5):
        fibonacci(i)

    fibonacci(20)  # if this returns 6765, the function works
