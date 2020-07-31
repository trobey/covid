import numpy as np
import math

from mesa import Agent

class People(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        if self.model.imperial:
            self.home = np.array(pos)
            x = self.model.random.random() * self.model.space.x_max
            y = self.model.random.random() * self.model.space.y_max
            self.work = np.array((x, y))
            # 10% travel for work.
            self.travel = False
            if (100.0 * self.random.random() < 10.0):
                self.travel = True
            else:
                self.travel = False

    def step(self):
        if self.model.imperial:
            if self.model.state == "community" or (self.model.state == "work" and self.travel):
                x = self.model.random.random() * self.model.space.x_max
                y = self.model.random.random() * self.model.space.y_max
                new_pos = np.array((x, y))
            elif self.model.state == "work":
                angle = 360.0 * self.model.random.random();
                x = math.sin(angle);
                y = math.cos(angle)
                new_pos = self.work + np.array((x, y)) * self.model.random.random() * self.model.mobility
            else:
                angle = 360.0 * self.model.random.random();
                x = math.sin(angle);
                y = math.cos(angle)
                new_pos = self.home + np.array((x, y)) * self.model.random.random() * self.model.mobility
            
        else:
            angle = 360.0 * self.model.random.random();
            x = math.sin(angle);
            y = math.cos(angle)
            new_pos = self.pos + np.array((x, y)) * self.model.random.random() * self.model.mobility

        self.model.space.move_agent(self, new_pos)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Susceptible(People):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.name = "Susceptible"
        self.color = "Black"

    def step(self):
        super().step()

class Infected(People):
    def __init__(self, unique_id, model, pos, asymptomatic):
        super().__init__(unique_id, model, pos)
        self.name = "Infected"
        self.color = "Red"
        self.asymptomatic = asymptomatic
        if self.asymptomatic:
            self.energy = 42
        else:
            self.energy = 15

    def step(self):
        super().step()
        self.energy -= 1
        if self.energy == 0:
          person = Recovered(self.model.next_id(), self.model, self.pos)
          if self.model.imperial:
            person.set_imperial(self.home, self.work, self.travel)
          self.model.space.remove_agent(self)
          self.model.schedule.remove(self)
          self.model.space.place_agent(person, person.pos)
          self.model.schedule.add(person)

    def set_imperial(self, home, work, travel):
          self.home = np.array(home)
          self.work = np.array(work)
          self.travel = travel

class Recovered(People):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.name = "Recovered"
        self.color = "Green"

    def step(self):
        super().step()

    def set_imperial(self, home, work, travel):
          self.home = np.array(home)
          self.work = np.array(work)
          self.travel = travel
