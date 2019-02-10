import model as md
import time

from config import GRID_WIDTH, GRID_HEIGHT


def main():
    """
    Class used in testing the bee_model internally.
    """
    bee_model = md.BeeForagingModel(GRID_WIDTH, GRID_HEIGHT, 10, 30, 7)

    iteration_size = 1000

    for i in range(45):
        print(f'ITERATION {i*iteration_size}')

        print({k: len(v) for k, v in bee_model.grid.grids.items()})
        start_time = time.time()
        bee_model.run_model(iteration_size)
        print(time.time() - start_time)


main()
