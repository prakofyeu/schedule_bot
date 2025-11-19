from sqlalchemy.future import select
from database import SessionLocal
from models import Task

async def create_task(date, time, name):
    async with SessionLocal() as session:
        new_task = Task(date=date, time=time, name=name)
        session.add(new_task)
        await session.commit()
        
async def get_task_by_date(date):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.date == date))
        print(result)
        return result.scalars().all()
        