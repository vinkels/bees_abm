from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from food import Bee
from model import HiveModel

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

    # elif type(agent) is Sugar:
    #     if agent.amount != 0:
    #         portrayal["Color"] = color_dic[agent.amount]
    #     else:
    #         portrayal["Color"] = "#D6F5D6"

    #     portrayal["Shape"] = "rect"
    #     portrayal["Filled"] = "true"
    #     portrayal["Layer"] = 0
    #     portrayal["w"] = 1
    #     portrayal["h"] = 1

    return portrayal

width = 5
height = 5

canvas_element = CanvasGrid(hive_portrayal, width, height, 500, 500)
# chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

server = ModularServer(
    HiveModel, 
    [canvas_element], 
    "Hive", 
    {
        "width": width, 
        "height": height
    }
)
