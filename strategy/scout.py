from strategy import BeeStrategy

import random
from food import Food

class Scout(BeeStrategy):
    '''
    This type of bee does a random walk, searching for food, and return to hive if he has found this.
    '''

    def step(self):
        """
        No food found yet, do random walk
        """
        bee = self.bee

        if bee.loaded is False:
            if bee.energy < 0.5 * bee.max_energy and bee.pos != bee.hive_loc:
                bee.move(bee.hive_loc)

                # check if destination is reached
                if bee.pos == bee.hive_loc:
                    hive = bee.model.get_hive(bee.hive_id)
                    assert hive
                    bee.arrive_at_hive(hive)
            else:
                food_neighbours = [
                    nb
                    for nb in bee.model.grid.get_neighbors_by_breed(Food, bee.pos, moore=True, include_center=False, radius=1)
                    if nb.can_be_eaten()
                ]

                # If you see food that is uneaten, move there.
                if food_neighbours:
                    food = random.choice(food_neighbours)

                    bee.model.grid.move_agent(bee, food.pos)
                    food.get_eaten()

                    # Become a forager take food and remember location
                    bee.type_bee = 'foraging'
                    bee.loaded = True
                    bee.food_loc = bee.pos

                # otherwise, move randomly
                else:
                    self.random_move()

        else:
            raise Exception("Scouts should be unloaded.")

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        bee = self.bee

        # get neighboorhood
        neighbourhood = bee.get_accessible_neighbourhood()

        # select random cell in neighbourhood
        target = random.choice(neighbourhood)

        # move to cell
        bee.model.grid.move_agent(bee, target)
