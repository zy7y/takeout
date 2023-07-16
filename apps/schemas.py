"""
通用Schema
"""

from typing import Generic, TypeVar, Optional
from pydantic import generics


T = TypeVar('T')


class R(generics.GenericModel, Generic[T]):
    code: int = 1
    data: Optional[T]
    msg: str = "ok"

    @classmethod
    def ok(cls, data: T = None) -> "R":
        return cls(code=1, data=data, msg="ok")

    @classmethod
    def fail(cls, msg: str = "fail") -> "R":
        return cls(code=0, msg=msg)