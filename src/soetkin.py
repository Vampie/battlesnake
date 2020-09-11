from snake import SnakeBrain

class Soetkin(SnakeBrain):
  
  def hungry(self):
    return self.health < 25

  def calculate_next_move(self):
      # for each direction calculate
      directions = {}
      for dir in self.possible_directions:
        directions[dir] = self.get_value(dir)
     
      new_dir = max(directions, key=directions.get)  
      return self.move_towards(new_dir)

  def get_value(self, direction):
    if self.is_blocked(board, direction):
      return -1000
    head = self.board.cell_at(self.snake_x, self.snake_y)
    val = self.board.number_of_free_cells(head, direction)
    if (self.board.cells_in_direction(head, direction).can_be_occupied_in_next_round):
      val = val - 20
    # print("## get value ##")
    # print(str(self.snake_x) + ", " + str(self.snake_y))
    # print(str(head.x) + ", " + str(head.y))
    
    if self.hungry():
      d = self.board.distance_to_food(head, direction)
      val = val + (20 - d)
    return val