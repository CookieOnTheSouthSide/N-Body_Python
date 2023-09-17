from typing import Final
from math import sqrt, atan2, sin, cos
from random import randint

import pygame
"""
Next Implementation: 3d
"""


class Particle:
    MASS: Final[int] = 10
    SIZE: Final[int] = 4
    GRAVITATIONAL_CONSTANT: Final[int] = 6.673 * (10 ** -11)

    def __init__(self, position: list[int, int] = (0, 0),
                 velocity: list[float, float] = (0, 0)):
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.velocity = velocity

    def calculate_velocity(self, center_x: int | float = 0, center_y: int | float = 0, center_mass: int | float = 0):
        distance = sqrt(((center_x - self.x_pos)**2) + ((center_y - self.y_pos)**2))
        force_gravity = (center_mass * self.MASS / distance) * self.GRAVITATIONAL_CONSTANT
        angle = atan2(center_y - self.y_pos, center_x - self.x_pos)
        dx = cos(angle)*force_gravity*10
        dy = sin(angle)*force_gravity*10

        self.velocity[0] += dx*400000000
        self.velocity[1] += dy*400000000

    def update(self):
        self.x_pos += self.velocity[0]
        self.y_pos += self.velocity[1]

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (0, 255, 255), (self.x_pos, self.y_pos), self.SIZE)


class LargeMass(Particle):
    def __init__(self, x: int | float = 0, y: int | float = 0,
                 size: int | float = 1, velocity: list[int, int] = (0, 0),
                 mass: int = 40):
        super().__init__(position=[x, y], velocity=velocity)
        self.size = size
        self.mass = mass
        self.gravity = size * mass

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 165, 0), (self.x_pos, self.y_pos), self.SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()

        self.particles = []
        self.center = LargeMass(self.screen.get_width()/2, self.screen.get_height()/2, 50, [0, 0], 100)

    def setup(self):
        for i in range(1000):
            particle = Particle([randint(10, 790), randint(10, 790)],
                                [randint(-30, 30), randint(-30, 30)])
            self.particles.append(particle)

    def run(self):
        done = False
        self.setup()
        while not done:
            # Drawing
            self.screen.fill('black')

            for p1 in self.particles:
                p1.render(self.screen)
            self.center.render(self.screen)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # self.center.update()
            for thing in self.particles:
                thing.calculate_velocity(self.center.x_pos, self.center.y_pos, self.center.mass)
                thing.update()

            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
