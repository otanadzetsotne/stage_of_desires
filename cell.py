import random

import numpy as np
from PIL import Image


TEXTURES = {
    'GRASSLAND': [(50, 100), (120, 170), (20, 70)],
    'JUNGLE': [(0, 50), (80, 130), (0, 30)],
    'DESERT': [(210, 250), (205, 230), (140, 180)],
    'BEACH': [(240, 255), (220, 240), (170, 200)],
    # 'OCEAN': [(0, 20), (0, 30), (120, 180)],
    'RIVER': [(0, 30), (30, 60), (180, 220)],
    'MOUNTAIN': [(90, 120), (90, 120), (90, 120)],
    'HILLS': [(120, 150), (120, 150), (60, 100)],
    'SNOWY_MOUNTAIN': [(220, 255), (220, 255), (220, 255)],
    'FOREST': [(0, 50), (80, 130), (0, 50)],
    'RAINFOREST': [(0, 30), (70, 110), (0, 30)],
    'PLAINS': [(120, 170), (180, 230), (80, 130)],
    'TUNDRA': [(180, 210), (180, 210), (180, 210)],
    'SWAMP': [(50, 80), (70, 100), (30, 60)],
    # 'LAVA': [(180, 220), (10, 30), (0, 10)],
}

TEXTURES_ = {
        'GRASS': [(25, 75), (100, 200), (25, 75)],
        'SAND': [(200, 250), (190, 220), (150, 180)],
        'WATER': [(0, 25), (0, 50), (200, 255)],
        'MOUNTAIN': [(100, 130), (100, 130), (100, 130)],
}


class Cell:
    def __init__(self, width: int, height: int, texture: str):
        self.width = width
        self.height = height
        self.name = texture
        self._pixels = None

    @property
    def pixels(self):
        if self._pixels is None:
            self._pixels = np.zeros((self.width, self.height, 3), dtype=np.uint8)
            color_ranges = TEXTURES[self.name]
            for idx, color_range in enumerate(color_ranges):
                self._pixels[:, :, idx] = np.random.randint(color_range[0], color_range[1] + 1, (self.width, self.height))

        return self._pixels

    @property
    def color(self):
        return self.pixels.mean(axis=(0, 1)).astype(int)

    def to_img(self, img_out):
        img = Image.fromarray(self.pixels)
        img.save(img_out)


if __name__ == '__main__':
    textures = TEXTURES.keys()
    width_, height_ = 50, 50
    for texture_ in textures:
        Cell(width_, height_, texture_).to_img(f'static/{texture_}.jpeg')
