import asyncio

from config.config import bot, dp
from handlers import router
from utils.set_bot_commands import set_default_commands
from models import User, MiniCourse
from utils.mini_cuorce import Course
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


async def event_verification():
    users = await User.all()
    if users:
        for user in users:
            course = await MiniCourse.all(user_id=user.id)
            if course:
                if course[0].day_two:
                    await Course.day_two_start(user_id=user.id)
                elif course[0].day_three:
                    await Course.day_three_start(user_id=user.id)
                elif course[0].day_four:
                    await Course.day_four_start(user_id=user.id)
                elif course[0].day_five:
                    await Course.day_five_start(user_id=user.id)
                elif course[0].day_six:
                    await Course.day_six_start(user_id=user.id)
                elif course[0].day_seven:
                    await Course.day_seven_start(user_id=user.id)
                elif course[0].day_eight:
                    await Course.day_eight_start(user_id=user.id)
                    course[0].day_eight = False
                    course[0].finish = True
                    await course[0].save()


async def event_verification_two():
    users = await User.all()
    if users:
        for user in users:
            course = await MiniCourse.all(user_id=user.id)
            if course:
                if course[0].day_one:
                    course[0].day_one = False
                    course[0].day_two = True
                    await course[0].save()
                elif course[0].day_two:
                    await Course.day_two_end(user_id=user.id)
                    course[0].day_two = False
                    course[0].day_three = True
                    await course[0].save()
                elif course[0].day_three:
                    await Course.day_three_end(user_id=user.id)
                    course[0].day_three = False
                    course[0].day_four = True
                    await course[0].save()
                elif course[0].day_four:
                    await Course.day_four_end(user_id=user.id)
                    course[0].day_four = False
                    course[0].day_five = True
                    await course[0].save()
                elif course[0].day_five:
                    await Course.day_five_end(user_id=user.id)
                    course[0].day_five = False
                    course[0].day_six = True
                    await course[0].save()
                elif course[0].day_six:
                    await Course.day_six_end(user_id=user.id)
                    course[0].day_six = False
                    course[0].day_seven = True
                    await course[0].save()
                elif course[0].day_seven:
                    await Course.day_seven_end(user_id=user.id)
                    course[0].day_seven = False
                    course[0].day_eight = True
                    await course[0].save()
                elif course[0].day_eight:
                    course[0].day_eight = False
                    course[0].finish = True
                    await course[0].save()


async def start():
    dp.include_router(router=router)
    dp.startup.register(set_default_commands)
    scheduler = AsyncIOScheduler()

    scheduler.add_job(event_verification, trigger=CronTrigger(hour=5, minute=0))
    scheduler.add_job(event_verification_two, trigger=CronTrigger(hour=16, minute=0))

    scheduler.start()

    await bot.delete_webhook()
    try:
        await bot.send_message(540697966, "Бот успешно запущен и готов к работе!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
