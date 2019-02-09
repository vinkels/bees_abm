from food import Food


def foraging_step(bee):
    '''
    This type of bee goes to a given food location, takes the food and return to the hive
    '''
    # if not yet arrived at food location
    if bee.loaded is False:
        bee.move(bee.food_location)

        # check if arrived, then take food
        if bee.food_location == bee.pos:
            food_neighbors = [
                nb
                for nb in bee.model.grid.get_food_neighbors(bee.pos, 0)
                if nb.can_be_harvested()
            ]

            bee.planned_route = []
            if food_neighbors:
                food = food_neighbors[0]
                food.harvest()
                bee.loaded = True

            # if there was no food at the promised location become a scout
            else:
                bee.type_bee = "scout"

    # if loaded, return to hive
    else:
        bee.move(bee.hive_location)

        # check if destination is reached
        if bee.pos == bee.hive_location:
            hive = bee.model.get_hive(bee.hive_id)
            assert hive
            bee.arrive_at_hive(hive)