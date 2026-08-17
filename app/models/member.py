from sqlalchemy import Column ,Date, ForeignKey,Text,Integer , String , Boolean,Enum,Time
from ..database import Base
from datetime import date,timedelta
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
class User(Base) : 
    __tablename__= "users"
    id = Column(Integer , primary_key=True , index=True)
    full_name=Column(String,nullable=False)
    phone_number = Column(Integer , nullable=False)
    email = Column(String,unique=True,nullable=False)
    status = Column(
        Enum("active", "inactive","expired", name="user_status"),
        nullable=False,
        default="active"
    )
    notes = Column(Text)
    
    

    

    



class Member(Base) :

    __tablename__ = "member"
    id = Column(Integer,primary_key=True)
    member_id = Column(Integer , ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE") , unique=True)
    joined_at = Column(Date)
    expiry_date = Column(Date)
    user = relationship("User")
    fitness_goal_id = Column(Integer,ForeignKey("fitness_goal.id",ondelete="CASCADE",onupdate="CASCADE"))
    fitness = relationship("Fitness")
    membership_id = Column(Integer,ForeignKey("membership.id",ondelete="CASCADE",onupdate="CASCADE"))
    membership = relationship("Membership")


class Trainer(Base):
    __tablename__ = "trainer"

    id = Column(Integer,primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    monthly_salary = Column(Integer)
    hire_date = Column(Date, nullable=False)

    user = relationship("User")

    schedules = relationship(
        "Schedule",
        back_populates="trainer",
        cascade="all, delete-orphan"
    )
    mark_att = relationship("MarkAttendance" , back_populates="trainer")
    


class MarkAttendance(Base) :
    __tablename__ = "mark_attendance"
    trainer_id = Column(Integer , ForeignKey("trainer.id",ondelete="CASCADE",onupdate="CASCADE"),primary_key=True)
    attendance_id = Column(Integer , ForeignKey("attendance.id",ondelete="CASCADE",onupdate="CASCADE"))
    date_att = Column(Date,default=date.today,primary_key=True)
    check_in = Column(Time)
    check_out = Column(Time)
    notes = Column(Text)
    trainer = relationship("Trainer" , back_populates="mark_att")
    attendance = relationship("Attendance", back_populates="mark_att")
class Attendance(Base) :
    __tablename__ = "attendance"
    id = Column(Integer ,primary_key=True)
    status = Column(String,nullable=False)
    mark_att = relationship("MarkAttendance",back_populates="attendance")

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)

    trainer_id = Column(
        Integer,
        ForeignKey("trainer.id", ondelete="CASCADE"),
        nullable=False
    )

    date_schedule = Column(Date, nullable=False)
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
    

    
    

