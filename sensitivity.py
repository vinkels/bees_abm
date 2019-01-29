from mesa import Model
from mesa import Agent
from mesa.datacollection import DataCollector
from SALib.sample import saltelli
from food import Food
from bee import Bee
from hive import Hive
from schedule import RandomActivationBeeWorld
from model import BeeForagingModel
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import time as tm

#TODO: number of hives, food availability, 
# We define our variables and bounds


var_params = {'obstacle_density': [10, 20, 30],
              'food_density': [5, 10, 20]}

fixed_params = {"width": 50,
                "height": 50
                }

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 50
distinct_samples = 10

# Set the outputs
model_reporters = {"n_bees": lambda m: m.schedule.get_breed_count(Bee),
                   "food": lambda m: m.hives[m.hive.unique_id].get_food_stat(),
                   "scout_bee": lambda m: m.schedule.get_bee_count("scout"),
                   "forage_bee": lambda m: m.schedule.get_bee_count("foraging"),
                   "rest_bee": lambda m: m.schedule.get_bee_count("rester"),
                   "baby_bee": lambda m: m.schedule.get_bee_count("babee")}

data = {}

# for i, var in enumerate(problem['names']):
#     # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
#     samples = problem['bounds'][i]

#     # Keep in mind that wolf_gain_from_food should be integers. You will have to change
#     # your code to acommidate for this or sample in such a way that you only get integers.


batch = BatchRunner(BeeForagingModel,
                    max_steps=max_steps,
                    iterations=replicates,
                    fixed_parameters=fixed_params,
                    variable_parameters=var_params,
                    model_reporters=model_reporters,
                    display_progress=True)

batch.run_all()
jup = batch.get_model_vars_dataframe()
jup.to_csv('jeej.csv')

# data[var] = batch.get_model_vars_dataframe()



