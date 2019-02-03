from strategy import BeeStrategy
import random

class Rester(BeeStrategy):
    '''
    This type of bee stays at the hive, until a location for food is known and then he becomes a foraging bee
    '''

    def step(self):
        bee = self.bee

        # Resting bees can only be at the hive.
        assert bee.pos == bee.hive_loc

        hive = bee.model.get_hive(bee.hive_id)

        # check if bee has enough energy for foraging
        if bee.energy >= bee.max_energy:

            # check if food locations are known
            if hive.food_locs:

                # become forager at random food location
                bee.type_bee = "foraging"
                bee.food_loc = random.choice(hive.food_locs)

            # otherwise, stay at hive and gain energy
            else:
                # become scout if no food has been found
                bee.type_bee = "scout"

        else:
            bee.relax_at_hive(hive)