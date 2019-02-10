import random
from food import Food


def scout_step(bee):
    """
    This type of bee does a random walk, searching for food,
    and returns to its hive if he has found food or is tired.
    """
    assert not bee.is_carrying_food, "Scouts should be unloaded."

    if bee.is_tired and not bee.at_hive:
        bee.move_to_hive()
    else:
        food_in_neighbourhood = [
            nb
            for nb in bee.model.grid.get_food_neighbors(bee.pos, 1)
            if nb.can_be_harvested
        ]

        # If you see food that is uneaten, move there.
        if food_in_neighbourhood:
            food = random.choice(food_in_neighbourhood)

            bee.model.grid.move_agent(bee, food.pos)
            food.harvest()

            # Become a forager take food and remember location
            bee.type_bee = 'foraging'
            bee.is_carrying_food = True
            bee.food_location = bee.pos

        # otherwise, move to a random neighbour
        else:
            neighbourhood = bee.get_accessible_neighbourhood()
            bee.model.grid.move_agent(bee, random.choice(neighbourhood))

