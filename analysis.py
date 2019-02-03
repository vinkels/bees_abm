from SALib.sample import saltelli
# from wolf_sheep.model import WolfSheep
# from wolf_sheep.agents import Wolf, Sheep
from model import BeeForagingModel
from mesa.batchrunner import BatchRunnerMP
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import os
# import matplotlib.pyplot as plt
# from itertools import combinations
from tqdm import tqdm
from datetime import datetime

def prepare_data():

    # We define our variables and bounds
    # params = {
    #         'obstacle_density': [0, 15, 30],
    #         'food_density': [5, 15, 25],
    #         'nr_hives': [1, 3, 5],
    #         'num_vars': 3,
    #         'bounds':[[0,15,30],[5,15,25],[1,3,5]]
    #         }

    new_path = datetime.now().strftime('%Y%m%d%H%M')
    # Set the repetitions, the amount of steps, and the amount of distinct values per variable

    replicates = 10
    max_steps = 1000
    distinct_samples= 10

    # Define output parameters
    model_reporters = {
        'step_data': lambda m: m.datacollector.get_model_vars_dataframe(),
        'obstacle_density': lambda m: m.obstacle_density,
        'food_density': lambda m: m.food_density,
        'nr_hives': lambda m: m.nr_hives
    }

    data = {}

    # Same datastructure but different design to match requirements in retrieving sampling
    problem = {
    'num_vars': 3,
    'names': ['nr_hives','obstacle_density', 'food_density'],
    'bounds': [[1,6],[0,31],[5,26]]
    # 'dists': ['unif', 'unif','unif']
    }
    params_values = saltelli.sample(problem,N=distinct_samples, calc_second_order=True)
    #transform to int value and overwrite array if copy needed set flag to True
    params_values = params_values.astype(int, copy=False)
    # print(np.where(params_values == 5))
    # print(params_values[:][:,0], len(params_values))
    

    # params_values_ = saltelli.sample(params,N=distinct_samples, calc_second_order=False)
    # test = {val:[] for val in problem['names']}
    # print(test)
    # test = np.allclose(params_values, params_values_)
    # print(test)
    batch = BatchRunnerMP(BeeForagingModel,
                        nr_processes=os.cpu_count(),
                        max_steps=max_steps,
                        variable_parameters={val:[] for val in problem['names']},
                        model_reporters=model_reporters)
    counter = 0
    # progress bar
    pbar = tqdm(total=replicates)
    for i in range(replicates):
        for values in params_values:
            var_parameters = {}
            #collect all data samples from salteli sampling
            for n, v, in zip(problem['names'],values):
                var_parameters[n] = v
            batch.run_iteration(var_parameters, tuple(values),counter)
            counter +=1
            # data = batch.get_model_vars_dataframe() 
            # data.to_csv(f'pickles/{counter}_{new_path}.csv')
            # data.to_pickle(f'pickles/{counter}_{new_path}.p')
            pbar.update(counter)
    pbar.close()
    data = batch.get_model_vars_dataframe()
    data.to_csv(f'pickles/analysis_{new_path}.csv')
    data.to_pickle(f'pickles/analysis_{new_path}.p')
    return data

def analyse(data):
    pass
    # Si_sheep = sobol.analyze(problem, data['Sheep'].as_matrix(), print_to_console=True)
    # Si_wolves = sobol.analyze(problem, data['Wolves'].as_matrix(), print_to_console=True)
    
def plot_param_var_conf(ax, df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    pass
    # x = df.groupby(var).mean().reset_index()[var]
    # y = df.groupby(var).mean()[param]

    # replicates = df.groupby(var)[param].count()
    # err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    # ax.plot(x, y, c='k')
    # ax.fill_between(x, y - err, y + err)

    # ax.set_xlabel(var)
    # ax.set_ylabel(param)

def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """
    pass
    # f, axs = plt.subplots(3, figsize=(7, 10))
    
    # for i, var in enumerate(problem['names']):
    #     plot_param_var_conf(axs[i], data[var], var, param, i)

# for param in ('Sheep', 'Wolves'):
#     plot_all_vars(data, param)
#     plt.show()

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """
    pass
    # if i == '2':
    #     p = len(params)
    #     params = list(combinations(params, 2))
    #     indices = s['S' + i].reshape((p ** 2))
    #     indices = indices[~np.isnan(indices)]
    #     errors = s['S' + i + '_conf'].reshape((p ** 2))
    #     errors = errors[~np.isnan(errors)]
    # else:
    #     indices = s['S' + i]
    #     errors = s['S' + i + '_conf']
    #     plt.figure()

    # l = len(indices)

    # plt.title(title)
    # plt.ylim([-0.2, len(indices) - 1 + 0.2])
    # plt.yticks(range(l), params)
    # plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    # plt.axvline(0, c='k')

def plot_sensitivity_order():
    pass
    # for Si in (Si_sheep, Si_wolves):
    #     # First order
    #     plot_index(Si, problem['names'], '1', 'First order sensitivity')
    #     plt.show()

    #     # Second order
    #     plot_index(Si, problem['names'], '2', 'Second order sensitivity')
    #     plt.show()

    #     # Total order
    #     plot_index(Si, problem['names'], 'T', 'Total order sensitivity')
    #     plt.show()
if __name__ == "__main__":
    dt = prepare_data()
    
    print(dt.shape)