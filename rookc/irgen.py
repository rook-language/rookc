from collections.abc import Generator

from rich import print
from dataclasses import dataclass, field

from contextlib import contextmanager


@dataclass
class Instruction:
    name: str
    args: list[int]

    def __repr__(self):
        return f"| {self.name} {' '.join(map(str, self.args))} |"


@dataclass
class IFunc:
    instructions: list = field(default_factory=list)

    def append(self, name: str, *args: int):
        self.instructions.append(Instruction(name, list(args)))

    def push(self, val: int):
        self.append("push", val)

    def malloc(self):
        self.append("malloc")

    def set(self):
        self.append("set")

    def add(self):
        self.append("add")

    def sub(self):
        self.append("sub")

    def mul(self):
        self.append("mul")

    def div(self):
        self.append("div")

    def auto_operator(self, op):
        ops = {"+": self.add, "-": self.sub, "*": self.mul, "/": self.div}

        ops[op]()

    def __repr__(self):
        return "\n".join(map(str, self.instructions))


@dataclass
class IRGen:
    funcs: dict[str, IFunc] = field(default_factory=dict)

    @contextmanager
    def create_function(self, id_: str) -> Generator[IFunc, None, None]:
        new_func = IFunc()
        yield new_func
        self.funcs[id_] = new_func

    def __repr__(self):
        return "\n\n".join(
            [f"-== {k} ==- : \n" + str(v) for k, v in self.funcs.items()]
        )
