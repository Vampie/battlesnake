from snake import SnakeBrain

# Pelle is very hungry all the time
class Pelle(SnakeBrain):
  
  def hungry(self):
    return True

  def get_value(self, direction):
    val = super().get_value(direction)
    neighbour = self.board.neighbour(self.my_head(), direction)  
    # pelle is smart, she also checks if neighbour cell *might* be occupied next round
    if neighbour is not None:
      if neighbour.can_be_occupied_in_next_round:
        val = val - 100
      if neighbour.is_food:
        val = val + 100
    return val

  def value_for_cell(self, cell):
        if cell.is_snake():
            return -5
        elif cell.is_food():
                return 15
        else:
                return 1
        