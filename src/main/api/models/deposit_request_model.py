from src.main.api.models.base_model import BaseModel
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule

class DepositRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(min_float=1000, max_float=9000)]