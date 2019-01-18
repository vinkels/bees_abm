from mesa import Agent
import random as rd


class Hive(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.food_locs = []
        self.food = 0
        self.n_bees = 0
        self.hungry = False
        # self.energy_level_critical = 10
        # self.energy_level_optimal = 100
        # self.energy_level_minimum = 25

    def receive_info(self, info):
        if info not in self.food_locs:
            self.food_locs.append(info)

    def step(self):

        # Make random new bees
        # TODO make this actually depend on queen, drones and food resources.

        # determine number of bees in hive
        bees_hive = self.model.grid.get_neighbors(self.pos, moore=True, include_center = True, radius = 0)
        self.n_bees = len(bees_hive)
        # hungry_count = 0

        # # give every bee a chance of reproduction
        for bee in range(0, self.n_bees):
            
        #     if self.food > 0:
        #         self.food -= 1
        #         self.hungry = False
        #         hungry_count = 0

        #     else:
        #         self.hungry = True
        #         hungry_count += 1

        #     if not self.hungry:
                # if self.n_bees > self.food:
            if rd.random() > 0.99:
                self.model.add_bee(self.pos, self, "rester")
                self.n_bees += 1

                # else:
                #     if rd.random() > 0.90:
                #         self.model.add_bee(self.pos, self, "rester")
                #         self.n_bees += 1

        # print("bees hungry: ", hungry_count)
        # print("percentage hungry: ", hungry_count/self.n_bees)

        # # determine percentage hungry bees, and let bees die when more hunger in hive
        # if rd.random() < hungry_count/self.n_bees:
        #     bee_die = rd.randint(0, self.n_bees - 1)
        #     self.model.remove_agent(bees_hive[bee_die])

        # if self.hungry is True:
        #     hungry_count += 1
        #     if hungry_count > 5:
        #         print(bees_hive[0])
        #         self.model.remove_agent(bees_hive[0])

        if rd.random() > 0.90: #self.energy_level_critical/100.0:
            self.model.add_bee(self.pos, self, "scout")

        self.balance_hive()

        
    def unload_food(self, food=1):
        self.food += 10

    def get_food_stat(self):
        return self.food
    
    def balance_hive(self):
        pass
        # if self.food > 0:
        #     if self.food == self.energy_level_optimal:
        #         self.model.add_bee(self.pos, self, "rester")
        #         self.food = 0.5*self.energy_level_minimum
        #     if self.food > self.energy_level_optimal:
        #         self.food = 0.1*self.energy_level_critical
