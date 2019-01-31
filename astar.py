"""
From tutorial: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

Code from https://gist.githubusercontent.com/Nicholas-Swift/003e1932ef2804bebef2710527008f44/raw/8fd79d81dcd5b52d01918b29689e0727154f886c/astar.py
"""

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, route, position=None):
        self.route = route + [position]
        self.position = position

        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node([], start)

    # Init height and width
    width = len(maze)
    height = len(maze[0])

    # Initialize both open and closed list
    open_list = [start_node]
    closed_set = set()

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):

            # Found the goal
            if item.position == end:
                return item.route

            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_set.add(current_node.position)

        curr_x, curr_y = current_node.position

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (curr_x + new_position[0], curr_y + new_position[1])

            # Child position is on the closed list
            if node_position in closed_set:
                continue

            # Make sure within range and walkable
            if 0 <= node_position[0] < width and 0 <= node_position[1] < height and maze[node_position[0]][node_position[1]] == 0:
                # Create new node
                children.append(Node(current_node.route, node_position))

        # Loop through children
        for child in children:
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child_h = ((child.position[0] - end[0]) ** 2) + ((child.position[1] - end[1]) ** 2)
            child.f = child.g + child_h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

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