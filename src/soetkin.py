from snake import SnakeBrain

class Soetkin(SnakeBrain):
  
  def hungry(self):
    return self.health < 50

  def get_value(self, direction):
    val = self.board.number_of_free_cells(self.head(), direction)
    neighbour = self.board.neighbour(self.head(), direction)
    
    # soetkin is smart, she also checks if neighbour cell *might* be occupied next round
    if neighbour is not None:
      if neighbour.can_be_occupied_in_next_round:
        val = val - 20

    if self.hungry():
      d = self.board.distance_to_food(self.head(), direction)
      val = val + (20 - d)
    return val