from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Assign:
    name: str
    val: int


@dataclass
class FuncCall:
    name: str
    args: list


@dataclass
class PyCall:
    func: Callable


@dataclass
class Block:
    items: list[Assign | FuncCall | PyCall]


@dataclass
class Func:
    type_: str
    name: str
    params: list
    block: Block


def py_call(type_: str, name: str):
    def wrap(f) -> Func:
        return Func(
            type_,
            name,
            [],
            Block([PyCall(f)])
        )

    return wrap


@dataclass
class Source:
    funcs: list[Func]
