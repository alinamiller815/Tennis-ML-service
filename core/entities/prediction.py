from dataclasses import dataclass
from datetime import datetime

@dataclass
class Prediction:
    def __init__(self, id: int = None, user_id: int = None, model_id: int = None,
                 input_data: str = None, output_data: str = None, 
                 created_at: datetime = None):
        self.id = id
        self.user_id = user_id
        self.model_id = model_id
        self.input_data = input_data
        self.output_data = output_data
        self.created_at = created_at if created_at else datetime.utcnow()

    