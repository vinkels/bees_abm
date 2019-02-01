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
from mesa.batchrunner import BatchRunnerMP
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import time as tm
import os
from datetime import datetime


# We define our variables and bounds
params = {
        'nr_vars': 3,
        'bounds':[[1, 3 ,5],[5,10,20],[10,20,30]],
        'names':['obstacle_density','food_density','nr_hives']
        }
var_params = {
    'obstacle_density': [0, 15, 30],
    'food_density': [5, 15, 25],
    'nr_hives': [1,3, 5]
    }


# Set the repetitions, the amount of steps, and the amount of distinct values per variable

replicates = 1
max_steps = 2000
distinct_samples = 3

model_reporters = {
    'step_data': lambda m: m.datacollector.get_model_vars_dataframe(),
    'obstacle_density': lambda m: m.obstacle_density,
    'food_density': lambda m: m.food_density,
    'nr_hives': lambda m: m.nr_hives
}

# Set the outputs
# model_reporters = {
#                    "step_data": lambda m: m.datacollector.get_model_vars_dataframe()
#                    }

data = {}
new_path = datetime.now().strftime('%Y%m%d%H%M')
for i, var in enumerate(params['names']): 
    # names = list(params)
    # names = names.remove(var)
    
    samples = sorted(var_params[var]*distinct_samples)

    batch = BatchRunnerMP(BeeForagingModel,
                        max_steps=max_steps,
                        nr_processes=os.cpu_count(),
                        iterations=replicates,
                        variable_parameters={var:samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()
    data = batch.get_model_vars_dataframe() 

# define a timestamp format you like
    
    data.to_csv(f'pickles/{var}_{new_path}.csv')
    data.to_pickle(f'pickles/{var}_{new_path}.p')








