from dataclasses import dataclass


@dataclass()
class LoginInput:
    username: str
    password: str


@dataclass()
class RegisterInput(LoginInput):
    pass
