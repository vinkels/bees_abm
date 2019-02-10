from mesa import Model
from mesa.datacollection import DataCollector

import random as rd

from config import GRID_HEIGHT, GRID_WIDTH, FOOD_OBSTACLE_RATIO, BABYTIME
from food import Food
from bee import Bee
from hive import Hive
from obstacle_grid import MultiGridWithObstacles

from schedule import RandomActivationBeeWorld


class BeeForagingModel(Model):
    def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT, obstacle_density=15, food_density=15, nr_hives=3, VIZUALISATION=False):
        super().__init__()
        self.height = height
        self.width = width
        self.nr_hives = nr_hives
        self.death_count = 0
        self.birth_count = 0
        self.death_age = []
        self.obstacle_density = obstacle_density
        self.food_density = food_density
        self.nr_hives = nr_hives
        self.load_count = 0

        self.user_error = None
        if self.obstacle_density + self.food_density > FOOD_OBSTACLE_RATIO:
            raise Exception("Food and obstacles do not fit in the grid.")

        hive_locations, food_locations, self.obstacle_locations = self.init_grid(height,
                                                                                 width,
                                                                                 self.obstacle_density,
                                                                                 self.food_density,
                                                                                 self.nr_hives)

        self.grid = MultiGridWithObstacles(self.width,
                                           self.height,
                                           torus=False,
                                           obstacle_positions=set(self.obstacle_locations),
                                           VIZUALISATION=VIZUALISATION)

        self.schedule = RandomActivationBeeWorld(self)

        self.hives = {}

        for hive_location in hive_locations:

            # Init Hives
            r = lambda: rd.randint(0, 255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            hive = Hive(self, hive_location, color=color, bee_color=color)

            self.hives[hive.unique_id] = hive
            self.add_agent(hive, hive_location)

            # Init Bees
            # TODO TAG BEES FOR WARM-UP PERIOD
            # TODO DEFINE THE AMOUNT OF STARTING BEES BABIES AS WELL
            for _ in range(0, 20):
                self.add_bee(hive=hive,
                             type_bee="scout",
                             color=hive.bee_color,
                             age=BABYTIME)

                self.add_bee(hive=hive,
                             type_bee="rester",
                             color=hive.bee_color,
                             age=BABYTIME)

        # TODO ADD MORE ROBUST RANDOMNESS TO FOOD UTILITY
        # DONE?
        for f_loc in food_locations:
            food = Food(self, f_loc)
            self.add_agent(food, f_loc)

        self.datacollector = DataCollector({
            "n_bees": lambda m: m.schedule.get_breed_count(Bee),
            "hive_food": lambda m: sum([h.get_food_stat() for h in m.hives.values()]),
            "scout_bees": lambda m: m.schedule.get_bee_count("scout"),
            "forage_bees": lambda m: m.schedule.get_bee_count("foraging"),
            "rest_bees": lambda m: m.schedule.get_bee_count("rester"),
            "baby_bees": lambda m: m.schedule.get_bee_count("babee"),
            "death_age": lambda m: m.get_death_age(),
            "n_births": lambda m: m.get_birth_count(),
            "n_deaths": lambda m: m.get_death_count(),
            "load_count": lambda m: m.load_count
        })

        self.running = True

        self.datacollector.collect(self)
        self.grid.warmup()

    def get_hive(self, hive_id):
        """
        Get the Hive belonging to hive_id.
        """
        return self.hives[hive_id]

    def step(self):
        """
        Steps the schedule and collect data.
        """
        self.schedule.step()
        self.datacollector.collect(self)

    def get_birth_count(self):
        """
        Returns the current birth count en resets it to 0.
        """
        count = self.birth_count
        self.birth_count = 0
        return count

    def get_death_count(self):
        """
        Returns the current death count en resets it to 0.
        """
        count = self.death_count
        self.death_count = 0
        return count

    def get_death_age(self):
        """
        Returns the current mean death age count en resets it to 0.
        """
        if len(self.death_age) > 0:
            mean_age = sum(self.death_age)/len(self.death_age)
            self.death_age = []
            return mean_age
        else:
            return 0

    def run_model(self, number_of_steps):
        """
        Runs the model for a certain number_of_steps.
        """
        for i in range(number_of_steps):
            self.step()

    def add_agent(self, agent, pos):
        """
        Add an agent to the grid and schedule.
        """
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

    def remove_agent(self, agent):
        """
        Remove an agent from the grid and schedule.
        """
        if type(agent) == Bee:
            self.death_count += 1
            self.death_age.append(agent.age)

        self.grid.remove_agent(agent)
        self.schedule.remove(agent)

    def add_bee(self, hive, type_bee, color, age=0):
        """
        Add a bee to the model.
        """
        bee = Bee(self, pos=hive.pos, hive=hive, type_bee=type_bee, hive_id=hive.unique_id, color=color, age=age)

        if type_bee == 'babee':
            self.birth_count += 1

        self.add_agent(bee, hive.pos)

    @staticmethod
    def init_grid(height, width, obstacle_density, food_density, nr_hives):
        """
        Set the initial locations for the hives, food and obstacles.
        """
        possible_locations = [
            (x, y)
            for y in range(height)
            for x in range(width)
        ]
        amount_of_possible_locations = len(possible_locations)

        amount_food = int((amount_of_possible_locations / 100) * food_density)
        amount_obstacle = int((amount_of_possible_locations / 100) * obstacle_density)

        rd.shuffle(possible_locations)

        food_end_index = amount_food + 1
        obstacle_end_index = food_end_index + amount_obstacle

        hive_locations = possible_locations[0:nr_hives]

        food_locations = possible_locations[nr_hives:food_end_index]
        obstacle_locations = set(possible_locations[food_end_index:obstacle_end_index])

        return hive_locations, food_locations, obstacle_locations
