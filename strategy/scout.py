import random
from food import Food


def scout_step(bee):
    """
    This type of bee does a random walk, searching for food, and return to hive if he has found this.
    """
    if bee.loaded is False:
        if bee.energy < 0.5 * bee.max_energy and bee.pos != bee.hive_location:
            bee.move(bee.hive_location)

            # check if destination is reached
            if bee.pos == bee.hive_location:
                hive = bee.model.get_hive(bee.hive_id)
                assert hive
                bee.arrive_at_hive(hive)
        else:
            food_neighbours = [
                nb
                for nb in bee.model.grid.get_food_neighbors(bee.pos, 1)
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
                bee.food_location = bee.pos

            # otherwise, move to a random neighbour
            else:
                neighbourhood = bee.get_accessible_neighbourhood()
                bee.model.grid.move_agent(bee, random.choice(neighbourhood))

    else:
        raise Exception("Scouts should be unloaded.")
