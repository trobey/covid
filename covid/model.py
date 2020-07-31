'''
Covid-19
=============================================================
A Mesa implementation of a coronavirus SIR model on a continuous space.
'''

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from .agents import Susceptible, Infected, Recovered


class Covid(Model):
    '''
    Covid model class. Handles agent creation, placement and scheduling.
    '''

    def __init__(self,
                 population=100,
                 width=100,
                 height=100,
                 mobility=6,
                 social_distance=2,
                 asymptomatic_percentage=50.0,
                 imperial=True):
        '''
        Create a new Covid model.

        Args:
            population: Number of people (density) with one asymptomatic infected person.
            imperial: Agent rotates between home, work and community.  For home the agent returns to a random point near a fixed home position.  Community has the agent randomly placed in the space.  Work has 90% like home but with a fixed work position and 10% random like community.  This is patterned after the Imperial College model.  Turning off imperial iterates with each agent traveling a random direction and distance from the current position.
            asymptomatic_percentage: Percentage of infected people that are asymptomatic.  Asymptomatic people transmit the virus for 42 time steps versus 15 time steps for those that are symptomatic.
            social_distance: Distance at which neighboring susceptible agents can b ecome infected.
            mobility: The maximum distance that an agent can travel.
        '''

        self.current_id = 0;
        self.population = population
        self.mobility = mobility
        self.social_distance = social_distance
        self.asymptomatic_percentage = asymptomatic_percentage
        self.imperial = imperial
        if imperial:
            self.state = "home"
        else:
            self.state = "diffusion"
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.make_agents()
        self.running = True

        self.datacollector = DataCollector(
            {"Susceptible": lambda m: self.count("Susceptible"),
             "Infected": lambda m: self.count("Infected"),
             "Recovered": lambda m: self.count("Recovered"),
             "Symptomatic": lambda m: self.active("symptomatic"),
             "Asymptomatic": lambda m: self.active("asymptomatic")})

    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''

        for i in range(0, 1):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            asymptomatic = True
            person = Infected(self.next_id(), self, pos, asymptomatic)
            self.space.place_agent(person, pos)
            self.schedule.add(person)

        for i in range(self.population - 1):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            person = Susceptible(self.next_id(), self, pos)
            self.space.place_agent(person, pos)
            self.schedule.add(person)

    def step(self):
        self.infect()

        if self.state == "home":
            self.state = "work"
        elif self.state == "work":
            self.state = "community"
        elif self.state == "community":
            self.state = "home"

        self.schedule.step()

        # collect data
        self.datacollector.collect(self)
        if self.count("Infected") == 0:
          self.running = False

    def infect(self):
        agent_keys = list(self.schedule._agents.keys())
        susceptible = [];
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == "Susceptible":
                susceptible.append(agent_key)
        for agent_key in susceptible:
            agent = self.schedule._agents[agent_key]
            neighbors = self.space.get_neighbors(agent.pos, self.social_distance)
            for neighbor in neighbors:
                if neighbor.name == "Infected":
                    asymptomatic = False
                    if (100.0 * self.random.random() < self.asymptomatic_percentage):
                        asymptomatic = True
                    person = Infected(self.next_id(), self, agent.pos, asymptomatic)
                    if self.imperial:
                        person.set_imperial(agent.home, agent.work, agent.travel)
                    self.space.remove_agent(agent)
                    self.schedule.remove(agent)
                    self.space.place_agent(person, person.pos)
                    self.schedule.add(person)
                    break

    def count(self, type):
        agent_keys = list(self.schedule._agents.keys())
        num = 0
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == type:
                num += 1
        return num

    def active(self, type):
        agent_keys = list(self.schedule._agents.keys())
        num = 0
        for agent_key in agent_keys:
            if self.schedule._agents[agent_key].name == 'Infected':
                if type == 'asymptomatic':
                    if self.schedule._agents[agent_key].asymptomatic:
                        num += 1
                else:
                    if not self.schedule._agents[agent_key].asymptomatic:
                        num += 1
        return num

