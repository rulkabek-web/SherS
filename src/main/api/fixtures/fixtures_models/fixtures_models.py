from typing import TypedDict, Any
from pydantic import BaseModel


class AccountData(TypedDict):
    id: int
    create_user_request: BaseModel

class RequestsData(TypedDict):
    Any: BaseModel
    create_user_request: BaseModel