from pydantic import BaseModel,ConfigDict

class MembershipCreate(BaseModel) :
    name : str
    
class MembershipModify(BaseModel) : 
    name : str | None = None