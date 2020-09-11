from enum import Enum
from debug import Debug


class Board(object):
  
    def __init__(self, data):
        self.snakes = []
        self.data = data
        self.init_board()

    def __str__(self):
        return 'Bord'

    def init_board(self):
        n = self.data['board']['height']
        m = self.data['board']['width']
        self.board_width = m
        self.board_height = n
        self.board = [[Cell(i, j) for i in range(m)] for j in range(n)]
        self.set_foods()
        self.set_snakes()


    def set_foods(self):
        foods = self.data['board']['food']
        for f in foods:
            x = f['x']
            y = f['y']
            food = Food(x, y)
            self.board[x][y] = food

    def set_snakes(self):
        snake_datas = self.data['board']['snakes']

        for snake_data in snake_datas:
            snake = self.parse_snake(snake_data)
            self.snakes.append(snake)
            self.update_board_with_snake(snake)

        for snake in self.snakes:
            for c in self.potential_next_moves(snake):
                (self.board[c.x][c.y]).can_be_occupied_in_next_round = True

    def parse_snake(self, snake_data):
        snake = Snake()
        for b in (snake_data['body'])[:-1]:
            snake.add_snakePart(SnakePart(b['x'], b['y']))
        tail = SnakeTail(snake_data['body'][-1]['x'],
                         snake_data['body'][-1]['y'])
        snake.add_snakePart(tail)
        return snake

    def update_board_with_snake(self, snake):
        for p in snake.snakeParts:
            self.board[p.x][p.y] = p

    def potential_next_moves(self, snake):
        head = snake.snakeParts[0]
        Debug.log_with_action(head.position_string(), 'Head + potential moves')
        potential_cells = []
        c = self.neighbour_left(head)
        if c is not None:
            potential_cells.append(PotentialSnakePart(c.x, c.y))
        c = self.neighbour_right(head)
        if c is not None:
            potential_cells.append(PotentialSnakePart(c.x, c.y))
        c = self.neighbour_up(head)
        if c is not None:
            potential_cells.append(PotentialSnakePart(c.x, c.y))
        c = self.neighbour_down(head)
        if c is not None:
            potential_cells.append(PotentialSnakePart(c.x, c.y))
        for i in potential_cells:
          Debug.log(i.position_string())
        return potential_cells

    def neighbour (self, cell, direction):
      if direction == Direction.up:
        return self.neighbour_up(cell)
      elif direction == Direction.right:
        return self.neighbour_right(cell)
      elif direction == Direction.down:
        return self.neighbour_down(cell)
      elif direction == Direction.left:
        return self.neighbour_left(cell)

    def neighbours(self, cell):
        Debug.log_with_action(cell.position_string(), 'Cell + neighbours')
        neighbours = []
        c = self.neighbour_left(cell)
        if c is not None:
          neighbours.append(c)
        c = self.neighbour_right(cell)
        if c is not None:
          neighbours.append(c)
        c = self.neighbour_up(cell)
        if c is not None:
          neighbours.append(c)
        c = self.neighbour_down(cell)
        if c is not None:
          neighbours.append(c)
        for i in neighbours:
          Debug.log(i.position_string())
        return neighbours


    def neighbour_right(self, cell):
        if cell.x == self.board_width -1:
            return None
        else:
            return self.cell_at(cell.x + 1, cell.y)

    def neighbour_left(self, cell):
        if cell.x == 0:
            return None
        else:
            return self.cell_at(cell.x - 1, cell.y)

    def neighbour_up(self, cell):
        if cell.y == self.board_height -1:
            return None
        else:
            return self.cell_at(cell.x, cell.y + 1)

    def neighbour_down(self, cell):
        if cell.y == 0:
            return None
        else:
            return self.cell_at(cell.x, cell.y - 1)

    def cells_in_direction(self, cell, direction):
        if direction == Direction.up:
            return self.cells_in_direction_up(cell)
        elif direction == Direction.right:
            return self.cells_in_direction_right(cell)
        elif direction == Direction.down:
            return self.cells_in_direction_down(cell)
        elif direction == Direction.left:
            return self.cells_in_direction_left(cell)

    def cells_in_direction_left(self, cell):
        cells = []
        for i in reversed(range(0, cell.x)):
            cells.append(self.cell_at(i, cell.y))
        return cells

    def cells_in_direction_right(self, cell):
        cells = []
        for i in range(cell.x + 1, self.board_width):
            cells.append(self.cell_at(i, cell.y))
        return cells

    def cells_in_direction_up(self, cell):
        cells = []
        for i in range(cell.y + 1, self.board_height):
            cells.append(self.cell_at(cell.x, i))
        return cells

    def cells_in_direction_down(self, cell):
        cells = []
        for i in reversed(range(0, cell.y)):
            cells.append(self.cell_at(cell.x, i))
        return cells

    def number_of_free_cells(self, cell, direction):
        cells = self.cells_in_direction(cell, direction)
        count = 0
        for c in cells:
            if not c.is_free():
                return count
            else:
                count = count + 1
        return count

    def is_food_in_direction(self, cell, direction):
        cells = self.cells_in_direction(cell, direction)
        for c in cells:
            if c.is_food():
                return True
            elif c.is_snake():
                return False
        return False

    def distance_to_food(self, cell, direction):
        cells = self.cells_in_direction(cell, direction)
        count = 0
        for c in cells:
            if c.is_free():
                if c.is_food():
                    return count + 1
                else:
                    count = count + 1
            elif c.is_snake():
                return count
        return count

    def cell_at(self, x, y):
        return self.board[x][y]

    def is_blocked(self, cell, direction):
        if self.number_of_free_cells(cell, direction) == 0:
          return True
          
        if direction == Direction.up:
            return self.is_blocked_up(cell)
        elif direction == Direction.right:
            return self.is_blocked_right(cell)
        elif direction == Direction.down:
            return self.is_blocked_down(cell)
        elif direction == Direction.left:
            return self.is_blocked_left(cell)

    def is_blocked_left(self, cell):
        if cell.x == 0:
            return True
        else:
            return self.cell_at(cell.x - 1, cell.y).is_snake()

    def is_blocked_right(self, cell):
        if cell.x == self.board_width - 1:
            return True
        else:
            return self.cell_at(cell.x + 1, cell.y).is_snake()

    def is_blocked_up(self, cell):
        if cell.y == self.board_height - 1:
            return True
        else:
            return self.cell_at(cell.x, cell.y + 1).is_snake()

    def is_blocked_down(self, cell):
        if cell.y == 0:
            return True
        else:
            return self.cell_at(cell.x, cell.y - 1).is_snake()

    def print_board(self):
        str = ""
        for y in reversed(range(0, self.board_height)):
            for x in range(0, self.board_width):
                str = str + self.cell_at(x, y).shortString() + " "
            str = str + "\n"
        print(str)


class Snake():
    def __init__(self):
        self.snakeParts = []

    def add_snakePart(self, sp):
        self.snakeParts.append(sp)


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_be_occupied_in_next_round = False

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def is_food(self):
        return False

    def is_snake(self):
        return False

    def is_free(self):
        return True

    def shortString(self):
        return ' '

    def position_string(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class PotentialSnakePart(Cell):

    def is_free(self):
        return False

    def shortString(self):
        return '?'


class Food(Cell):
    def is_food(self):
        return True

    def shortString(self):
        return '*'


class SnakePart(Cell):
    def is_snake(self):
        return True

    def is_free(self):
        return False

    def shortString(self):
        return '^'


class SnakeTail(SnakePart):
    def is_snake(self):
        return True

    # tail is free in next move
    def is_free(self):
        return True


class Direction(Enum):
    up = 'up'
    right = 'right'
    down = 'down'
    left = 'left'
