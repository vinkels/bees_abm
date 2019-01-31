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

        portrayal["Color"] = agent.color
    

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
      
        portrayal["Color"] = agent.color

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
chart_element = ChartModule([{"Label": "n_bees", "Color": "#AA0000"}, {"Label": "hive_food", "Color": "#000000"}, {"Label": "scout_bees", "Color": "#70a5f9"},
    {"Label": "forage_bees", "Color": "#f4b042"}, {"Label": "rest_bees", "Color": "#17ef71"}, {"Label": "baby_bees", "Color": "#ff93d0"}], 500, 500)

server = ModularServer(
    BeeForagingModel,
    [canvas_element,chart_element],
    "Hive",
    {
        "width": width,
        "height": height,
        "obstacle_density": UserSettableParameter('slider', 'obstacle density', value=0, min_value=0, max_value=100),
        "food_density": UserSettableParameter('slider', 'food density', value=1, min_value=0, max_value=100)
    }
)
