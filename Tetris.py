import pygame as pg
import configparser
import functions as f
from classes import tetronimo


def main():
    pg.init()
    config = configparser.ConfigParser()
    config.read('Resources/Settings/config.ini')
    screen_width = 520
    screen_height = 660
    surface = pg.Surface((screen_width, screen_height))
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE | pg.SCALED)
    background = f.draw_background(screen_width, screen_height, config)
    rows = int(config['DEFAULT']['rows'])
    columns = int(config['DEFAULT']['columns'])
    block_table = f.generate_blank_table(rows, columns)
    fixed_table = f.generate_blank_table(rows, columns)
    clock = pg.time.Clock()
    running = True
    tetronimo_on = False
    while running:
        if not tetronimo_on:
            main_tet = tetronimo([5, 0], 'j', 0)
        surface.blit(background, (0, 0))
        for row_index, row in enumerate(fixed_table):
            for column_index, cell in enumerate(row):
                if cell[0]:
                    new_block = f.draw_block(cell[1], config)
                    row = (row_index + 1) * 30
                    column = (column_index + 1) * 30
                    surface.blit(new_block, (row, column))
        screen_width, screen_height = pg.display.get_surface().get_size()
        transformed_surface = pg.transform.scale(surface, (screen_width, screen_height))
        screen.blit(transformed_surface, (0, 0))
        pg.display.flip()
        fixed_table, new_position = main_tet.move('down', fixed_table)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    fixed_table, new_position = main_tet.move('down', fixed_table)
                if event.key == pg.K_LEFT:
                    fixed_table, new_position = main_tet.move('left', fixed_table)
                if event.key == pg.K_RIGHT:
                    fixed_table, new_position = main_tet.move('right', fixed_table)
        if new_position:
            main_tet.update(new_position)
        else:
            tetronimo_on = False
        clock.tick(60)


if __name__ == "__main__":
    main()