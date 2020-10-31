import os


class TestConfig:
    server_port: int = 9003
    users_url: str = os.environ.get(
        'users_url', 'http://localhost:9000')
    routes_url: str = os.environ.get(
        'routes_url', 'http://localhost:9001')
    web_routes_url: str = os.environ.get(
        'web_routes_url', 'http://localhost:9002')


conf = TestConfig()
