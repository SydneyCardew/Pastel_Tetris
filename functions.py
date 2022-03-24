import pygame as pg
import json
from classes import tetronimo


def get_colours():
    """retrieves a python dict containing RGB tuples for the colours from the json file"""
    with open('Resources/Settings/colours.json', 'r+') as colour_json:
        colours = json.load(colour_json)
    return colours


def get_pieces():
    """retrieves a python dict containing piece patterns from the json file"""
    with open('Resources/Settings/pieces.json', 'r+') as piece_json:
        pieces = json.load(piece_json)
    return pieces


def get_values():
    """retrieves a python dict containing colour values from the json file"""
    with open('Resources/Settings/values.json', 'r+') as values_json:
        values = json.load(values_json)
    return values


def generate_blank_table(rows, columns):
    return [[0 for i in range(columns)] for j in range(rows)]


def add_tables(table_one, table_two):
    return [[table_one[i][j] + table_two[i][j] for j in range(len(table_one[0]))] for i in range(len(table_one))]


def draw_background(width, height, config):
    """draws the background as a surface"""
    # retrieves the currently configured colours
    colours = get_colours()
    background_colour = config['DEFAULT']['background']
    frame_colour = config['DEFAULT']['frames']
    play_colour = config['DEFAULT']['play_window']
    # draws the surface
    background = pg.Surface((width, height))
    background.fill(colours[background_colour])
    pg.draw.rect(background, colours[frame_colour], pg.Rect(28, 28, 304, 604))
    pg.draw.rect(background, colours[play_colour], pg.Rect(30, 30, 300, 600))
    return background


def draw_block(cell, config):
    colours = get_colours()
    piece_colour_one = config['DEFAULT']['piece_colour_one']
    block = pg.Surface((30, 30))
    pg.draw.rect(block, colours[piece_colour_one], pg.Rect(0, 0, 30, 30))
    return block


def get_table(tetronimo, rows, columns):
    square_list = []
    for y_index, row in enumerate(tetronimo.pattern):
        for x_index, cell in enumerate(row):
            if cell > 0:
                square_list.append([y_index + tetronimo.position[0], x_index + tetronimo.position[1]])
    ghost_table = generate_blank_table(rows, columns)
    new_table = []
    for y_index, row in enumerate(ghost_table):
        new_row = []
        for x_index, cell in enumerate(row):
            if [y_index, x_index] in square_list:
                new_row.append(tetronimo.value)
            else:
                new_row.append(0)
        new_table.append(new_row)
    return new_table


def collision_detector(new_position, dead_table, tet, rows, columns):
    if tet.down_size + new_position[1] > len(dead_table):
        return True
    ghost_tetronimo = tetronimo(new_position, tet.type, tet.rotation)
    collision_table = get_table(ghost_tetronimo, rows, columns)
    for y_index, row in enumerate(dead_table):
        for x_index, cell in enumerate(row):
            if cell > 0 and collision_table[y_index][x_index] > 0:
                return True
    return False






