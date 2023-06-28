import pickle
from typing import Optional
from random import choice, randint

import numpy as np
from PIL import Image

from render.cell import TEXTURES, Cell


CELL_WIDTH = 50
CELL_HEIGHT = 50


class Terrain:
    def __init__(
            self,
            terrain_width: int,
            terrain_height: int,
            cell_width: int = CELL_WIDTH,
            cell_height: int = CELL_HEIGHT,
            asymmetric_biome: bool = True,
            asymmetric_biomes_quantity: int = 10,
            symmetric_biome_smoothness: int = 5,
            long_biomes: bool = False,
            diagonal_cells: bool = False,
    ):
        self.width = terrain_width
        self.height = terrain_height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.asymmetric_biome = asymmetric_biome
        self.asymmetric_biomes_quantity = asymmetric_biomes_quantity
        self.symmetric_biome_smoothness = symmetric_biome_smoothness
        self.diagonal_cells = diagonal_cells
        self.long_biomes = long_biomes

        self.texture_names = tuple(TEXTURES.keys())

        self.biomes_meta = {
            'passed': set(),
            'free': dict(),
        }

        self.terrain = self.generate()

    def generate(self):
        terrain: list[list[Optional[Cell]]]
        terrain = [[None for _ in range(self.height)] for _ in range(self.width)]
        cell_counter = 0

        biomes = self.__biomes()
        for x, y in biomes:
            terrain[x][y] = Cell(self.cell_width, self.cell_height, choice(self.texture_names))
            cell_counter += 1

        while biomes:
            rnd_biome = choice(biomes)
            new_cell = self.__biome_new_cell(rnd_biome, terrain)

            if not new_cell:
                biomes.remove(rnd_biome)
                continue

            x, y = new_cell
            texture = terrain[rnd_biome[0]][rnd_biome[1]].name
            terrain[x][y] = Cell(self.cell_width, self.cell_height, texture)

            cell_counter += 1

        return terrain

    def to_img(self, out: str) -> None:
        # Convert each tile to uint8
        map_ = [[tile.pixels.astype(np.uint8) for tile in row] for row in self.terrain]
        # Concatenate the tiles
        full_image = np.concatenate([np.concatenate(row, axis=1) for row in map_], axis=0)
        # Rotate axis
        full_image = np.rot90(full_image, axes=(0, 1))
        # Create a PIL image
        img = Image.fromarray(full_image, 'RGB')
        # Save the image
        img.save(out)

    def to_pickle(self, out) -> None:
        with open(out, 'wb') as f:
            pickle.dump(self, f)

    def __symmetric_biomes(self):
        biomes = []
        for x in range(0, self.width, self.symmetric_biome_smoothness):
            for y in range(0, self.height, self.symmetric_biome_smoothness):
                biomes.append((x, y))

        return biomes

    def __asymmetric_biomes(self):
        biomes = []
        for _ in range(self.asymmetric_biomes_quantity):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            biomes.append((x, y))

        return biomes

    def __biomes(self):
        return self.__asymmetric_biomes() if self.asymmetric_biome else self.__symmetric_biomes()

    def __find_free_cells(self, cell, biome, terrain) -> list[tuple[int, int]]:
        center_x, center_y = cell
        x_less_available = center_x - 1 >= 0
        x_more_available = center_x + 1 < len(terrain)
        y_less_available = center_y - 1 >= 0
        y_more_available = center_y + 1 < len(terrain[0])

        check_cells = []
        if x_less_available:
            check_cells.append((center_x - 1, center_y))
        if y_less_available:
            check_cells.append((center_x, center_y - 1))
        if x_more_available:
            check_cells.append((center_x + 1, center_y))
        if y_more_available:
            check_cells.append((center_x, center_y + 1))

        if self.diagonal_cells:
            if x_less_available and y_less_available:
                check_cells.append((center_x - 1, center_y - 1))
            if x_less_available and y_more_available:
                check_cells.append((center_x - 1, center_y + 1))
            if x_more_available and y_less_available:
                check_cells.append((center_x + 1, center_y - 1))
            if x_more_available and y_more_available:
                check_cells.append((center_x + 1, center_y + 1))

        free_cells = []
        for x, y in check_cells:
            if (x, y) not in self.biomes_meta['passed']:
                if self.long_biomes and (x, y) in self.biomes_meta['free'][biome]:
                    continue
                free_cells.append((x, y))

        return free_cells

    def __biome_new_cell(self, biome_center, terrain) -> tuple[int, int]:
        free_cells = self.biomes_meta['free'][biome_center] = self.biomes_meta['free'].get(biome_center, [])

        if biome_center not in self.biomes_meta['passed']:
            self.biomes_meta['passed'].add(biome_center)
            free_cells += self.__find_free_cells(biome_center, biome_center, terrain)

        biome_new_cell = None
        if free_cells:
            new_i = randint(0, len(free_cells) - 1)
            biome_new_cell = free_cells[new_i]

            for filtering_free in self.biomes_meta['free'].values():
                while biome_new_cell in filtering_free:
                    filtering_free.remove(biome_new_cell)
            self.biomes_meta['passed'].add(biome_new_cell)

            free_cells += self.__find_free_cells(biome_new_cell, biome_center, terrain)

        return biome_new_cell


if __name__ == '__main__':
    width, height = 50, 25
    terrain_ = Terrain(width, height, long_biomes=False, asymmetric_biomes_quantity=20)
    terrain_.to_img('map.png')
    terrain_.to_pickle('map.pickle')


# TODO:
#  * smooth cells
#  * near biomes are logically near
#  * biome probabilities. if it is desert, it is many desert
#  * code optimization
#  * custom objects in biomes
