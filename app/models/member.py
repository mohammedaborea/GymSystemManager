from sqlalchemy import Column ,Date, ForeignKey,Text,Integer , String , Boolean
from ..database import Base
from datetime import date,timedelta
from sqlalchemy.orm import relationship



class User(Base) : 
    __tablename__= "users"
    id = Column(Integer , primary_key=True , index=True)
    full_name=Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    role = Column(String,default="member")
    

class Offers(Base) :
    __tablename__= "offers"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    price = Column(Integer , nullable=False)
    duration_days = Column(Integer , nullable=False)
    descp = Column(Text,nullable=False)
    

class Membership(Base) :
    __tablename__ = "membership"
    id = Column(Integer , primary_key=True , index=True)
    offer_id = Column(Integer,ForeignKey("offers.id",ondelete="CASCADE",onupdate="CASCADE"),unique=True)
    user_id = Column(Integer , ForeignKey("users.id",ondelete="CASCADE",onupdate="CASCADE"),unique=True)
    start_date = Column(Date,default=date.today)
    end_date = Column(Date)
    duration_days_at_purchase = Column(Integer,nullable=False)
    def calculate_end_date(self):
        self.end_date = self.start_date + timedelta(days=self.duration_days_at_purchase)
  

class Payment(Base) :
    __tablename__ = "payment"
    id = Column(Integer , primary_key=True , index=True)
    membership_id = Column(Integer , ForeignKey("membership.id",ondelete="CASCADE",onupdate="CASCADE"))
    status = Column(String , nullable=False)
    paid_at = Column(Date,default=date.today)

class Offer_activities(Base) :
    __tablename__ = "offer_activities"
    offer_id = Column(Integer,ForeignKey("offers.id",ondelete="CASCADE",onupdate="CASCADE"),primary_key=True)
    activity_id = Column(Integer , ForeignKey("activities.id",ondelete="CASCADE" , onupdate="CASCADE"),primary_key=True)
    
class Activities(Base) :
    __tablename__ = "activities"
    id = Column(Integer , primary_key=True , index=True)
    name = Column(String , nullable=False)
    descp = Column(Text,nullable=False)
    
    

