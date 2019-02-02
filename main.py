import model as md
import time

from config import GRID_WIDTH, GRID_HEIGHT

from util import path_finder


def main():
    # bee_model = md.BeeForagingModel(GRID_WIDTH, GRID_HEIGHT, 10, 30, 7)

    # Start at 16.0721 for 100000 iterations 5,5
    # After immediate children eval 15.8216 for 100000 iterations 5,5
    # After Moore static 15.7563 for 100000 iterations 5,5
    # With earlier astar exit 15.1243 for 100000 iterations 5,5
    # Cython compiled 10.8601 for 100000 iterations 5,5
    # Cython compiled 3.2140 for 1000 iterations 50,50
    # Cython compiled 27.7039 for 100 iterations 50,50 with proper wall 

    import numpy as np
    grid = np.zeros((50, 50))
    start = (0, 0)
    end = (50, 50)

    grid[48][48] = 1
    for i in range(1, 48):
        grid[48][i] = 1
        grid[i][48] = 1

    tt = 0

    for _ in range(100):
        s = time.time()
        path_finder(start, end, grid, 50, 50)
        e = time.time()
        tt += e - s

    print(tt)

#     for i in range(10000):
        # print(f'ITERATION {i*1}')

        # print({k: len(v) for k, v in bee_model.grid.grids.items()})
        # start_time = tm.time()
        # bee_model.run_model(1)
        # print(tm.time() - start_time)

        # print(bee_model.total_schedule_time)
        # print(bee_model.schedule.timing_by_breed)
        # print(bee_model.time_by_strategy)
        # print(bee_model.planning_time)
        # print(bee_model.grid.timings)

        # print({k: len(v) for k, v in bee_model.schedule.agents_by_breed.items()})

        # print(bee_model.timings_scout)

main()
