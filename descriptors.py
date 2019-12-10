# https://realpython.com/python-descriptors/
import time


def is_one_digit_numeric_value(value):
    return 10 > value > -1 and int(value) == value


def function_a(cls):
    print(f'{cls.__name__:-^30}')
    n_1 = cls()
    print(f'Before changing the number {n_1.number}')
    n_1.number = 4
    print(f'After changing the number {n_1.number}')

    n_2 = cls()
    print(f'Before changing the number {n_2.number}')


class VerboseAttribute:
    def __get__(self, instance, owner):
        print("Getting attribute")
        return 80

    def __set__(self, instance, value):
        raise AttributeError("Cannot change value")


class OneDigitNumericValueA:
    def __init__(self):
        self.value = 0

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not is_one_digit_numeric_value(value):
            raise AttributeError
        self.value = value


class OneDigitNumericValueB:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        # works fine only if used as class attribute
        return instance.__dict__.get(self.name) or 0

    def __set__(self, instance, value):
        if not is_one_digit_numeric_value(value):
            raise AttributeError
        instance.__dict__[self.name] = value


class OneDigitNumericValueC:
    def __set_name__(self, owner, name):
        # in 3.6 and above
        # With this new method, whenever you instantiate a descriptor
        # this method is called and the name parameter automatically set.
        self.name = name

    def __get__(self, instance, owner):
        # works fine only if used as class attribute
        return instance.__dict__.get(self.name) or 0

    def __set__(self, instance, value):
        if not is_one_digit_numeric_value(value):
            raise AttributeError
        instance.__dict__[self.name] = value


class Foo1:
    atr = VerboseAttribute()

    def __init__(self):
        self.name = 'Some Name'

    @staticmethod
    def dummy():
        print('Dummy')

    @classmethod
    def new(cls):
        return cls()


class NumericalA:
    number = OneDigitNumericValueA()


class NumericalB:
    # need to specify the name, can be solved
    number = OneDigitNumericValueB('number')


class NumericalC:
    number = OneDigitNumericValueC()


def lazy_property():
    class LazyProperty:
        def __init__(self, function):
            self.function = function

        def __set_name__(self, owner, name):
            self.name = name

        def __get__(self, instance, owner):
            instance.__dict__[self.function.__name__] = self.function(instance)
            return instance.__dict__[self.function.__name__]

    class Some:
        @LazyProperty
        def long_fn(self):
            time.sleep(10)
            return "Urgh!!"

    s = Some()
    print(s.long_fn)  # take 10 seconds
    print(s.long_fn)  # does not take time
    print(s.long_fn)  # does not take time

    # Since it is a non-data descriptor, when you first access the value of
    # the meaning_of_life attribute, .__get__() is automatically called and
    # executes .meaning_of_life() on the my_deep_thought_instance object. The
    # resulting value is stored in the __dict__ attribute of the object itself.
    # When you access the meaning_of_life attribute again, Python will use
    # the lookup chain to find a value for that attribute inside the __dict__
    # attribute, and that value will be returned immediately.
    # Does not work if it is a data-descriptor ( have __set__ or __delete__ )


if __name__ == '__main__':
    # Descriptors are Python objects that implement a method of the descriptor
    # protocol, which gives you the ability to create objects that have
    # special behavior when they’re accessed as attributes of other objects
    f = Foo1()
    print(f'Getting atr {f.atr}')

    # dict of class and objects are different
    print(f"dict of class Foo1 {Foo1.__dict__} \n\t It's instance's "
          f"dict {f.__dict__}")
    # instance methods get accessed via objects dict, class methods and static
    # methods via Class's dict

    # lookup chain for . access
    #   1. Result from __get__ of the *data descriptor* named after the
    #       variable trying to access
    #   2. Value from objects __dict__
    #   3. Result from __get__ of *non-data descriptor* named after the variable
    #   4. Value from object's __dict__
    #   5. Objects parent type's dict is searched
    #   6. Previous step repeated for parent's type in MRO
    # if everything failed, then attribute error

    # signature of get, set, del
    # __get__(self, obj, type=None) -> object
    #           |     |     |
    #           |     |     Type of object to which descriptor is attached to
    # __set__(self, obj, value) -> None
    #           |     |     |
    #           |     |     New value
    #           |     Object to which the descriptor is attached to
    #           Instance of the descriptor
    #
    # set can only be called on object, get can be called on both object and
    # class

    # descriptors are instantiated only once, *per class*
    function_a(NumericalA)

    # can be solved as in
    function_a(NumericalB)

    # better way
    function_a(NumericalC)

    # implementing a lazy property using descriptors
    lazy_property()
