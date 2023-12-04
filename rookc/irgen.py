from collections.abc import Generator

from rich.text import Text
from rich.protocol import rich_cast
from dataclasses import dataclass, field
from rich.panel import Panel
from rich.console import Group

from contextlib import contextmanager


def cast_text(a) -> Text:
    return a.__rich__()


@dataclass
class Instruction:
    name: str
    args: list[int]

    def __repr__(self):
        return f"| {self.name} {' '.join(map(str, self.args))} |"

    def __rich__(self):
        return Text.assemble(
            (self.name, "green"), *[(f" {a}", "magenta") for a in self.args]
        )


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

    def __rich__(self):
        return Text("\n").join(map(cast_text, self.instructions))

    def get_panel(self, name) -> Panel:
        return Panel.fit(rich_cast(self), title=Text(name, "cyan bold"), padding=(0, 2))


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

    def __rich__(self):
        return Group(*(v.get_panel(k) for k, v in self.funcs.items()))
