from dataclasses import dataclass


@dataclass()
class LoginForm:
    username: str
    password: str


@dataclass()
class RegisterForm(LoginForm):
    password_confirmation: str
