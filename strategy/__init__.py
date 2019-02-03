class BeeStrategy:
    """
    Base Class to create a bee strategy
    """

    def __init__(self, bee):
        self.bee = bee

    def step(self):
        raise NotImplementedError