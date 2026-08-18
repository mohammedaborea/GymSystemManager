from pydantic import BaseModel,ConfigDict

class MembershipCreate(BaseModel) :
    id : int
    name : str
    
class MembershipModify(BaseModel) : 
    
    name : str | None = None