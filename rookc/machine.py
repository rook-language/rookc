from rookc import parse
from rookc.compiler import compile_
from rookc.irgen import IFunc, IRGen
from rich import print


class StackFrame:
    locals_: list[int]
    args: list[int]

    def __init__(self, locals_: int, args: int):
        self.locals_ = [0 for _ in range(locals_)]
        self.args = [0 for _ in range(args)]


class Machine:
    globals: dict[str, IFunc]
    compute_s: list[int]
    call_s: list[StackFrame]

    def __init__(self):
        self.globals = {}
        self.compute_s = []
        self.call_s = []

    def load(self, ir: IRGen):
        self.globals = ir.funcs

    def call(self, id_: str):
        self.call_s.append(StackFrame(10, 10))

    def run(self, entry: str = "main"):
        self.call(entry)


ast = parse.parse("test.rk")
ir = compile_(ast)

print(ir)

m = Machine()
m.load(ir)
m.run()
