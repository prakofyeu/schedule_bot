from sqlalchemy import String, Integer, Date, Column
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    time = Column(String, nullable=False)
    name = Column(String, nullable=False)
    