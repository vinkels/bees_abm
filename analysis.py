from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    pass

def plot_sensitivity_order():
    pass
    # Si_sheep = sobol.analyze(problem, data['Sheep'].as_matrix(), print_to_console=True)
    # Si_wolves = sobol.analyze(problem, data['Wolves'].as_matrix(), print_to_console=True)
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