from ..database import Base
from sqlalchemy import Column , Date,Time,DateTime,ForeignKey,Integer , Text,String , Boolean
from sqlalchemy.orm import relationship

from datetime import datetime

class Trainer(Base) :
    __tablename__="trainers"
    user_id = Column(Integer , ForeignKey("users.id") , primary_key=True)
    experience = Column(String)
    bio = Column(Text , nullable=False)
    user = relationship("User")
    
    

class Trainer_activity(Base) : 
    __tablename__="trainers_activities"
    id = Column(Integer , primary_key=True)
    Trainer_id = Column(Integer , ForeignKey("trainers.user_id",ondelete="CASCADE",onupdate="CASCADE"),unique=True)
    activity_id = Column(Integer , ForeignKey("activities.id",ondelete="CASCADE",onupdate="CASCADE"),unique=True)
    salary = Column(Integer)
    room_id = Column(Integer , ForeignKey("rooms.id",ondelete="CASCADE",onupdate="CASCADE"))
    
    
    
class Room(Base) : 
    __tablename__ = "rooms"
    id = Column(Integer , primary_key=True)
    pseudo = Column(String , nullable=False)


class Sessions(Base) :
    __tablename__ = "sessions"
    id = Column(Integer , primary_key=True)
    trainer_activity_id = Column(Integer , ForeignKey("trainers_activities.id",ondelete="CASCADE",onupdate="CASCADE"))
    day = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    capacity = Column(Integer)
    

