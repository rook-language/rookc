from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any


class AtomType(str, Enum):
    NAME = "name"
    NUMBER = "number"


@dataclass
class Atom:
    type_: AtomType
    val: Any


class Name(str):
    pass


@dataclass
class Assign:
    name: Name
    val: int


@dataclass
class BinOp:
    left: int
    right: int
    op: str


@dataclass
class FuncCall:
    name: Name
    args: list


@dataclass
class PyCall:
    func: Callable


@dataclass
class Block:
    items: list[Assign | FuncCall | PyCall]


@dataclass
class Func:
    type_: Name
    name: str
    params: list
    block: Block


def py_call(type_: Name, name: str):
    def wrap(f) -> Func:
        return Func(type_, name, [], Block([PyCall(f)]))

    return wrap


@dataclass
class Source:
    funcs: list[Func]
