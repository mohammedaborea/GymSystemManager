from sqlalchemy import Column ,Date, ForeignKey,Text,Integer , String , Boolean,Enum,Time
from ..database import Base
from datetime import date,timedelta
from sqlalchemy.orm import relationship


class User(Base) : 
    __tablename__= "users"
    id = Column(Integer , primary_key=True , index=True)
    full_name=Column(String,nullable=False)
    phone_number = Column(Integer , nullable=False)
    email = Column(String,nullable=False)
    
    status = Column(
        Enum("active", "inactive","expired", name="user_status"),
        nullable=False,
        default="active"
    )
    notes = Column(Text)
    
    
    role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE",onupdate="CASCADE"))
    role = relationship("Role")
    
class Role(Base) : 
    __tablename__ = "roles"
    id = Column(Integer , primary_key=True)
    pseudo = Column(String , nullable=False)
    

    



class Member(Base) :

    __tablename__ = "member"
    member_id = Column(Integer , ForeignKey("users.id") , primary_key=True)
    joined_at = Column(Date)
    expiry_date = Column(Date)
    user = relationship("User")
    fitness_goal_id = Column(Integer,ForeignKey("fitness_goal.id",ondelete="CASCADE",onupdate="CASCADE"))
    fitness = relationship("Fitness")
    membership_id = Column(Integer,ForeignKey("membership.id",ondelete="CASCADE",onupdate="CASCADE"))
    membership = relationship("Membership")


class Trainer(Base):
    __tablename__ = "trainer"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    monthly_salary = Column(Integer)
    hire_date = Column(Date, nullable=False)

    user = relationship("User")

    schedules = relationship(
        "Schedule",
        back_populates="trainer",
        cascade="all, delete-orphan"
    )


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)

    trainer_id = Column(
        Integer,
        ForeignKey("trainer.user_id", ondelete="CASCADE"),
        nullable=False
    )

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    zone = Column(String)
    notes = Column(Text)

    trainer = relationship(
        "Trainer",
        back_populates="schedules"
    )

class Membership(Base) :
    __tablename__= "membership"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    

class Fitness(Base) : 
    __tablename__ = "fitness_goal"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    

    
    

