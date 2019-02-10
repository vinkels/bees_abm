import os
import pickle
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mesa.batchrunner import BatchRunnerMP

import seaborn as sns
from model import BeeForagingModel


class OFAT():
    def __init__(self, time_stamp=False, warm_it=500):
        self.var_names = ['food_density', 'nr_hives', 'obstacle_density']
        self.warm_it = warm_it
        if not time_stamp:
            self.time_stamp = datetime.now().strftime('%Y%m%d%H%M')
        else:
            self.time_stamp = time_stamp

    def run_ofat(self):
        # We define our variables and bounds
        params = {
            'obstacle_density': [0, 15, 30],
            'food_density': [5, 15, 25],
            'nr_hives': [1, 3, 5]
        }

<<<<<<< HEAD

        # Set the repetitions, the amount of steps, and the amount of distinct values per variable

        replicates = 500
=======
        # Set the repetitions and the amount of steps
        replicates = 400
>>>>>>> fc30fc0c4174ca55c6a81c96aed4ff10e2ae696c
        max_steps = 3000

        # Define output parameters
        model_reporters = {
            'step_data': lambda m: m.datacollector.get_model_vars_dataframe(),
            'obstacle_density': lambda m: m.obstacle_density,
            'food_density': lambda m: m.food_density,
            'nr_hives': lambda m: m.nr_hives
        }

        for var in params:
            batch = BatchRunnerMP(BeeForagingModel,
                                  max_steps=max_steps,
                                  nr_processes=os.cpu_count(),
                                  iterations=replicates,
                                  variable_parameters={var: params[var]},
                                  model_reporters=model_reporters,
                                  display_progress=True)

            batch.run_all()

            # Collect data from batch.
            data = batch.get_model_vars_dataframe()
            data.to_csv(f'pickles/{self.time_stamp}_{var}.csv')
            data.to_pickle(f'pickles/{self.time_stamp}_{var}.p')

    def data_prep(self):
        self.step_dct = {}
        self.sample_dct = {}

        for name in self.var_names:
            df = pd.read_pickle(f'pickles/{self.time_stamp}_{name}.p')

            sample = 0
            final_dfs = []
            for i, row in df.iterrows():
                df_temp = df.at[i, 'step_data']
                df_temp['obstacle_density'] = row['obstacle_density']
                df_temp['food_density'] = row['food_density']
                df_temp['nr_hives'] = row['nr_hives']
                df_temp['sample'] = row['Run']
                df_temp['step'] = df_temp.index
                sample += 1
                final_dfs.append(df_temp.iloc[self.warm_it-1:])

            df_final = pd.concat(final_dfs)
            df_new = df_final[['nr_hives', 'food_density', 'obstacle_density', 'sample', 'step']]
            df_new['scout_forage'] = (df_final['scout_bees'] - df_final['forage_bees']) / (df_final['scout_bees'] + df_final['forage_bees'])
            df_new['food_bee'] = df_final['hive_food'] / df_final['n_bees']
            df_new['bees_hive'] = df_final['n_bees'] / df_final['nr_hives']

            df_step = df_new.groupby(
                ['obstacle_density', 'food_density', 'nr_hives', 'step']
            ).agg({
                'food_bee': ['mean', 'std'],
                'scout_forage': ['mean', 'std'],
                'bees_hive': ['mean', 'std']
            })

            df_step = df_step.reset_index()
            df_step.columns = ['_'.join(col) if col[1] else col[0]
                               for col in df_step.columns]

            self.step_dct[name] = df_step
            df_step.to_pickle(f'pickles/step_{name}_{self.time_stamp}.p')

            df_sample = df_new.groupby(
                ['obstacle_density', 'food_density', 'nr_hives', 'sample']
            )[['food_bee', 'scout_forage', 'bees_hive']].mean()

            df_sample = df_sample.reset_index()
            df_step.to_pickle(f'pickles/sample_{name}_{self.time_stamp}.p')
            self.sample_dct[name] = df_sample

        return self.sample_dct, self.step_dct

    def make_pwetty_plots(self, df_new):
        sns_plot = sns.lineplot(x="step",
                                y="food_bee",
                                hue="nr_hives",
                                data=df_new)
        plt.savefig('plots/plot2.png')
<<<<<<< HEAD
            
    def get_ofat(self):
        """

        """
=======
>>>>>>> fc30fc0c4174ca55c6a81c96aed4ff10e2ae696c

    def get_ofat(self):
        self.ofat_dict, self.df_plot = self.data_prep()

        for param in ('food_bee', 'scout_forage', 'bees_hive'):
            self.plot_all_vars(param)
            plt.savefig(f'plots/test_ofat_{param}.png')

    def plot_param_var_conf(self, ax, df, var, param, i):
        """
        Helper function for plot_all_vars. Plots the individual parameter vs
        variables passed.

        Args:
            ax: the axis to plot to
            df: dataframe that holds the data to be plotted
            var: variables to be taken from the dataframe
            param: which output variable to plot
        """
        x = df.groupby(var).mean().reset_index()[var]
        y = df.groupby(var).mean()[param]

        replicates = df.groupby(var)[param].count()
        err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

        ax.plot(x, y, c='k')
        ax.fill_between(x, y - err, y + err)

        ax.set_xlabel(var)
        ax.set_ylabel(param)

    def plot_all_vars(self, param):
        """
        Plots the parameters passed vs each of the output variables.

        Args:
            df: dataframe that holds all data
            param: the parameter to be plotted
        """
        f, axs = plt.subplots(3, figsize=(7, 10))

        for i, var in enumerate(self.var_names):
            self.plot_param_var_conf(axs[i], self.ofat_dict[var], var, param)


if __name__ == "__main__":
    ofat_obj = OFAT()
    ofat_obj.run_ofat()
    ofat_obj.get_ofat()
