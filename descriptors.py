# https://realpython.com/python-descriptors/
# https://docs.python.org/3/howto/descriptor.html
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
        # long_fn = LazyProperty(long_fn)
        @LazyProperty
        def long_fn(self):
            time.sleep(10)
            return "Urgh!!"

    s = Some()
    print(s.long_fn)  # take 10 seconds
    print(s.long_fn)  # does not take time
    print(s.long_fn)  # does not take time

    # Since it is a non-data descriptor, when you first access the value of the
    # long_fn attribute, .__get__() is automatically called and executes 
    # .long_fn() on the s object. The resulting value is stored in the __dict__
    #  attribute of the object itself. When you access the long_fn attribute
    # again, Python will use the lookup chain to find a value for that
    # attribute inside the __dict__ attribute, and that value will be returned
    #  immediately.
    # Does not work if it is a data-descriptor ( have __set__ or __delete__ )

def desc_in_parent():
    print('=====================')
    print('Desc in super')
    print('=====================')
    class DataDesc:
        def __set_name__(self, instance, name):
            self.private_name = f'_{name}'
            self.public_name = name
        def __set__(self, instance, value):
            print('setting value in data desc')
            setattr(instance, self.private_name, value)
        def __get__(self, instance, type=None):
            print('getting value in data desc')
            return getattr(instance, self.private_name)
    class NonDataDesc:
        def __get__(self, instance, type=None):
            return 'getting from non-data desc'
    class A:
        dd = DataDesc()
        nd = NonDataDesc()
    class A1:
        dd = DataDesc()
        nd = NonDataDesc

        def __getattribute__(self, name: str):
            print(f'getting {name} in A1')
            if name == 'dd':
                return 'intercepted dd'
            if name == 'nd':
                return 'intercepted nd'
            raise AttributeError
    class A2:
        dd = DataDesc()
        nd = NonDataDesc()

        def __getattr__(self, name):
            if name == 'dd':
                return '__getattr__ on dd'
            if name == 'nd':
                return '__getattr__ on nd'
            return f'attribute {name} does not exist'

        def __getattribute__(self, name: str):
            raise AttributeError
    class B(A):
        def __init__(self):
            super().__init__()
            self.dd = 'some value'
        def fun(self):
            print(f'calling dd in super {super().dd}')
            print(f'calling nd in super {super().nd}')
            print('=======')
            print(f'calling dd in super {self.dd}')
            print(f'calling nd in super {self.nd}')
    class B1(A1):
        def __init__(self):
            self.dd = 'dd was set from b1'
    class B2(A2):
        def __init__(self):
            self.dd = 'dd was set from b2'
    print('__getattribute__ or __getattr__ not implemented')
    b = B()
    b.fun()
    print('__getattribute__ implemented')
    print(B1().dd)
    print(B1().nd)
    print('__getattribute__ and __getattr__ implemented')
    print(B2().dd)
    print(B2().nd)

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
    #   4. Value from object's type's__dict__
    #   5. Objects parent type's dict is searched
    #   6. Previous step repeated for parent's type in MRO
    #   7. if everything failed, then attribute error
    # Access is always via __getattribute__ ( see:
    # https://docs.python.org/3/reference/datamodel.html#object.__getattribute__ )
    # If 1-7 fails, the __getattr__ will be called (if it exists)
    # https://docs.python.org/3/reference/datamodel.html#object.__getattr__
    # Also, if a user calls object.__getattribute__() directly, the 
    # __getattr__() hook is bypassed entirely. This is because of the
    # implementation detail
    # 
    # The logic for super's dotted lookup is in the __getattribute__() method
    # for object returned by super(). A dotted lookup such as super(A, obj).m
    # searches obj.__class__.__mro__ for the base class B immediately following
    # A and then returns B.__dict__['m'].__get__(obj, A). If not a descriptor,
    # m is returned unchanged.
    # 
    # def getattr_hook(obj, name):
    # "Emulate slot_tp_getattr_hook() in Objects/typeobject.c"
    #   try:
    #         return obj.__getattribute__(name)
    #   except AttributeError:
    #         if not hasattr(type(obj), '__getattr__'):
    #             raise
    #   return type(obj).__getattr__(obj, name)             # __getattr__
    # 
    # Attribute lookup doesn’t call object.__getattribute__() directly.
    # Instead, both the dot operator and the getattr() function perform
    # attribute lookup by way of a helper function which is similar to the
    # above one.

    # signature of get, set, del
    # __get__(self, obj, type=None) -> object
    #            |   |     |
    #            |   |     Type of object to which descriptor is attached to
    # __set__(self, obj, value) -> None
    #            |   |     |
    #            |   |     New value
    #            |  Object to which the descriptor is attached to
    #           Instance of the descriptor
    # __delete__(self, obj) -> None
    #
    # __set__ can only be called on object, __get__ can be called on both
    # object and class.

    # descriptors are instantiated only once, *per class*
    function_a(NumericalA)

    # can be solved as in
    function_a(NumericalB)

    # better way
    function_a(NumericalC)

    # implementing a lazy property using descriptors
    lazy_property()

    desc_in_parent()
