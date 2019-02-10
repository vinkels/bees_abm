from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

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

    elif type(agent) is Bee:
        return {
            "Shape": "circle",
            "scale": 0.9,
            "r": 0.5,
            "Layer": 2,
            "Filled": "true",
            "Color": agent.color
        }

    elif type(agent) is Food:
        col_intensity = agent.util

        assert col_intensity >= 0, agent.__dict__

        col_intensity = 4 if col_intensity > 4 else col_intensity

        return {
            "Shape": "circle",
            "scale": 0.9,
            "Layer": 1,
            "Filled": "true",
            "Color": color_dic[col_intensity],
            "r": 0.7
        }

    elif type(agent) is Hive:
        return {
            "Shape": "rect",
            "scale": 0.9,
            "Layer": 0,
            "Filled": "true",
            "w": 1,
            "h": 1,
            "Color": agent.color
        }
    elif agent is OBSTACLE:
        return {
            "Shape": "rect",
            "scale": 0.9,
            "Layer": 0,
            "Filled": "true",
            "Color": "GREY",
            "w": 1,
            "h": 1
        }


width = GRID_WIDTH
height = GRID_HEIGHT


canvas_element = CanvasGrid(hive_portrayal, width, height, 500, 500)
chart_element = ChartModule([{"Label": "n_bees", "Color": "#AA0000"},
                             {"Label": "hive_food", "Color": "#000000"},
                             {"Label": "scout_bees", "Color": "#70a5f9"},
                             {"Label": "forage_bees", "Color": "#f4b042"},
                             {"Label": "rest_bees", "Color": "#17ef71"},
                             {"Label": "baby_bees", "Color": "#ff93d0"}],
                            500, 500)

server = ModularServer(
    BeeForagingModel,
    [canvas_element, chart_element],
    "Hive",
    {
        "width": width,
        "height": height,
        "obstacle_density": UserSettableParameter('slider',
                                                  'obstacle density',
                                                  value=0,
                                                  min_value=0,
                                                  max_value=100),
        "food_density": UserSettableParameter('slider',
                                              'food density',
                                              value=1,
                                              min_value=0,
                                              max_value=100),
        "VIZUALISATION": True
    }
)
