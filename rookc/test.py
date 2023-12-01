from collections.abc import Callable


class ComposableWrapper:
    f: Callable

    def __init__(self, f: Callable):
        self.f = f

    def __add__(self, other: Callable):
        def wrap():
            self.f()
            other()

        return ComposableWrapper(wrap)

    def __gt__(self, other) -> "ComposableWrapper":
        def wrap(*args, **kwargs):
            return other(self.f(*args, **kwargs))

        return ComposableWrapper(wrap)

    def __lt__(self, other):
        return self(other)

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def _composable(f: Callable):
    return ComposableWrapper(f)


composable = _composable(_composable)


@composable
def say_hello():
    print("hello")


@composable
def say_goodbye():
    print("goodbye")


@composable
def double(a):
    return a * 2


@composable
def add_five(a):
    return a + 5


double_and_add_five = double > add_five

add_five_and_double = add_five > double

print(double_and_add_five(2))
print(add_five_and_double(2))

print(3 > (double > add_five > double))