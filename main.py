import model as md
import time as tm

from config import GRID_WIDTH, GRID_HEIGHT


def main():
    bee_model = md.BeeForagingModel(GRID_WIDTH, GRID_HEIGHT, 10, 30, 7)

    for i in range(45):
        print(f'ITERATION {i*1000}')

        print({k: len(v) for k, v in bee_model.grid.grids.items()})
        start_time = tm.time()
        bee_model.run_model(1000)
        print(tm.time() - start_time)

        print(bee_model.total_schedule_time)
        print(bee_model.schedule.timing_by_breed)
        print(bee_model.time_by_strategy)
        print(bee_model.planning_time)
        print(bee_model.grid.timings)

        print({k: len(v) for k, v in bee_model.schedule.agents_by_breed.items()})

        print(bee_model.timings_scout)

main()
