from config import BABYTIME, BABYBITE


def babee_step(bee):
    """
    This type of bee stays at the hive until a certain age (BABYTIME).
    If the hive can be eaten from by the baby, take a bite for energy.
    """
    hive = bee.hive

    if hive.food >= BABYBITE:
        bee.energy += BABYBITE
        hive.food -= BABYBITE

    if bee.age > BABYTIME:
        bee.type_bee = "rester"
