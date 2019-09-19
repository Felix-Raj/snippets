"""Going through https://realpython.com/primer-on-python-decorators/"""
import functools


def dec1(fun):
    def dec1_wrapper(*args, **kwargs):
        print('Entering wrapper dec1')
        v = fun(*args, **kwargs)
        print('Exiting wrapper dec1')
        return v
    return dec1_wrapper


def dec2(fun):
    @functools.wraps(fun)
    # w/o wraps info on functions like docstring, function name will be lost
    def dec2_wrapper(*args, **kwargs):
        print('Entering wrapper dec2')
        v = fun(*args, **kwargs)
        print('Exiting wrapper dec2')
        return v
    return dec2_wrapper


def add(a, b):
    """Perform addition."""
    print('Performing addition')
    return sum((a, b))


@dec1
def add2(a, b):
    print('Performing addition2')
    return add(a, b)


@dec2
def add3(a, b):
    """Perform addition - 3"""
    print('Performing addition3')
    return add(a, b)


if __name__ == '__main__':
    print('Before decorating')
    print(add(1, 2))
    print(add2(1, 2), end='\n\n')

    print('After decorating')
    add = dec1(add)
    print(add(3, 4))
    print(add2(3, 4), end='\n\n')

    print('Repr of decorated function')
    print(repr(add))
    print(repr(add2), end='\n\n')

    print('What functools.wraps does')
    print('Name of add function ', add.__name__)
    print('Name of add3 function ', add3.__name__)
    print('Doc of add function ', add.__doc__)
    print('Doc of add3 function ', add3.__doc__, end='\n\n')

    print('Continue from "https://realpython.com/primer-on-python-decorators/#fancy-decorators"')
