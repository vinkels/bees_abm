from mesa import Agent
import random as rd


class Food(Agent):
    def __init__(self, model, pos, util_pars=(5, 2.5), max_step=3):
        super().__init__(model.next_id(), model)
        self.max_step = max_step

        self.pos = pos

        #TODO GENERATE RANDOMNESS BETWEEN 1 AND MAX_UTIL CHANGE THIS IN MODEL.PY
 
        
        self.max_util = int(round(np.random.normal(util_pars[0], util_pars[1])))
        self.util = rd.randint(1, self.max_util)
        self.steps = 0

    def step(self):
        #TODO CHANGE STEPCOUNT  AND ADD THIS VARIABLE IN CONFIG
        if self.steps % self.max_step == 0:
            if self.util < self.max_util:
                self.util += 1

        self.steps += 1


    def get_eaten(self):
        #TODO THIS SHOULD DEPENDENT ON CARRYING CAPACITY OF BEES. 
        self.util -= 1
