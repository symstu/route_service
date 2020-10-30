import random
import string

from models import Points


def dots_generator():
    for letter in string.ascii_uppercase:
        yield letter, \
              random.randrange(0, 1000), \
              random.randrange(0, 1000)


async def generate_dots():
    await Points.create_many(list(dots_generator()))


def routes_generator(points: list):
    length = len(points)

    for _ in range(0, 10):
        route_dots = []

        for _ in range(0, 5):
            index = random.randrange(0, length)
            route_dots.append(points[index])

        yield ro

async def generate_routes():
    points = await Points.list()
