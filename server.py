from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from food import Bee, Food
from model import BeeForagingModel

color_dic = {
    4: "#005C00",
    3: "#008300",
    2: "#00AA00",
    1: "#00F800"
}


def hive_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Bee:
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = "#000000"
        portrayal["r"] = 0.5

    if type(agent) is Food:
        portrayal["Shape"] = "circle"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = "#f4df42"
        portrayal["r"] = 0.5

    return portrayal

width = 5
height = 5

canvas_element = CanvasGrid(hive_portrayal, width, height, 500, 500)
chart_element = ChartModule([{"Label": "Bees", "Color": "#AA0000"}])

server = ModularServer(
    BeeForagingModel, 
    [canvas_element, chart_element], 
    "Hive", 
    {
        "width": width, 
        "height": height
    }
)
