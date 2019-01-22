from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization import TextVisualization

from food import Food
from bee import Bee
from hive import Hive
from obstacle_grid import OBSTACLE

from model import BeeForagingModel

color_dic = {
    4: "#005C00",
    3: "#008300",
    2: "#00AA00",
    1: "#00F800",
    0: "#FFFFFF"
}


def hive_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Bee:
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.5
        if agent.hive_id == 0:
            portrayal["Color"] = "PURPLE"
        elif agent.hive_id == 1:
            portrayal["Color"] = "ORANGE"

    elif type(agent) is Food:
        col_intensity = agent.util
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

width = 100
height = 100

canvas_element = CanvasGrid(hive_portrayal, width, height, 500, 500)
chart_element = ChartModule([{"Label": "Bees", "Color": "#AA0000"}, {"Label": "HiveFood", "Color": "#000000"}, {"Label": "Scout bees", "Color": "#70a5f9"},
    {"Label": "Foraging bees", "Color": "#f4b042"}, {"Label": "Rester bees", "Color": "#17ef71"}, {"Label": "Baby bees", "Color": "#ff93d0"}], 500, 500)
# error_text = TextVisualization.TextData(BeeForagingModel, var_name="user_error")
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
