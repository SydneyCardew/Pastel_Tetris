import pygame as pg
import json


def get_colours():
    """retrieves a python dict containing RGB tuples for the colours from the json file"""
    with open('Resources/Settings/colours.json', 'r+') as colour_json:
        colours = json.load(colour_json)
    return colours


def generate_blank_table(rows, columns):
    return [[[False, None] for x in range(rows)] for x in range(columns)]


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


def draw_block(colour, config):
    colours = get_colours()
    j_colour = config['DEFAULT']['background']
    block = pg.Surface((30, 30))
    block.fill(colours[j_colour])
    return block







