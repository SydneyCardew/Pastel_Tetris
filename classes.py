import functions as f


class tetronimo:
    """the basic tetronimo object"""
    def __init__(self, origin, type, rotation):
        pieces = f.get_pieces()
        values = f.get_values()
        self.type = type
        self.value = values[self.type]
        self.position = origin
        self.rotation = rotation
        self.absolute_pattern = pieces[self.type]
        self.pattern = self.rotated_pattern()
        self.get_sizes()

    def update(self, new_position):
        self.position = new_position

    def rotate(self):
        self.rotation += 1
        if self.rotation >= 4:
            self.rotation = 0
        self.pattern = self.rotated_pattern()
        self.get_sizes()

    def rotated_pattern(self):
        pattern = self.absolute_pattern
        for x in range(self.rotation):
            list(zip(*pattern[::-1]))
        return pattern

    def get_sizes(self):
        self.right_size = len(self.pattern[0])
        self.down_size = len(self.pattern)

