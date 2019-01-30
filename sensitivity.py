from SALib.sample import saltelli
from food import Food
from bee import Bee
from hive import Hive
from schedule import RandomActivationBeeWorld
import model as md
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import time as tm

#TODO: number of hives, food availability, 
# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['bee', 'wolf_reproduce', 'wolf_gain_from_food'],
    'bounds': [[0.01, 0.1], [0.01, 0.1], [10, 40]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 100
distinct_samples = 20

# Set the outputs
model_reporters = {model_reporters = {"Bees": lambda m: m.schedule.get_breed_count(Bee),
                                      "HiveFood": lambda m: m.hive.get_food_stat()/10,
                                      "Scout bees": lambda m: m.schedule.get_bee_count("scout"),
                                      "Foraging bees": lambda m: m.schedule.get_bee_count("foraging"),
                                      "Rester bees": lambda m: m.schedule.get_bee_count("rester"),
                                      "Baby bees": lambda m: m.schedule.get_bee_count("babee")}}

data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # Keep in mind that wolf_gain_from_food should be integers. You will have to change
    # your code to acommidate for this or sample in such a way that you only get integers.
    if var == 'wolf_gain_from_food':
        samples = np.linspace(
            *problem['bounds'][i], num=distinct_samples, dtype=int)

    batch = BatchRunner(WolfSheep,
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()



