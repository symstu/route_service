import typing

from dataclasses import dataclass


@dataclass()
class GenerateRouteInput:
    start: int
    finish: int


@dataclass()
class SaveRouteInput:
    name: int
    points: str
