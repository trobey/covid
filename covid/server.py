from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement

from .model import Covid
from .SimpleContinuousModule import SimpleCanvas


def virus_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": agent.color}


virus_canvas = SimpleCanvas(virus_draw, 500, 500)
model_params = {
    "population": 100,
    "width": 100,
    "height": 100,
    "mobility": 6,
    "social_distance": 2,
    "asymptomatic_percentage": 50.0,
}

class CovidTextElement(TextElement):
    def render(self, model):
        infected = round(100 * model.count("Infected") / model.population, 1)
        susceptible = round(100 * model.count("Susceptible") / model.population ,1)
        return "location: " + model.state + " (infected " + str(infected) + "% susceptible " + str(susceptible) + "%)"

text_element = CovidTextElement()

chart_element = ChartModule([{"Label": "Susceptible", "Color": "#666666"},
                             {"Label": "Infected", "Color": "#AA0000"},
                             {"Label": "Recovered", "Color": "#00AA00"}])

model_params = {"population": UserSettableParameter('slider', 'Population', 100, 0, 500),
                "imperial": UserSettableParameter('checkbox', 'Imperial College Model', True),
                "asymptomatic_percentage": UserSettableParameter('slider', 'Asymptomatic (%)', 50, 0, 100),
                "social_distance": UserSettableParameter('slider', 'Social Distance ', 2.0, 0.0, 5.0, 0.1),
                "mobility": UserSettableParameter('slider', 'Mobility', 6.0, 0.0, 10.0, 0.1)}

server = ModularServer(Covid, [virus_canvas, text_element, chart_element], "Covid-19 Model", model_params)
