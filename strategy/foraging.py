from food import Food


def foraging_step(bee):
    """
    This type of bee goes to a given food location and takes the food.
    If the bee is loaded it returns to the hive.
    """
    if bee.is_carrying_food:
        bee.move_to_hive()
    else:
        bee.move(bee.food_location)

        # Check if arrived, then take food.
        if bee.food_location == bee.pos:
            bee.planned_route = []

            food_on_location = [
                food
                for food in bee.model.grid.get_food_neighbors(bee.pos, 0)
                if food.can_be_harvested
            ]

            if not food_on_location:
                # No food was found, so next step bee will scout.
                bee.type_bee = "scout"
            else:
                food_on_location[0].harvest()
                bee.is_carrying_food = True
