#!/bin/python3

from PIL import Image, ImageDraw
from typing import List, Tuple
import json
import sys

SCALE: int = 50
BORDER: int = 10
PATH_TRANSPARENCY = 'FF'  # transparency in hexadecimal format (00..FF)


COLOR_PALETTE_8 = [
    '#191970',  # midnightblue
    '#006400',  # darkgreen
    '#ff0000',  # red
    '#ffd700',  # gold
    '#00ff00',  # lime
    '#00ffff',  # aqua
    '#ff00ff',  # fuchsia
    '#ffb6c1',  # lightpink
]

COLOR_PALETTE_16 = [
    '#2f4f4f',  # darkslategray
    '#800000',  # maroon
    '#006400',  # darkgreen
    '#00008b',  # darkblue
    '#ff0000',  # red
    '#ffa500',  # orange
    '#ffff00',  # yellow
    '#00ff00',  # lime
    '#00fa9a',  # mediumspringgreen
    '#00ffff',  # aqua
    '#0000ff',  # blue
    '#ff00ff',  # fuchsia
    '#1e90ff',  # dodgerblue
    '#f0e68c',  # khaki
    '#ff1493',  # deeppink
    '#ffb6c1',  # lightpink
]


class BoardDrawer:
    def __init__(self, solution: dict) -> None:
        self.width: int = solution['board']
        self.height: int = solution['board']
        self.regions: List[Tuple[int, int]] = solution['regions']
        self.connections: List[List[int]] = solution['connections']

        # colors
        if 0 in solution['colors']:
            self.colors = solution['colors']
        else:
            self.colors: List[int] = [c - 1 for c in solution['colors']]
       
        self.color_range: int = len(set(self.colors))
        self.__convert_cartesian_board_cords()
        self.__create_plane()
        self.__create_board()

    def __convert_cartesian_board_cords(self):
        for region in self.regions:
            region[1] = (self.height - 1) - region[1]

    def __image_cords(self, x: int, y: int) -> Tuple[int, int]:
        im_x = x * SCALE + BORDER + self.__board_dim[0][0]
        im_y = y * SCALE + BORDER + self.__board_dim[0][1]
        return im_x, im_y

    def __create_plane(self):
        inner_width, inner_height = (
            self.width - 1) * SCALE + 3 * BORDER, (self.height - 1) * SCALE + 3 * BORDER

        im_dim = inner_width + BORDER, inner_height + BORDER

        self.__board_dim = ((BORDER, BORDER), (inner_width, inner_height))

        self.__img = Image.new('RGBA', im_dim)
        self.__draw = ImageDraw.Draw(self.__img)

        # draw outline plane
        self.__draw.rectangle([(0, 0), im_dim], fill=(0, 0, 0))

        # draw inline plane
        self.__draw.rectangle(self.__board_dim,  fill=(84, 84, 84))

        # draw points
        for x in range(self.width):
            for y in range(self.height):
                im_x, im_y = self.__image_cords(x, y)
                self.__draw.rectangle(
                    ((im_x - 1, im_y - 1), (im_x + 1, im_y + 1)), fill=(120, 120, 120))

    def __create_board(self):
        def draw_line(start: Tuple[int, int], end: Tuple[int, int], color=(255, 255, 255, 125)):
            line_seq = tuple((self.__image_cords(x, y)
                              for x, y in (start, end)))
            self.__draw.line(line_seq, width=SCALE//4,
                             joint="curve", fill=color)

        def draw_point(x: int, y: int):
            x, y = self.__image_cords(x, y)
            self.__draw.ellipse(((x - SCALE//4, y - SCALE//4),
                                 (x + SCALE // 4, y + SCALE//4)),
                                fill=(255, 255, 255), outline=(0, 0, 0))

        color_palette = COLOR_PALETTE_8 if self.color_range < 9 else COLOR_PALETTE_16

        # draw connections
        for i, connections in enumerate(self.connections):
            start = self.regions[i]
            color = f'{color_palette[self.colors[i] % len(color_palette)]}{PATH_TRANSPARENCY}'
            for index in connections:
                end = self.regions[index]
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                draw_line(start, (start[0] + dx / 2,
                                  start[1] + dy / 2), color=color)

        # draw points
        for x, y in self.regions:
            draw_point(x, y)

    def get_image(self) -> Image.Image:
        return self.__img.copy()
