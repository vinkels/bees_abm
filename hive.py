from mesa import Agent
import random as rd


class Hive(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.food_locs = []

        self.food = 0
        # self.energy_level_critical = 10
        # self.energy_level_optimal = 100
        # self.energy_level_minimum = 25

    def receive_info(self, info):
        if info not in self.food_locs:
            self.food_locs.append(info)

    def step(self):

        # Make random new bees
        # TODO make this actually depend on queen, drones and food resources.
        print(self.food_locs)

        if rd.random() > 0.90: #self.energy_level_critical/100.0:
            self.model.add_bee(self.pos, self, "scout")

        self.balance_hyve()

    def unload_food(self, food=1):
        self.food += 1

    def get_food_stat(self):
        return self.food
    
    def balance_hyve(self):
        pass
        # if self.food > 0:
        #     if self.food == self.energy_level_optimal:
        #         self.model.add_bee(self.pos, self, "rester")
        #         self.food = 0.5*self.energy_level_minimum
        #     if self.food > self.energy_level_optimal:
        #         self.food = 0.1*self.energy_level_critical
           
            
                
                
            

