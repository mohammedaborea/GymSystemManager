from typing import Generic , TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ErrorResponse(BaseModel) :
    code : str 
    message : str
    field : str | None = None

class StandardResponse(BaseModel , Generic[T]) :
    success : bool 
    data : T | None = None 
    message : str 
    error : ErrorResponse | None = None