from strategy import BeeStrategy
from config import BABYTIME

class Babee(BeeStrategy):
    '''
    This type of bee stays at the hive until a certain age
    '''

    def step(self):
        bee = self.bee

        hive = bee.model.get_hive(bee.hive_id)

        # gain strength until old enough
        bee.relax_at_hive(hive)

        # age is arbitrary
        # print("Bee age: ", bee.age, "BABYTIME: ", BABYTIME)
        if bee.age > BABYTIME:
            # raise Exception("Binnen")
            bee.type_bee = "rester"
