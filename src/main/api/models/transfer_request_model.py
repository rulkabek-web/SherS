from src.main.api.models.base_model import BaseModel
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule

class TransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[float, CreationRule(min_float=500, max_float=10000)]