import typing
from dataclasses import dataclass


@dataclass()
class GenRouteInput:
    start: int
    finish: int


@dataclass()
class CreateRouteInput:
    name: str
    points: typing.List[int]
