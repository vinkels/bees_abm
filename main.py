from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import model as md
import time as tm


def main():
    bee_model = md.BeeForagingModel(100, 100, 1, 10)

    start_time = tm.time()
    bee_model.run_model(1000)
    print(tm.time() - start_time)

    df = bee_model.datacollector.get_model_vars_dataframe()
    df2 = bee_model.datacollector2.get_model_vars_dataframe()
    df.to_pickle('pickles/huppelfluppel.p')
    df.to_csv('pickles/df.csv')
    df2.to_csv('pickles/df2.csv')


main()
