from board import Direction

class SnakeBrain(object):

    possible_moves = ["up", "right", "down", "left"]
    possible_directions = [Direction.up,
                           Direction.right, Direction.down, Direction.left]

    def __init__(self, move):
        self.moves = [move]
        self.snake_x = 0
        self.snake_y = 0
        self.health = 0
        self.heading = Direction.up

    def updateStatus(self, dataJson):
        self.data = dataJson
        self.snake_x = self.data['you']['head']['x']
        self.snake_y = self.data['you']['head']['y']
        self.health = self.data['you']['health']
        self.heading = self.calculate_heading()

    def calculate_heading(self):
        x2 = self.data['you']['body'][1]['x']
        y2 = self.data['you']['body'][1]['y']
        if x2 < self.snake_x:
            return Direction.left
        elif x2 > self.snake_x:
            return Direction.right
        elif y2 < self.snake_y:
            return Direction.up
        else:
            return Direction.down

    def move(self, board):
        move = self.calculate_next_move(board)
        self.moves.append(move)
        return move

    def last_move(self):
        return self.moves[-1]

    def move_towards(self, direction):
        return direction.value

    def calculate_next_move(self, board):
        directions = {}
        for dir in self.possible_directions:
            directions[dir] = self.get_value(board, dir)
        print(directions)
        new_dir = max(directions, key=directions.get)
        return self.move_towards(new_dir)

    def calculate_next_move_random(self, board):
        self.free_directions(board)
        last_move_index = self.possible_moves.index(self.last_move())
        new_index = (last_move_index + 1) % 4
        new_move = self.possible_moves[new_index]
        return new_move

# this method gives a score to a cell
    def value_for_cell(self, cell, board):
        if cell.is_snake():
            return -10
        elif cell.is_food():
            if self.hungry:
                return 4
            else:
                return 1
        else:
            return 4 - board.count_neigbour_snakes(cell)

    def hungry(self):
        return self.health < 40

    def get_value(self, board, direction):
        if direction == Direction.up:
            return self.value_up(board)
        elif direction == Direction.right:
            return self.value_right(board)
        elif direction == Direction.down:
            return self.value_down(board)
        elif direction == Direction.left:
            return self.value_left(board)

    def value_up(self, board):
        if self.up_is_blocked(board):
            return -1000
        count = 0
        for y in range(self.snake_y + 1, board.board_height):
            cell = board.cellAt(self.snake_x, y)
            if cell.is_snake():
                return count
            count = count + self.value_for_cell(cell, board)
        return count

    def value_down(self, board):
        if self.down_is_blocked(board):
            return -1000
        count = 0
        for y in reversed(range(self.snake_y)):
            cell = board.cellAt(self.snake_x, y)
            if cell.is_snake():
                return count
            count = count + self.value_for_cell(cell, board)
        return count

    def value_right(self, board):
        if self.right_is_blocked(board):
            return -1000
        count = 0
        for x in range(self.snake_x + 1, board.board_width):
            cell = board.cellAt(x, self.snake_y)
            if cell.is_snake():
                return count
            count = count + self.value_for_cell(cell, board)
        return count

    def value_left(self, board):
        if self.left_is_blocked(board):
            return -1000
        count = 0
        for x in reversed(range(self.snake_x)):
            cell = board.cellAt(x, self.snake_y)
            if cell.is_snake():
                return count
            count = count + self.value_for_cell(cell, board)
        return count

    def my_head(self, board, direction):
        return board.cell_at(self.snake_x, self.snake_y)

    def is_blocked(self, board, direction):
        return board.is_blocked(self.my_head(board), direction)
