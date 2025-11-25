from sqlalchemy import String, Integer, Date, Column, Time
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, index=True)
    time = Column(Time, nullable=False)
    name = Column(String, nullable=False)
    