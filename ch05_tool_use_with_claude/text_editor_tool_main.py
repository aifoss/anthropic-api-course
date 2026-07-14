def greeting():
    print("Hi there")


def calculate_pi():
    """Calculate pi rounded to the 5th decimal digit.

    Uses the Nilakantha series, which converges faster than the
    Leibniz series:

        pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...

    Returns:
        float: The value of pi rounded to 5 decimal places (3.14159).
    """
    pi = 3.0
    sign = 1
    # Iterate enough terms to be accurate well beyond 5 decimals.
    for i in range(2, 1000000, 2):
        pi += sign * (4.0 / (i * (i + 1) * (i + 2)))
        sign *= -1
    return round(pi, 5)
