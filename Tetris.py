import pygame as pg
import configparser
import functions as f


def main():
    # initialisations
    pg.init()
    config = configparser.ConfigParser()
    config.read('Resources/Settings/config.ini')
    screen_width = 520
    screen_height = 660
    surface = pg.Surface((screen_width, screen_height))
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE | pg.SCALED)
    rows = int(config['DEFAULT']['rows'])
    columns = int(config['DEFAULT']['columns'])
    dead_table = f.generate_blank_table(rows, columns)
    clock = pg.time.Clock()
    running = True
    tetronimo_on = True
    paused = False
    timer = 0
    speed = 40
    score = 0
    level = 0
    clear_count = 0
    game_over = False
    main_tet = f.random_tetronimo()
    next_tetronimo = f.random_tetronimo(main_tet)

    # main game loop
    while running:
        if paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        paused = not paused
        else:
            background = f.draw_background(screen_width, screen_height, config, next_tetronimo, score, level)
            if not tetronimo_on:
                main_tet = next_tetronimo
                next_tetronimo = f.random_tetronimo()
                tetronimo_on = True
            current_position = main_tet.position
            surface.blit(background, (0, 0))

            # draws the blocks
            display_table = f.add_tables(dead_table, f.get_table(main_tet, rows, columns))
            for row_index, row in enumerate(display_table):
                for column_index, cell in enumerate(row):
                    if cell > 0:
                        try:
                            new_block = f.draw_block(cell, config)
                            row = (row_index + 1) * 30
                            column = (column_index + 1) * 30
                            surface.blit(new_block, (column, row))
                        except IndexError:
                            column_heights = f.get_height_of_columns(dead_table, rows, columns)
                            if max(column_heights) > rows:
                                game_over = True
                            else:
                                pass
            screen_width, screen_height = pg.display.get_surface().get_size()
            transformed_surface = pg.transform.scale(surface, (screen_width, screen_height))
            screen.blit(transformed_surface, (0, 0))
            pg.display.flip()

            # the movement logic and game controls
            next_position = current_position.copy()
            if timer == speed:
                next_position[0] += 1
                timer = 0
            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN]:
                next_position[0] += 1
            if timer % 2 == 0:
                if keys[pg.K_LEFT]:
                    if next_position[1] > 0:
                        collision = f.collision_detector((next_position[0], next_position[1] - 1),
                                                         dead_table, main_tet, rows, columns)
                        if not collision:
                            next_position[1] -= 1
                if keys[pg.K_RIGHT]:
                    if next_position[1] + main_tet.right_size < columns:
                        collision = f.collision_detector((next_position[0], next_position[1] + 1),
                                                         dead_table, main_tet, rows, columns)
                        if not collision:
                            next_position[1] += 1

            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.VIDEORESIZE:
                    screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        main_tet.rotate()
                        if current_position[1] + main_tet.right_size > columns:
                            next_position[1] += (columns - (current_position[1] + main_tet.right_size))
                    if event.key == pg.K_p:
                        paused = not paused
                    if event.key == pg.K_SPACE:
                        # this logic controls the 'super drop' function
                        column_heights = f.get_height_of_columns(dead_table, rows, columns)
                        occupied_columns = [column_heights[x] for x in range(main_tet.position[1], main_tet.position[1]
                                            + main_tet.right_size)]
                        next_position[0] += (len(dead_table) - main_tet.down_size - main_tet.position[0]
                                             - max(occupied_columns))
                        # these lines handle cases where the tetronimo needs to 'slot in'
                        further_position = next_position[0] + 1, next_position[1]
                        collision = f.collision_detector(further_position, dead_table, main_tet, rows, columns)
                        if collision:
                            pass
                        else:
                            next_position[0] += 1

            # collision detection and row removal
            if next_position[0] >= current_position[0]:
                collision = f.collision_detector(next_position, dead_table, main_tet, rows, columns)
            else:
                collision = False
            if collision:
                tetronimo_on = False
                dead_table = f.add_tables(dead_table, f.get_table(main_tet, rows, columns))
            else:
                main_tet.update(next_position)
            dead_table, score, clear_count = f.check_rows(dead_table, score, clear_count)
            clear_count, level, speed = f.check_level(clear_count, level, speed)
            clock.tick(speed)
            timer += 1

            if game_over:
                print("Game over! Thank you for playing")
                running = not running


if __name__ == "__main__":
    main()
