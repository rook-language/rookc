from typing import Any

import parse
from rich import print


from rookc.nodes import (
    Source,
    Func,
    Assign,
    FuncCall,
    py_call,
    PyCall,
    Atom,
    AtomType,
    BinOp,
    Name,
)


@py_call("void", "print")
def print_(s):
    print(f"PRINT: {s}")


class Interpreter:
    globals: dict[str, Func]

    def __init__(self):
        self.globals = {}
        self.define_func(print_)

    def run(self, src: Source):
        for f in src.funcs:
            self.define_func(f)

        print(self.globals)

        self.call_func("main", [])

    def call_func(self, name: str, params: list):
        f: Func = self.globals[name]
        locals_: dict[str, Any] = {}

        for s in f.block.items:
            self.evaluate_expr(s, params, locals_)

    def evaluate_expr(self, s, params: list, locals_: dict[str, Any]):
        def reval(x):
            return self.evaluate_expr(x, params, locals_)

        if isinstance(s, Assign):
            locals_[s.name] = reval(s.val)

        elif isinstance(s, FuncCall):
            args_eval = []
            for a in s.args:
                args_eval.append(reval(a))
            self.call_func(s.name, args_eval)

        elif isinstance(s, PyCall):
            s.func(*params)

        elif isinstance(s, BinOp):
            if s.op == "+":
                return reval(s.left) + reval(s.right)
            if s.op == "-":
                return reval(s.left) - reval(s.right)
            if s.op == "*":
                return reval(s.left) * reval(s.right)
            if s.op == "/":
                return reval(s.left) // reval(s.right)

        elif isinstance(s, Name):
            if s in locals_:
                return locals_[s]
            if s in self.globals:
                return self.globals[s]
            raise IndexError

        else:
            return s

    def define_func(self, func: Func):
        self.globals[func.name] = func


ast = parse.parse("test.rk")
interpreter = Interpreter()

interpreter.run(ast)
