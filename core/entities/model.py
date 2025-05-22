from dataclasses import dataclass

@dataclass
class Model:
    def __init__(self, id: int = None, name: str = None, cost: float = 0.0):
        self.id = id
        self.name = name
        self.cost = cost