import typing
from dataclasses import dataclass


@dataclass()
class GenRouteInput:
    start: str
    finish: str


@dataclass()
class CreateRouteInput:
    name: str
    points: typing.List[int]
