def use_of_underscore():
    """
    Usage of underscores in python
    source : https://hackernoon.com/understanding-the-underscore-of-python-309d1a029edc
    """

    def _print_x_y(): # single leading inderscore - private
        print('x and y : {x}, {y}'.format(x=x, y=y))
    # ignore value when unpacking
    x, _, y = (1,2,3)
    _print_x_y()

    # ignore multiple values, "Extended upacking not
    # available in < 3.x
    x, *_, y = (1,2,3,4,5,5,6,7)
    _print_x_y()

    # ignore index
    for _ in range(10): print('s', end=' ',sep=' ')

    print()

    list_ =  [(1,2), (3,4)]
    # single trailing underscore - avoiding conflict
    # with builtins names

    for _, val in list_:
        print(val)

    class A:
        def _single_method(self):
            pass

        def __double_method(self):
            # double leading underscore - for mangling
            # cannot be accessed like A().__double_method
            # python add _ClassName to the front of
            # attribute
            # can be accessed like A()._A__double_method()
            pass

        def __str__(self):
            # double leading and trailing underscore
            # for special methods - called magic method
            return 'A!!'

    class B(A):
        def __double_method(self):  # for mangling
            pass

    # used in translations
    # see https://docs.python.org/3/library/gettext.html
    # seperate digits of numbers
    # see https://www.python.org/dev/peps/pep-0515/


if __name__ == '__main__':
    print('PASSING VALUE TO A FUNCTION, PROVIDED THE ARGUMENT NAME IS STORED IN A VARIABLE')


    def one(**kwargs):
        print(kwargs)


    a = 'name_of_argument_in_a_variable'

    one(a='felix')  # that's not what i want
    one(**{a: 'felix'})  # got u
    one(**{a + '_with_modification': 'felix'})

    use_of_underscore()
