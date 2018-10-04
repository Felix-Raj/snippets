def t(n):
    def p():
        nonlocal n
        n = n + 1
        return n

    return p


counter = t(0)

for _ in range(19):
    print(counter())

del t

for _ in range(19):
    print(counter())


def fib(a, b):
    def f():
        nonlocal a, b
        a, b = b, a + b
        return a, b

    return f


fc = fib(0, 1)

for _ in range(9):
    print(fc())
