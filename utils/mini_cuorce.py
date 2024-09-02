from aiogram import types
from aiogram.types import CallbackQuery
from config.config import bot
from keyboards.inline import main_menu_ikb, answer_for_user_ikb
from keyboards.inline.general import UserCallbackData
from utils.queue import queue
from models.models import User, Dialog


class Course(object):

    @staticmethod
    async def start(callback: CallbackQuery, callback_data: UserCallbackData):

        text = ('Наша команда рада видеть тебя на мини-курсе "Эмоциональное выгорание: восстановление и баланс"\n\n'
                '👉 У тебя будет свой личный куратор, поэтому можно задавать любые вопросы!\n\n'
                '💥 Твое сильное желание изменить свое состояние - это уже 50% успеха,'
                ' поэтому выполняй домашние задания и мы вместе отпразднуем твой результат!\n\n'
                '👉 Уже сегодня тебе будет доступен День 1: теория и домашнее задание!')

        # photo = types.FSInputFile("media/min.jpg")
        photo = types.FSInputFile("/opt/git/Eco_bot_tg/media/min.jpg")

        await callback.message.answer_photo(
            photo=photo,
            caption=text
        )

        text_day1 = ("ДЕНЬ - 1\n"
                     "✅ Введение\n\n"
                     "•узнаешь , где  взять энергию для  жизни\n"
                     "• поймешь как улучшить состояния уже сегодня\n"
                     "• бонус- трекер привычек\n"
                     "• узнаешь, как забрать подарок после прохождения мини-курса\n"
                     "• поймешь алгоритм работы привычки\n"
                     "• вместе пропишем цель на мини-курс\n"
                     "• получишь ссылки на приложения для удобства внедрения новых привычек\n"
                     "📚 Домашнее задание\n\n")

        text_day2 = ("ДЕНЬ - 2\n"
                     "✅ Правильный перекус\n\n"
                     "• правильное питание это не про диеты\n"
                     "• в чем сила ПП?\n"
                     "• какие шаги можно сделать  для получения результата\n"
                     "•  разберемся - едим чтобы жить, или живем чтобы есть\n"
                     "•дефициты - как восполнить\n"
                     "📚 Домашнее задание\n\n")

        text_day3 = ("ДЕНЬ - 3\n"
                     "✅ Питьевой режим\n\n"
                     "• что значит вода для организма\n"
                     "• тест- достаточно ли ты пьешь воды\n"
                     "• норма воды в мл/л в сутки\n"
                     "📚 Домашнее задание\n\n")

        text_day4 = ("ДЕНЬ - 4\n"
                     "✅ Физическая активность\n\n"
                     "• в чем твой успех? в постоянстве\n"
                     "• симптомы гиподинамии, как с ней справиться?\n"
                     "• одно упражнение которое заменит 30 минутную тренировку\n"
                     "📚 Домашнее задание\n\n")

        text_day5 = ("ДЕНЬ - 5\n"
                     "✅ Качественный сон\n\n"
                     "• сон и его влияние на психическое равновесие\n"
                     "•жизнь без стресса -можно!\n"
                     "• разберем важные аспекты  здорового сна\n"
                     "• с чего начать в улучшении своего сна\n"
                     "• что изменится в состоянии\n"
                     "📚 Домашнее задание\n\n")

        text_day6 = ("ДЕНЬ 6 - Бонусный день\n"
                     "✅Расслабление\n\n"
                     "• как расслабление помогает быть здоровым\n"
                     "• покой нам только снится"
                     "• как понять, что ты в эмоциональной ловушке\n"
                     "• как понять что силы на исходе\n"
                     "• 🎁 бонус - способы расслабления\n"
                     "📚 Домашнее задание\n\n")

        text_day7 = ("ДЕНЬ 7"
                     "✅ Подведение итогов\n\n"
                     "• начало пути определяет первый шаг\n"
                     "• твой трекер привычек, твой лучший друг\n"
                     "• ты - это твои привычки\n"
                     "📚 Домашнее задание\n\n")

        text_gift = ("🎁 ПОДАРОК для тех, кто прошел мини-курс до конца\n\n"
                     "• как получить подарок (см. День 7)\n"
                     "• бонус - консультация специалиста по балансу белков жиров и углеводов")

        text_dop = ("<b>Для большей эффективности направляю тебя на личного куратора.</b> \n\n"
                    "Он пришлет тебе дополнительные индивидуальные доступы к материалам"
                    " и ответит на все твои вопросы")

        # photo_one = types.FSInputFile("media/onemini.jpg")
        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/onemini.jpg")

        await callback.message.answer_photo(
            photo=photo_one,
            caption=f"{text_day1} {text_day2} {text_day3} {text_day4}"
        )

        await callback.message.answer(
            text=f"{text_day5} "
                 f"{text_day6} {text_day7} {text_gift}"
        )

        await callback.message.answer(
            text=f"{text_dop}",
            reply_markup=await main_menu_ikb()
        )

        # document = FSInputFile('files/mini_course/Мини-курс день 1.pdf')
        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 1.pdf")

        await callback.message.answer_document(
            document=document,
            caption="Мини-курс день 1"
        )

        send_text = "начал мини-курс, нужно выслать опрос."

        callback_data.user_id = callback.from_user.id
        callback_data.details = send_text

        await queue(callback=callback, callback_data=callback_data)

    @staticmethod
    async def day_two_start(user_id: int):
        text = ("Доброе утро ☀️\n\n"
                "<b>Важно понимать, что привычки имеют огромное влияние на наше здоровье.</b>\n\n"
                "Сегодня мы начинаем углубленно разбираться в этой теме.\n\n"
                "Если ты ещё не посмотрел День 1, приятного тебе просмотра\n\n"
                "<b>🌿 Мудрость дня:</b> А теперь давайте встретим новый день, "
                "полный событий, которых никогда не было!")

        # photo_one = types.FSInputFile("media/p2.png")
        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p2.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_two_end(user_id: int):
        text = ("Добрый вечер 💫\n\n"
                "<b>Уверены, что тебе уже удалось изучить День 1 мини-курса - Введение!</b>\n\n"
                "Если ты еще не сделал (а) этого, поторопись 😊 пока открыт доступ!\n\n"
                "Поздравляю 🌺\n\n"
                "Тебе открыт доступ к День 2 мини-курса\n\n"
                "Уже завтра ты приступишь к практическим занятиям!\n"
                "До встречи 👋")

        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 2.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 2"
        )

    @staticmethod
    async def day_three_start(user_id: int):
        text = ("Доброе утро ☀️\n\n"
                "Сегодня тебя ждёт увлекательное путешествие в мир полезностей!\n\n"
                "Желаем тебе плодотворного дня и ждём на День 2 мини-курса, второй урок уже открыт 😉!!!\n"
                "Приятного просмотра.\n\n"
                "<b>🌿 Мудрость дня:</b> Никогда не недооценивай силу, которой ты обладаешь, "
                "чтобы направить свою жизнь в новое русло!")

        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p3.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_three_end(user_id: int):
        text = ("Добрый вечер 💫\n\n"
                "<b>Помни, что здоровье начинается с того, ЧТО мы едим.</b>\n\n"
                "Как твои впечатления от урока о правильном перекусе и питании?\n\n"
                "Открываю доступ к следующему дню мини-курса.\n\n"
                "До встречи завтра👋")

        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 3.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 3"
        )

    @staticmethod
    async def day_four_start(user_id: int):

        text = ("Доброе утро ☀️\n\n"
                "<b>Вода – ключ к хорошему настроению и самочувствию. "
                "Сегодня разбираемся почему это так важно!!!</b>\n"
                "<b>Приятного погружения в полезное чтиво!</b>\n\n"
                "Не забудь отметить свои победы в Трекер привычек!\n"
                "Хорошего дня!\n\n"
                "<b>🌿 Мудрость дня:</b> Начало - самая важная часть работы!")

        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p4.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_four_end(user_id: int):
        text = ("Добрый вечер 💫\n\n"
                "Как прошел день с вниманием к питьевому режиму?!\n"
                "<b>Самое интересное, что как только ты будешь потреблять достаточное "
                "количество воды, почувствуешь изменения в состоянии.</b>\n\n"
                "Тебе совсем скоро будет открыт доступ к следующему уроку!\n"
                "Спойлер: движение – жизнь😉")
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 4.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 4"
        )

    @staticmethod
    async def day_five_start(user_id: int):
        text = ("Доброе утро ☀️\n\n"
                "<b>Новый день — сотня новых возможностей наполнить свою жизнь и жизнь близких счастьем. "
                "Сегодня этим и займемся!</b>\n"
                "Начните с себя. У вас есть уже в доступе 4 урока, воспользуйтесь ими, чтобы наполниться энергией, "
                "а потом подарите капельку энергии близким, сделав что-то приятное для них.\n\n"
                "Не забывайте отмечать свои победы в Трекер привычек ЕЖЕДНЕВНО!\n"
                "Солнечного во всех смыслах дня!\n\n"
                "<b>🌿 Мудрость дня:</b> Хотя никто не может вернуться назад и начать все с начала, "
                "но каждый может начать с этого момента и закончить все по-новому!")

        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p5.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_five_end(user_id: int):
        text = ("Доброго вечера 💫\n\n"
                "Завтра тебя ждёт очень полезный урок.<b>Как же часто люди пренебрегаю качественным "
                "сном – потом высплюсь. Сон очень сказывается на нашем общем состоянии!</b> И организм "
                "отвечает тем, что с утра мы уже устали не успев сесть за работу. Будем восполнять пробелы!\n\n"
                "Лови, тебе открыт доступ к следующему уроку!")
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 5.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 5"
        )

    @staticmethod
    async def day_six_start(user_id: int):
        text = ("Доброе утро ☀️\n\n"
                "Как прошла ночь?\n"
                "Есть ли у тебя вопросы к качественному сну?! Сегодня ты сможешь узнать и проверить это на себе. "
                "И конечно же ты получишь очень полезную информацию как помочь себе 😉.\n\n"
                "<b>Погрузись в материал и подари своему уму и телу заслуженный отдых!</b>\n\n"
                "<b>🌿 Мудрость дня:</b> Ваша жизнь не становится лучше случайно. "
                "Она становится лучше благодаря переменам!")

        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p6.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_six_end(user_id: int):
        text = ("Добрый вечер 💫\n\n"
                "Завтра тебя ждет БОНУСНЫЙ ДЕНЬ - ты погрузишься в релакс.\n"
                "Мы расскажем тебе как важно расслабляться!!!\n\n"
                "🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️🧘‍♀️")
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 6.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 6"
        )

    @staticmethod
    async def day_seven_start(user_id: int):
        text = ("Доброе утро ☀️\n\n"
                "Расслабься, наслаждайся и готовься к завершению нашего увлекательного путешествия!\n\n"
                "В твоем Трекере отмечены все твои новые победы. Мы гордимся, что с нами ты меняешься😉\n\n"
                "<b>🌿 Мудрость дня:</b> Как только у вас появилась решимость, "
                "вам нужна дисциплина и упорный труд, чтобы добиться этого!")

        photo_one = types.FSInputFile("/opt/git/Eco_bot_tg/media/p7.png")

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_one,
            caption=f"{text}",
            parse_mode="HTML"
        )

    @staticmethod
    async def day_seven_end(user_id: int):
        text = ("Добрый вечер 💫\n\n"
                "Даже немного грустно, что подходит к концу этот мини-курс!\n\n"
                "Сегодня я открою тебе доступ к заключительному дню.\n"
                "<b>Проделана большая работа нашей команды - мы щедро поделились с тобой опытом и, конечно, "
                "же твоя - ты выполнял все задания и начал новый путь к изменениям своего состояния!</b>")
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        document = types.FSInputFile("/opt/git/Eco_bot_tg/files/mini_course/Мини-курс день 7.pdf")

        await bot.send_document(
            chat_id=user_id,
            document=document,
            caption="Мини-курс день 7"
        )

    @staticmethod
    async def day_eight_start(user_id: int, callback_data: UserCallbackData = None):
        text = ("Доброе утро ☀️\n\n"
                "Все неслучайно в этой жизни и здесь ты неслучайно!\n\n"
                "Поздравляю с завершением нашего 7-дневного мини-курса!\n"
                "Какие изменения ты заметил в своей жизни?\n"
                "<b>Новые привычки - это новая жизнь.</b>\n\n"
                "Сегодня подведем итоги и откроемся более здоровому и сбалансированному образу жизни!\n\n"
                "Твой личный куратор пришлет тебе "
                "<b>индивидуальный доступ</b> к опросу и ПОСЛЕ ЭТОГО МЫ ПРИШЛЕМ ТЕБЕ САМЫЙ  🎁🎁🎁 НАСТОЯЩИЙ ПОДАРОК!\n\n"
                "<b>🌿 Мудрость дня:</b> Если это важно для вас, то вы найдете способ. "
                "Если нет, вы найдете оправдание!")
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )

        if callback_data is None:
            callback_data = UserCallbackData(
                target="Mini_course",
                user_id=user_id

            )

        user = await User.get(pk=user_id)
        user_dialogs = await Dialog.all(user_id=user.id)

        for user_dialog in user_dialogs:
            if user_dialog and user_dialog.manager_id:
                admin = await User.get(pk=user_dialog.manager_id)
                callback_data.user_id = user.id
                callback_data.dialog_id = user_dialog.id

                await bot.send_message(
                    chat_id=admin.id,
                    text=f"Пользователь @{user.tg_username} ({user.tg_first_name} {user.tg_username})\n"
                         f"завершил мини-курс, нужно выслать опрос",
                    reply_markup=await answer_for_user_ikb(callback_data=callback_data)
                )
