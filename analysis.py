from SALib.sample import saltelli
import seaborn as sns
from model import BeeForagingModel
from mesa.batchrunner import BatchRunnerMP
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from itertools import combinations
from tqdm import tqdm
from datetime import datetime
import sys

def create_data(problem, new_path):
    """
    problem : dict with specified input variables and range instead of discrete values otherwise saltelli will not work

    Run each batch iterations with all the samples obtained from saltelli and save at the end of the run

    Saves data with time stamp as .csv and .pickle
    """

    # Set the repetitions, the amount of steps, and the amount of distinct values per variable
    replicates = 1
    max_steps = 10
    distinct_samples= 1

    # Define output parameters
    model_reporters = {
        'step_data': lambda m: m.datacollector.get_model_vars_dataframe(),
        'obstacle_density': lambda m: m.obstacle_density,
        'food_density': lambda m: m.food_density,
        'nr_hives': lambda m: m.nr_hives
    }

    data = {}

    # Sample from data with every interactions, computationally expensive but gives all combinations
    params_values = saltelli.sample(problem,N=distinct_samples)

    # change nr of hives to ints -> looks ok 
    # for i, val in enumerate(params_values):
    #     params_values[i][0] = int(val[0])
    # print(params_values)

    #transform to int value and overwrite array if copy needed set flag to True
    params_values = params_values.astype(int, copy=False)
    # test range of combinations
    # print(params_values[:][:,0], len(params_values))
    print(params_values)

    batch = BatchRunnerMP(BeeForagingModel,
                        nr_processes=os.cpu_count(),
                        max_steps=max_steps,
                        variable_parameters={val:[] for val in problem['names']},
                        model_reporters=model_reporters,
                         display_progress=True)
    counter = 0

    # progress bar
    pbar = tqdm(total=len(params_values))
    for _  in range(replicates):
        for values in params_values:
            var_parameters = {}

            # #collect all data samples from salteli sampling
            for n, v, in zip(problem['names'],values):

                var_parameters[n] = v
            batch.run_iteration(var_parameters, tuple(values),counter)
            counter +=1
            pbar.update(counter)
    pbar.close()
    data = batch.get_model_vars_dataframe()

    data.to_csv(f'pickles/analysis_{new_path}.csv')
    data.to_pickle(f'pickles/analysis_{new_path}.p')
    # print('wat ben jij',type(data))
    return data



def clean_data(data, new_path):
    """
    data: pandas datframe saved as  pickle
    The data is one bulk of all combinations of data and just need to loop over the runs
    Assign the input values as columns but also add means en std of output values of interests.

    returns a new pandas dataframe
    """

    final_dfs = []

    for i, row in data.iterrows():
        df_temp = row['step_data']
        df_temp['obstacle_dens'] = row['obstacle_density']
        df_temp['food_dens'] = row['food_density']
        df_temp['n_hives'] = row['nr_hives']
        df_temp['sample'] = row['Run']
        df_temp['step'] = df_temp.index
        final_dfs.append(df_temp)
        # final_dfs.append(df_temp.iloc[500:])
    df_final = pd.concat(final_dfs)

    #TODO Fix create SettingWithcopyWarning, solution make a deepcopy of the result dataframe
    df_test = df_final.copy(deep=True)
    df_test.loc[:,'scout_forage'] = (df_final['scout_bees'] - df_final['forage_bees']) / (df_final['scout_bees'] + df_final['forage_bees'])
    df_test.loc[:,'food_bee'] = df_final['hive_food'] / df_final['n_bees']
    df_test.loc[:,'bees_hive'] = df_final['n_bees'] / df_final['n_hives']
    df_sample = df_test.groupby(['obstacle_dens', 'food_dens', 'n_hives', 'sample'])[
                ['food_bee', 'scout_forage', 'bees_hive']].mean()


    df_sample = df_sample.reset_index()
    print(df_sample)
    df_sample.to_pickle(f'pickles/sobol_small_sample_{new_path}.p')

    return df_sample



def analyse(data, problem):

    Si_scout_forage = sobol.analyze(problem, data['scout_forage'].values, print_to_console=False,n_processors=os.cpu_count(),parallel=True)
    Si_food_bee = sobol.analyze(problem, data['food_bee'].values, print_to_console=False,n_processors=os.cpu_count(), parallel=True)
    Si_bee_hive = sobol.analyze(problem, data['bees_hive'].values, print_to_console=False,n_processors=os.cpu_count(), parallel=True)
    print("Done")
    return Si_scout_forage, Si_food_bee, Si_bee_hive

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
    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')

def plot_sensitivity_order(data,problem, new_path):

    for Si in data:
        # First order
        plot_index(Si, problem['names'], '1', 'First order sensitivity')
        plt.savefig(f'sobol_first_{new_path}.png')

        # Second order
        plot_index(Si, problem['names'], '2', 'Second order sensitivity')
        plt.savefig(f'sobol_second_{new_path}.png')

        # Total order
        plot_index(Si, problem['names'], 'T', 'Total order sensitivity')
        plt.savefig(f'sobol_total_{new_path}.png')


if __name__ == "__main__":
    var_names  = ['nr_hives','obstacle_density', 'food_density']

    # Extract all the present CPU-thread for computation
    groups = np.arange(os.cpu_count())

    dfs = []
    # to make multiple small batches 
    for i in range(2):
        #path timestamp
        new_path = datetime.now().strftime('%Y%m%d%H%M')

        # We define our variables and bounds
        problem = {
            'num_vars': 3,
            'names': ['nr_hives','obstacle_density', 'food_density'],
            'bounds': [[1,6],[0,31],[5,26]],
            'groups':['G'+str(groups[1]),'G'+str(groups[2]),'G'+str(groups[3])] # for multiprocessing
        }
        df = create_data(problem, new_path)
        dfs.append(df)
    data = pd.concat(dfs)
    #TODO make this part interactive?
    # print(df)
    # Change this right_path by running create_data. Mind that max_steps should be bigger.
    # right_path = '201902071158'
    # data = pd.read_pickle(f'pickles/sobol_sample_{new_path}.p')
    cl_data = clean_data(data, new_path)
    Si_scout_forage, Si_food_bee, Si_bee_hive = analyse(cl_data, problem)
    to_plot = [Si_scout_forage, Si_food_bee, Si_bee_hive]
    plot_sensitivity_order(to_plot, problem, new_path)
