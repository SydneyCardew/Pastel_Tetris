import pygame as pg
import configparser
import functions as f
from classes import tetronimo


def main():
    pg.init()
    pg.font.init()
    myfont = pg.font.SysFont('Courier', 30)
    config = configparser.ConfigParser()
    config.read('Resources/Settings/config.ini')
    screen_width = 520
    screen_height = 660
    surface = pg.Surface((screen_width, screen_height))
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE | pg.SCALED)
    background = f.draw_background(screen_width, screen_height, config)
    rows = int(config['DEFAULT']['rows'])
    columns = int(config['DEFAULT']['columns'])
    dead_table = f.generate_blank_table(rows, columns)
    clock = pg.time.Clock()
    running = True
    tetronimo_on = False
    while running:
        if not tetronimo_on:
            main_tet = tetronimo([5, 0], 'j', 0)
        current_position = main_tet.position
        surface.blit(background, (0, 0))
        #
        display_table = f.add_tables(dead_table, f.get_table(main_tet, rows, columns))
        for row_index, row in enumerate(display_table):
            for column_index, cell in enumerate(row):
                if cell > 0:
                    new_block = f.draw_block(cell, config)
                    row = (row_index + 1) * 30
                    column = (column_index + 1) * 30
                    surface.blit(new_block, (row, column))
        text_surface = myfont.render(f"{current_position}", False, (255, 255, 255))
        surface.blit(text_surface, (0, 0))
        screen_width, screen_height = pg.display.get_surface().get_size()
        transformed_surface = pg.transform.scale(surface, (screen_width, screen_height))
        screen.blit(transformed_surface, (0, 0))
        pg.display.flip()
        # the movement logic
        next_position = current_position.copy()
        next_position[1] += 1
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            next_position[1] += 1
        if keys[pg.K_LEFT]:
            if next_position[0] > 1:
                next_position[0] -= 1
        if keys[pg.K_RIGHT]:
            if next_position[0] + main_tet.right_size < columns + 1:
                next_position[0] += 1
        # events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
        # collision detection and row removal
        collision = f.collision_detector(next_position, dead_table, main_tet, rows, columns)
        if collision:
            tetronimo_on = False
            dead_table = f.add_tables(dead_table, f.get_table(main_tet, rows, columns))
        else:
            main_tet.update(next_position)

        clock.tick(30)


if __name__ == "__main__":
    main()