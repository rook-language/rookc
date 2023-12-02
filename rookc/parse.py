from lark import Lark, Transformer
from rich import print

from rookc.nodes import (
    FuncCall,
    Assign,
    Block,
    Func,
    Source,
    Atom,
    AtomType,
    BinOp,
    Name,
)


class RookTransformer(Transformer):
    SIGNED_NUMBER = int

    def CNAME(self, t):
        return Name(t.value)

    def bin_op(self, t):
        return BinOp(t[0], t[2], t[1].value)

    def func_call(self, t):
        return FuncCall(t[0], t[1:])

    def assign(self, t):
        return Assign(t[0], t[1])

    def block(self, t):
        return Block(t)

    def func(self, t):
        return Func(t[0], t[1], t[2], t[3])

    def start(self, t):
        return Source(t)


with open("grammar.lark") as f:
    parser = Lark(f.read(), parser="lalr", transformer=RookTransformer())


def parse(file):
    with open(file) as f:
        ast = parser.parse(f.read())
        return ast
