from collections import defaultdict

from mesa.time import RandomActivation

from bee import Bee
from food import Food
from hive import Hive

import time


class RandomActivationBeeWorld(RandomActivation):
    '''
    Assumes that all agents have a step() method.

    Adapted from RandomActivationByBreed from mesa/examples
    '''

    def __init__(self, model):
        super().__init__(model)

        self.agents_by_breed = {
            Hive: {},
            Bee: {},
            Food: {}
        }

        self.agent_order = [Food, Hive, Bee]

        self.timing_by_breed = {
            Hive: 0,
            Bee: 0,
            Food: 0
        }

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''
        self._agents[agent.unique_id] = agent

        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''
        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self):
        '''
        Executes the step of each agent breed, one at a time, in random order.
        '''
        for agent_class in self.agent_order:
            breed_start = time.time()
            self.step_breed(agent_class)
            breed_end = time.time()
            self.timing_by_breed[agent_class] += breed_end - breed_start

        self.steps += 1
        self.time += 1

    def step_breed(self, breed):
        '''
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        '''
        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)

        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].step()

    def get_breed_count(self, breed_class):
        '''
        Returns the current number of agents of certain breed in the queue.
        '''
        return len(self.agents_by_breed[breed_class].values())

    def get_bee_count(self, bee_type):
        return sum([
            1
            for agent in self.agents_by_breed[Bee].values()
            if agent.type_bee == bee_type
        ])
