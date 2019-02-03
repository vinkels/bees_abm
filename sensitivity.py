from model import BeeForagingModel
from mesa.batchrunner import BatchRunnerMP
import os
from datetime import datetime


# We define our variables and bounds
params = {
        'obstacle_density': [0, 15, 30],
        'food_density': [5, 15, 25],
        'nr_hives': [1, 3, 5]
        }


# Set the repetitions, the amount of steps, and the amount of distinct values per variable

replicates = 10
max_steps = 2000

# Define output parameters
model_reporters = {
    'step_data': lambda m: m.datacollector.get_model_vars_dataframe(),
    'obstacle_density': lambda m: m.obstacle_density,
    'food_density': lambda m: m.food_density,
    'nr_hives': lambda m: m.nr_hives
}


data = {}

#Define time format
time_stamp = datetime.now().strftime('%Y%m%d%H%M')
for var in params: 

    batch = BatchRunnerMP(BeeForagingModel,
                        max_steps=max_steps,
                        nr_processes=os.cpu_count(),
                        iterations=replicates,
                        variable_parameters={var:params[var]},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()
    data = batch.get_model_vars_dataframe() 
    data.to_csv(f'pickles/{time_stamp}_{var}.csv')
    data.to_pickle(f'pickles/{time_stamp}_{var}.p')
