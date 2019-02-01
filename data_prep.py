import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_prep():
    final_dfs = []
    df = pd.read_pickle('pickles/test_nr_hives.p')

    cur_samp = 0
    sample = 0
    for i, row in df.iterrows():
        df_temp = df.at[i, 'step_data']
        df_temp['obstacle_dens'] = row['obstacle_density']
        df_temp['food_dens'] = row['food_density']
        df_temp['n_hives'] = row['nr_hives']
        df_temp['sample'] = row['Run']
        df_temp['step'] = df_temp.index
        sample += 1
        final_dfs.append(df_temp)
    df_final = pd.concat(final_dfs)
    df_new = df_final[['n_hives', 'food_dens', 'obstacle_dens', 'sample', 'step', 'death_age']]
    df_new['scout_forage'] = (df_final['scout_bees'] - df_final['forage_bees']) / (df_final['scout_bees'] + df_final['forage_bees'])
    df_new['food_bee'] = df_final['hive_food'] / df_final['n_bees']
    df_new['bees_hive'] = df_final['n_bees'] / df_final['n_hives']
    df_new.to_csv('pickles/test_newnew.csv')
    df_step = df_new.groupby(['obstacle_dens', 'food_dens', 'n_hives', 'step']).agg({
                                                                                    'food_bee': ['mean', 'std'], 
                                                                                    'scout_forage': ['mean', 'std'], 
                                                                                    'bees_hive': ['mean', 'std'], 
                                                                                    'death_age': ['mean', 'std']
                                                                                    })
    
    # [['food_bee', 'scout_forage', 'bees_hive', 'death_age']].mean().std()
    print(df_step)
    # df_step = df_step.reset_index()
    # df_sample = df_new.groupby(['obstacle_dens', 'food_dens', 'n_hives', 'sample'])[
    #     ['food_bee', 'scout_forage', 'bees_hive', 'death_age']].mean()
    # df_sample = df_sample.reset_index()
    # print(df_sample)
    

def make_pwetty_plots():


if __name__ == "__main__":
    data_prep()


        

    
