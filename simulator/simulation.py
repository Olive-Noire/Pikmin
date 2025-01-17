from action import *

class Simulation:
    count = 0

    def __init__(self):
        Simulation.count += 1

        self._identifiant = Simulation.count

        self._actions_stack = []
        self._canceled_actions_stack = []
        self._entities = dict()
    
    def __del__(self):
        Simulation.count -= 1
    
    def get(self):
        return self._entities

    def execute_action(self, action):
        action.apply(self._entities)

    def save(file_path):
        pass

def load_simulation(file_path):
    pass

s = Simulation()
a = Action(0, [15, "caca"])
b = Action(0, [21, "skibidi"])

s.execute_action(a)
s.execute_action(b)
print(s.get())
s.execute_action(Action(1, [21]))
print(s.get())