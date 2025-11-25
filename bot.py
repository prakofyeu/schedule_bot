import os
from telegram import Bot, Update
from datetime import date, datetime, time
from crud import get_task_by_date, create_task, get_all_tasks
from dotenv import load_dotenv
from telegram.ext import ContextTypes, Application, CommandHandler

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)

async def send_schedule_for_day():
    today = date.today()
    tasks = await get_task_by_date(today)
    
    if not tasks:
        message = "сегодня задач нет"
    else:
        message = "Задачи на сегодня: \n\n"
        for task in tasks:
            message += f"Задача: {task.name}" + "\n"
            message += f"Время: {str(task.time)}"
            
    await bot.send_message(chat=CHAT_ID, text=message)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет я бот хранящий расписание.\n /today - расписание на сегодня, /add YYYY-MM-DD HH:MM TaskName - добавить задачу")
    

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today()
    tasks = await get_task_by_date(update.effective_user.id, today)
    
    if not tasks:
        message = "сегодня задач нет"
    else:
        message = "Задачи на сегодня: \n\n"
        for task in tasks:
            message += f"Задача: {task.name}" + "\n"
            message += f"Время: {str(task.time)}"
            
    await update.message.reply_text(message)
    
async def all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = await get_all_tasks(update.effective_user.id)
    
    if not tasks:
        message = "задач нет"
    else:
        message = "Задачи: \n\n"
        for task in tasks:
            message += f"Задача: {task.name}" + "\n"
            message += f"Время: {str(task.time)}"
            
    await update.message.reply_text(message)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3:
            await update.message.reply_text("Ты ввел не все данные ")
            return
        task_date, task_time= context.args[0], context.args[1]
        task_name = " ".join(context.args[2:])
        try:
            date = datetime.strptime(task_date, "%Y-%m-%d").date()
        except ValueError:
            await update.message.reply_text("Дата должна быть в формате YYYY-MM-DD")
            return
        
        try:
            task_time = time(int(task_time[:2]), int(task_time[3:]))
        except ValueError:
            await update.message.reply_text("Время должно быть в формате HH:MM")
            return
        
        await create_task(update.effective_user.id,date, task_time, task_name)
        await update.message.reply_text("Задача добавлена ")
    except Exception as e:
         await update.message.reply_text(f"Возникла ошибка {e}")

        
        
def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("today", today))  
    app.add_handler(CommandHandler("all", all_tasks)) 
    app.run_polling()