from dataclasses import dataclass


@dataclass()
class CreateUserRouteInput:
    user_id: int
    route_id: int
    route_length: int
