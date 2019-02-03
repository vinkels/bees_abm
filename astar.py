"""
From tutorial: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

Code from https://gist.githubusercontent.com/Nicholas-Swift/003e1932ef2804bebef2710527008f44/raw/8fd79d81dcd5b52d01918b29689e0727154f886c/astar.py
"""

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, route, position=None, f=0, g=0):
        self.route = route + [position]
        self.position = position

        self.f = f
        self.g = g

    def __eq__(self, other):
        return self.position == other.position


WIDTH = 50
HEIGHT = 50
MOORE_NEIGHBOURS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node([], start)
    end_0, end_1 = end

    # Initialize both open and closed list
    open_list = [start_node]
    closed_set = set()
    seen = set()

    i = 0

    # Loop until you find the end
    while len(open_list) > 0:
        i += 1

        # Get the current node
        current_f = open_list[0].f
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_f:
                current_f = item.f
                current_index = index

        # Pop current off open list, add to closed list
        current_node = open_list.pop(current_index)
        closed_set.add(current_node.position)

        curr_x, curr_y = current_node.position

        # g value is used for prioritization
        g = current_node.g + 1

        for new_position in MOORE_NEIGHBOURS: # Adjacent squares

            # Get node position
            node_position = (curr_x + new_position[0], curr_y + new_position[1])

            if node_position == end:
                return current_node.route + [end]

            # Child position is on the closed list
            if node_position in closed_set:
                continue

            n0, n1 = node_position

            # Make sure within range and walkable
            if 0 <= n0 < 50 and 0 <= n1 < 50 and maze[n0][n1] == 0:

                # Create the f, g, and h values
                h = ((n0 - end_0) ** 2) + ((n1 - end_1) ** 2)
                f = g + h

                if node_position not in seen:
                    seen.add(node_position)
                    # Add the child to the open list
                    open_list.append(Node(current_node.route, node_position, f, g))

# def main():

# maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# start = (0, 0)
# end = (7, 6)

# path = astar(maze, start, end)
# print(path)