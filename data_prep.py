import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_prep():
    
    var_names = ['food_density', 'nr_hives', 'obstacle_density']
    right_time = '201902030912'
    step_dct = {}
    sample_dct = {}
    for name in var_names:
        df = pd.read_pickle(f'pickles/{right_time}_{name}.p')
        cur_samp = 0
        sample = 0
        final_dfs = []
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
        df_new = df_final[['n_hives', 'food_dens', 'obstacle_dens', 'sample', 'step']]
        df_new['scout_forage'] = (df_final['scout_bees'] - df_final['forage_bees']) / (df_final['scout_bees'] + df_final['forage_bees'])
        df_new['food_bee'] = df_final['hive_food'] / df_final['n_bees']
        df_new['bees_hive'] = df_final['n_bees'] / df_final['n_hives']
        df_new.to_csv('pickles/test_newnew.csv')
        df_step = df_new.groupby(['obstacle_dens', 'food_dens', 'n_hives', 'step']).agg({
                                                                                        'food_bee': ['mean', 'std'], 
                                                                                        'scout_forage': ['mean', 'std'], 
                                                                                        'bees_hive': ['mean', 'std']
                                                                                        })

        df_step = df_step.reset_index()
        df_step.columns = ['_'.join(col) if col[1] else col[0] for col in df_step.columns]
        step_dct[name] = df_step

        df_sample = df_new.groupby(['obstacle_dens', 'food_dens', 'n_hives', 'sample'])[
            ['food_bee', 'scout_forage', 'bees_hive']].mean()
        df_sample = df_sample.reset_index()
        sample_dct[name] = df_sample
        return step_dct, sample_dct
        

    def make_pwetty_plots(df_new):
        # plt.plot(df_new['scout_forage'], df_new['food_bee'], 'bo')
        # plt.savefig('jup.png')
        # df_new['n_hives'] = df_new["n_hives"].astype('category')
        sns_plot = sns.lineplot(x="step", y="food_bee", hue="n_hives",data=df_new)
        plt.savefig('plots/plot2.png')
        

if __name__ == "__main__":
    df_new = data_prep()
    # make_pwetty_plots(df_new)


        

    
