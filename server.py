from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization import TextVisualization

from food import Food
from bee import Bee
from hive import Hive
from obstacle_grid import OBSTACLE
from config import GRID_HEIGHT, GRID_WIDTH
from model import BeeForagingModel

color_dic = {
    4: "#005C00",
    3: "#008300",
    2: "#00AA00",
    1: "#00F800",
    0: "red"
}


def hive_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Bee:
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.9
        portrayal["r"] = 0.5
        portrayal["Layer"] = 2
        portrayal["Filled"] = "true"

        if agent.hive_id == 0:
            portrayal["Color"] = "PURPLE"
        elif agent.hive_id == 1:
            portrayal["Color"] = "ORANGE"
        elif agent.hive_id == 2:
            portrayal["Color"] = "PINK"

    elif type(agent) is Food:
        col_intensity = agent.util

        assert col_intensity >= 0, agent.__dict__

        if col_intensity > 4:
            col_intensity = 4
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = color_dic[col_intensity]
        portrayal["r"] = 0.7

    elif type(agent) is Hive:
        portrayal["Shape"] = "rect"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        portrayal["w"] = 1
        portrayal["h"] = 1
        #TODO DYNAMICALLY GIVE DIFFERENT COLOURS TO DIFFERENT NUMBERS OF HIVES
        if agent.unique_id == 0:
            portrayal["Color"] = "RED"
        else:
            portrayal["Color"] = "GREEN"

    elif agent is OBSTACLE:
        portrayal["Shape"] = "rect"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "GREY"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

width = GRID_WIDTH
height = GRID_HEIGHT

canvas_element = CanvasGrid(hive_portrayal, width, height, 500, 500)
chart_element = ChartModule([{"Label": "Bees", "Color": "#AA0000"}, {"Label": "HiveFood", "Color": "#000000"}, {"Label": "Scout bees", "Color": "#70a5f9"},
    {"Label": "Foraging bees", "Color": "#f4b042"}, {"Label": "Rester bees", "Color": "#17ef71"}, {"Label": "Baby bees", "Color": "#ff93d0"}], 500, 500)

server = ModularServer(
    BeeForagingModel,
    [canvas_element, chart_element],
    "Hive",
    {
        "width": width,
        "height": height,
        "obstacle_density": UserSettableParameter('slider', 'obstacle density', value=0, min_value=0, max_value=100),
        "food_density": UserSettableParameter('slider', 'food density', value=1, min_value=0, max_value=100)
    }
)
