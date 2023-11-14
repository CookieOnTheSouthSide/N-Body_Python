from typing import Final
from math import sqrt
from random import randint

import pygame
import pygame.gfxdraw
from pygame.math import Vector2

"""
Next Implementation: 3d
"""


class Particle:
    MASS: Final[int] = 10
    SIZE: Final[int] = 4
    GRAVITATIONAL_CONSTANT: Final[float] = 6.673 * (10 ** -11)

    def __init__(self, position: tuple[int, int] = (0, 0),
                 velocity: tuple[float, float] = (0, 0)):
        self.pos = Vector2(position)
        self.velocity = Vector2(velocity)
        self.trail = []

    def calculate_velocity(self, center_pos: Vector2 = 0, center_mass: int | float = 0):
        distance = (center_pos - self.pos)
        force_gravity = (center_mass * self.MASS / distance.magnitude()) * self.GRAVITATIONAL_CONSTANT
        norm_factor = 1 / distance.magnitude()
        direction = (distance * norm_factor) * force_gravity * 40000000

        self.velocity += direction

    def update(self):
        self.pos += self.velocity

    def render(self, surface: pygame.Surface):
        self.trail.append((int(self.pos.x), int(self.pos.y)))
        for point in self.trail:
            pygame.gfxdraw.circle(surface, point[0], point[1], 1, (0, 255, 255, 255))

        if len(self.trail) > 1000:
            self.trail.pop(0)


class LargeMass(Particle):
    def __init__(self, x: int | float = 0, y: int | float = 0,
                 size: int | float = 1, velocity: tuple[int, int] = (0, 0),
                 mass: int = 40):
        super().__init__(position=(x, y), velocity=velocity)
        self.size = size
        self.mass = mass
        self.gravity = size * mass

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 165, 0), self.pos, self.SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()

        self.particles = []
        self.center = LargeMass(self.screen.get_width() / 2, self.screen.get_height() / 2, 100, [1, 1], 500)

    def setup(self):
        for i in range(100):
            particle = Particle((randint(10, 790), randint(10, 790)),
                                (randint(1, 25), randint(0, 10)))
            self.particles.append(particle)

    def run(self):
        done = False
        self.setup()
        while not done:
            # Drawing
            self.screen.fill("black")

            for p1 in self.particles:
                p1.render(self.screen)
            self.center.render(self.screen)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # self.center.update()
            for thing in self.particles:
                thing.calculate_velocity(self.center.pos, self.center.mass)
                thing.update()

            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
