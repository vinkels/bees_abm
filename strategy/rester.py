import random


def rester_step(bee):
    '''
    This type of bee stays at the hive, until a location for food is known and then he becomes a foraging bee
    '''
    # Resting bees can only be at the hive.
    assert bee.pos == bee.hive_location

    hive = bee.model.get_hive(bee.hive_id)

    # check if bee has enough energy for foraging
    if bee.energy >= bee.max_energy:

        # check if food locations are known
        if hive.food_locations:

            # become forager at random food location
            bee.type_bee = "foraging"
            bee.food_location = random.choice(hive.food_locations)

        # otherwise, stay at hive and gain energy
        else:
            # become scout if no food has been found
            bee.type_bee = "scout"

    else:
        if hive.food >= hive.bite:
            bee.energy += hive.bite
            hive.food -= hive.bite
        else:
            bee.type_bee = "scout"