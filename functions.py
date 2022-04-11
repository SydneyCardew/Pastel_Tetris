import pygame as pg
import json
from classes import tetronimo
from random import seed
from random import randint


def random_tetronimo(last_tet=None):
    """This function selects the next tetronimo (crude, rework)"""
    if last_tet:
        type = last_tet.type
    else:
        type = None
    seed()
    selector = randint(1, 7)
    if selector == 1:
        if type == 'j':
            return tetronimo([0, 4], 'z', 0)
        else:
            return tetronimo([0, 4], 'j', 0)
    elif selector == 2:
        if type == 'o':
            return tetronimo([0, 4], 'j', 0)
        else:
            return tetronimo([0, 4], 'o', 0)
    elif selector == 3:
        if type == 'i':
            return tetronimo([0, 4], 'o', 0)
        else:
            return tetronimo([0, 4], 'i', 0)
    elif selector == 4:
        if type == 'l':
            return tetronimo([0, 4], 'i', 0)
        else:
            return tetronimo([0, 4], 'l', 0)
    elif selector == 5:
        if type == 's':
            return tetronimo([0, 4], 'l', 0)
        else:
            return tetronimo([0, 4], 's', 0)
    elif selector == 6:
        if type == 't':
            return tetronimo([0, 4], 's', 0)
        else:
            return tetronimo([0, 4], 't', 0)
    elif selector == 7:
        if type == 'z':
            return tetronimo([0, 4], 't', 0)
        else:
            return tetronimo([0, 4], 'z', 0)


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
    """Makes a blank game array"""
    return [[0 for i in range(columns)] for j in range(rows)]


def add_tables(table_one, table_two):
    """adds two arrays of the same size"""
    return [[table_one[i][j] + table_two[i][j] for j in range(len(table_one[0]))] for i in range(len(table_one))]


def draw_background(width, height, config, next_tet, score, level):
    """draws the background as a surface"""
    # retrieves the currently configured colours
    colours = get_colours()
    background_colour = config['DEFAULT']['background']
    frame_colour = config['DEFAULT']['frames']
    play_colour = config['DEFAULT']['play_window']
    text_colour = config['DEFAULT']['text_colour']
    # font initialisation
    pg.font.init()
    display_font = pg.font.SysFont('Corbel', 20)
    score_font = pg.font.SysFont('Corbel', 15)
    # draws the background
    background = pg.Surface((width, height))
    background.fill(colours[background_colour])
    pg.draw.rect(background, colours[frame_colour], pg.Rect(28, 28, 304, 604))
    pg.draw.rect(background, colours[play_colour], pg.Rect(30, 30, 300, 600))
    pg.draw.rect(background, colours[frame_colour], pg.Rect(350, 60, 160, 180))
    # draws the fixed text
    next_tetronimo_text = display_font.render('Next Piece:', False, (text_colour))
    background.blit(next_tetronimo_text, (350, 30))
    score_text = display_font.render('Score:', False, (text_colour))
    background.blit(score_text, (350, 260))
    # draws the next tetronimo
    next_pattern = next_tet_pattern(next_tet)
    for row_index, row in enumerate(next_pattern):
        for column_index, cell in enumerate(row):
            if cell > 0:
                new_block = draw_block(cell, config)
                row = (row_index + 3) * 30
                column = (column_index + 13) * 30
                background.blit(new_block, (column, row))
    # draws the score
    score_text = score_font.render(f"{score}", False, (255, 255, 255))
    background.blit(score_text, (350, 285))
    return background


def check_rows(dead_table, score, clear_count):
    """checks for scoring rows"""
    new_table = []
    temp_score = 0
    for row in dead_table:
        counter = 0
        for cell in row:
            if cell > 0:
                counter += 1
        if counter == len(row):
            new_table.insert(0, [0 for x in range(len(row))])
            temp_score += 10
            clear_count += 1
        else:
            new_table.append(row)
    score += temp_score * temp_score
    return new_table, score, clear_count


def draw_block(cell, config):
    """draws blocks"""
    colours = get_colours()
    one = config['DEFAULT']['piece_colour_one']
    two = config['DEFAULT']['piece_colour_two']
    three = config['DEFAULT']['piece_colour_three']
    four = config['DEFAULT']['piece_colour_four']
    five = config['DEFAULT']['piece_colour_five']
    six = config['DEFAULT']['piece_colour_six']
    seven = config['DEFAULT']['piece_colour_seven']
    colour_list = [None, one, two, three, four, five, six, seven]
    block = pg.Surface((30, 30))
    pg.draw.rect(block, colours[colour_list[cell]], pg.Rect(0, 0, 30, 30))
    return block


def next_tet_pattern(tetronimo):
    """creates patterns for the 'next piece' display"""
    square_list = []
    for y_index, row in enumerate(tetronimo.pattern):
        for x_index, cell in enumerate(row):
            if cell > 0:
                square_list.append([y_index, x_index])
    ghost_table = [[0 for i in range(4)] for j in range(4)]
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


def get_table(tetronimo, rows, columns):
    """This creates the table from the pattern and location of the piece to be added to the dead_table"""
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
    """performs collision detection one step ahead"""
    if tet.down_size + new_position[0] > len(dead_table):
        return True
    ghost_tetronimo = tetronimo(new_position, tet.type, tet.rotation)
    collision_table = get_table(ghost_tetronimo, rows, columns)
    for y_index, row in enumerate(dead_table):
        for x_index, cell in enumerate(row):
            if cell > 0 and collision_table[y_index][x_index] > 0:
                return True
    return False


def get_height_of_columns(dead_table, rows, columns):
    """gets the height of the columns for the instant drop function"""
    rotated_table = list(zip(*dead_table[::-1]))
    column_heights = {x: 0 for x in range(columns)}
    for column_index, column in enumerate(rotated_table):
        if sum(column) == 0:
            column_heights[column_index] = 0
        else:
            for row_index, cell in enumerate(column):
                if cell > 0:
                    column_heights[column_index] = row_index + 1
    return column_heights


def check_level(clear_count, level, speed):
    """this sets the current level and speed"""
    if clear_count == 10:
        clear_count = 0
        level += 1
        speed -= 1
    return clear_count, level, speed








