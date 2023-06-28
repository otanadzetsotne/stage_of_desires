from decimal import Decimal

import pygame
from pygame.locals import *

from render.terrain import Terrain


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up some constants
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1200, 800
        self.map_width, self.map_height = 250, 250
        self.TILE_SIZE = 32

        # Create a screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Create a clock
        self.clock = pygame.time.Clock()

        # Set up some variables for the camera position
        self.cam_x, self.cam_y = 0, 0

        # Store the terrain
        self.terrain = Terrain(self.map_width, self.map_height, self.TILE_SIZE, self.TILE_SIZE, diagonal_cells=True, long_biomes=True)

    def run(self):
        map_width_px = len(self.terrain.terrain[0]) * self.TILE_SIZE
        map_height_px = len(self.terrain.terrain) * self.TILE_SIZE

        running = True
        zoom_scale = 1
        # keys = {K_w: False, K_s: False, K_a: False, K_d: False}
        keys = {K_w: False, K_s: False, K_a: False, K_d: False}
        while running:
            old_zoom_scale = zoom_scale
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key in keys:
                        keys[event.key] = True
                    if event.key == K_r:
                        zoom_scale += .1
                    if event.key == K_f:
                        zoom_scale -= .1
                elif event.type == KEYUP:
                    if event.key in keys:
                        keys[event.key] = False

            if keys[K_w]:
                self.cam_y -= self.TILE_SIZE
            if keys[K_s]:
                self.cam_y += self.TILE_SIZE
            if keys[K_a]:
                self.cam_x -= self.TILE_SIZE
            if keys[K_d]:
                self.cam_x += self.TILE_SIZE

            # Limit zoom scale to reasonable limits
            zoom_scale = max(.5, min(zoom_scale, 1))
            tile_size = int(self.TILE_SIZE * zoom_scale)

            self.cam_x = (self.cam_x + self.SCREEN_WIDTH / 2) * zoom_scale / old_zoom_scale - self.SCREEN_WIDTH / 2
            self.cam_y = (self.cam_y + self.SCREEN_HEIGHT / 2) * zoom_scale / old_zoom_scale - self.SCREEN_HEIGHT / 2

            # Limit camera to map boundaries
            self.cam_x = max(0, min(self.cam_x, map_width_px * zoom_scale - self.SCREEN_WIDTH))
            self.cam_y = max(0, min(self.cam_y, map_height_px * zoom_scale - self.SCREEN_HEIGHT))

            # Draw the terrain
            self.screen.fill((0, 0, 0))

            for i, col in enumerate(self.terrain.terrain):
                for j, row in enumerate(col):
                    # Calculate the screen coordinates of the tile
                    x = int(i * tile_size - self.cam_x)
                    y = int(j * tile_size - self.cam_y)

                    # Only draw the tile if it is within the screen boundaries
                    if -tile_size <= x <= self.SCREEN_WIDTH and -tile_size <= y <= self.SCREEN_HEIGHT:
                    # if -self.TILE_SIZE <= x <= self.SCREEN_WIDTH and -self.TILE_SIZE <= y <= self.SCREEN_HEIGHT:
                        tile = self.terrain.terrain[i][j]
                        tile = pygame.image.frombytes(tile.pixels.tobytes(), (tile.width, tile.height), 'RGB')
                        tile = pygame.transform.scale(tile, (tile_size, tile_size))
                        self.screen.blit(tile, (x, y))

            # Flip the display
            pygame.display.flip()

            # Cap the frame rates
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
