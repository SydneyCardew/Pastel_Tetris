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
        """moves the tetronimo"""
        self.position = new_position

    def rotate(self):
        """performs the rotation action"""
        self.rotation += 1
        if self.rotation >= 4:
            self.rotation = 0
        self.pattern = self.rotated_pattern()
        self.get_sizes()

    def rotated_pattern(self):
        """rotates the pattern"""
        pattern = self.absolute_pattern
        for x in range(self.rotation):
            pattern = list(zip(*pattern[::-1]))  # this line performs the matrix translation
        return pattern

    def get_sizes(self):
        """works out the bounds"""
        self.right_size = len(self.pattern[0])
        self.down_size = len(self.pattern)

    def __str__(self):
        return self.id_string()

    def __repr__(self):
        return self.id_string()

    def id_string(self):
        """returns a string representation to the terminal (debugging tool)"""
        return f"rotation:{self.rotation} | position:{self.position} | type:{self.type}\n" \
               f"pattern: {self.pattern}"