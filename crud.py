from sqlalchemy.future import select
from database import SessionLocal
from models import Task

async def create_task(user_id, date, time, name):
    async with SessionLocal() as session:
        new_task = Task(user_id=user_id, date=date, time=time, name=name)
        session.add(new_task)
        await session.commit()
        
async def get_task_by_date(user_id, date):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.date == date, Task.user_id == user_id))
        return result.scalars().all()
   
    
async def get_all_tasks_by_date(date):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.date == date))
        return result.scalars().all()
    


async def get_all_tasks(user_id):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.user_id == user_id).order_by(Task.date, Task.time))
        return result.scalars().all()