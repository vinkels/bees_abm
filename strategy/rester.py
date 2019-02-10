import random


def rester_step(bee):
    """
    This type of bee stays at the hive until it has regained its energy.
    """
    assert bee.at_hive, "Resting bees can only be at the hive."

    hive = bee.hive

    if bee.energy < bee.max_energy:
        if hive.food >= hive.bite:
            bee.energy += hive.bite
            hive.food -= hive.bite
        else:
            # Become a scout if the hive is empty
            bee.type_bee = "scout"

    else:
        if hive.food_locations:
            # if food locations are known, forage to a random food source.
            bee.food_location = random.choice(hive.food_locations)
            bee.type_bee = "foraging"

        else:
            # become scout if no food has been found before.
            bee.type_bee = "scout"
