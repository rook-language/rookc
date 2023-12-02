from rookc import parse
from rookc.irgen import IRGen, IFunc
from rookc.nodes import Source, Func, Assign, BinOp
from rich import print


def evaluate(s, ifunc: IFunc):
    def reval(x):
        return evaluate(x, ifunc)

    if isinstance(s, Assign):
        ifunc.malloc()
        reval(s.val)
        ifunc.set()

    elif isinstance(s, BinOp):
        reval(s.left)
        reval(s.right)
        ifunc.auto_operator(s.op)

    else:
        ifunc.push(s)


def define_func(func: Func, ifunc: IFunc):
    # print(func)
    for s in func.block.items:
        evaluate(s, ifunc)


def compile_(src: Source):
    irgen = IRGen()

    for func in src.funcs:
        with irgen.create_function(func.name) as ifunc:
            define_func(func, ifunc)

    return irgen


ast = parse.parse("test.rk")
ir = compile_(ast)

print(ir)
