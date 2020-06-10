import numpy as np
import math

from mesa import Agent

class Susceptible(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.name = "Susceptible"
        self.color = "Black"
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

class Infected(Agent):
    def __init__(self, unique_id, model, pos, asymptomatic):
        super().__init__(unique_id, model)
        self.name = "Infected"
        self.color = "Red"
        self.pos = np.array(pos)
        self.asymptomatic = asymptomatic
        if self.asymptomatic:
            self.energy = 42
        else:
            self.energy = 15
        if self.model.imperial:
            self.home = np.array(pos)
            x = self.model.random.random() * self.model.space.x_max
            y = self.model.random.random() * self.model.space.y_max
            self.work = np.array((x, y))
            # 10% travel for work.
            if (100.0 * self.random.random() < 10.0):
                self.travel = True
            else:
                self.travel = False

    def step(self):
        '''
        Get the Infected person's neighbors, compute the new vector, and move accordingly.
        '''
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

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Recovered(Agent):
    def __init__(self, unique_id, model, pos, imperial=True):
        super().__init__(unique_id, model)
        self.name = "Recovered"
        self.color = "Green"
        self.pos = np.array(pos)

    def step(self):
        '''
        Get the Infected person's neighbors, compute the new vector, and move accordingly.
        '''
        if self.model.imperial:
            if self.model.state == "community":
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
    def set_imperial(self, home, work, travel):
          self.home = np.array(home)
          self.work = np.array(work)
          self.travel = travel

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
