from mesa import Agent


class Obstacle(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
