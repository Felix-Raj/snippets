"""Going through https://realpython.com/primer-on-python-decorators/"""


def dec1(fun):
    def wrapper():
        print('Before')
        fun()
        print('After')

    return wrapper


def one():
    print('*' * 8)
    print('one')
    print('*' * 8)


one()

one = dec1(one)

one()
