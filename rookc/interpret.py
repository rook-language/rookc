import parse
from rich import print

from rookc.nodes import Source, Func, Assign, FuncCall, py_call, PyCall


@py_call("void", "print")
def print_(s):
    print(s)


class Interpreter:
    globals: dict[str, Func]

    def __init__(self):
        self.globals = {}
        self.define_func(print_)

    def run(self, src: Source):
        print(src)
        for f in src.funcs:
            self.define_func(f)

        self.call_func("main", [])

    def call_func(self, name: str, params: list):
        f: Func = self.globals[name]
        locals_ = {}

        for s in f.block.items:
            if isinstance(s, Assign):
                locals_[s.name] = s.val
            elif isinstance(s, FuncCall):
                self.call_func(s.name, s.args)

            elif isinstance(s, PyCall):
                s.func(*params)

    def define_func(self, func: Func):
        self.globals[func.name] = func


ast = parse.parse("test.rk")
interpreter = Interpreter()

interpreter.run(ast)
