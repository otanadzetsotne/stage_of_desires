import pygame


class Screen:
    def __init__(
            self,
            screen,
            terrain,
            width,
            height,
    ):
        self.screen = screen
        self.terrain = terrain
        self.width = width
        self.height = height

        # self.screen = pygame.display.set_mode((self.width, self.height))
