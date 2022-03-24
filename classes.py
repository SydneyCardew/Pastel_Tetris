
class tetronimo:
    """the basic tetronimo object"""
    def __init__(self, origin, type, rotation):
        self.type = type
        self.position = origin
        self.rotation = rotation

    def move(self, direction, fixed_table):
        x = self.position[0]
        y = self.position[1]
        current_position = self.position
        if direction == 'down':
            new_position = [x, y + 1]
        elif direction == 'left':
            new_position = [x - 1, y]
        elif direction == 'right':
            new_position = [x + 1, y]
        if fixed_table[new_position[0]][new_position[1]] or y > 20:
            fixed_table = self.kill_tetronimo([x, y], fixed_table)
            new_position = None
        return (fixed_table, new_position)

    def update(self, new_position):
        self.position = new_position

    def kill_tetronimo(self, position, fixed_table):
        fixed_table[position[0]][position[1]][0] = True
        fixed_table[position[0]][position[1]][1] = self.type
        return fixed_table
