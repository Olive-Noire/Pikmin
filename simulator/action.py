def add(identifiant, ent, entities):
    entities[identifiant] = ent

def remove(identifiant, entities):
    del entities[identifiant]

callbacks = (
[
    add,
    remove
])

class Action:
    def __init__(self, action_type, arguments):
        self._type = action_type
        self._arguments = arguments
    
    def apply(self, entities):
        callbacks[self._type](*self._arguments, entities)
