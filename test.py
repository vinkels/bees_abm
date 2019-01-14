from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid

'''
Bijen:
- food coordinate when found
- food quality (utility value)
- accuracy of giving food direction
- energy/fatique of bee
- bee maximum travel distance
- range vision
'''

'''
'''

class HiveModel(Model):
    def __init__(self, width, height):
        self.height = width
        self.width = height
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.start_food = 10
        self.n_food = 0
        self.foods = []
        self.init_food()

    def init_food(self):
        for i in range(self.start_food):
            pos = (rd.randrange(self.width), rd.randrange(self.height))
            util = rd.randint(0, 10)
            food = Food(i, self, pos, util)
            self.foods.add(food)


    def new_food(self, pos):

        self.n_food += 1
        new_food = agent_type(Food, self, pos)
        self.grid.place_agent(new_food, pos)
        self.foods.append(new_food)

    def remove_food(self, food):
        '''
        Method that enables us to remove passed agents.
        '''
        self.n_food -= 1

        # Remove agent from grid
        self.grid.remove_agent(food)

        # Remove agent from model
        self.agents.remove(food)

    def step(self):

        for food in list(self.foods):
            food.step()


    class Food(Agent):
        def __init__(self, id, model, pos, util):
            super().__init__(id, model)
            self.pos = pos
            self.util = util

        def step(self):

            print(f'current utility: {self.util}')

if __name__ == '__main__':
    model = HiveModel(10, 10)
