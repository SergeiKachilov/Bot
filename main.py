import telebot
from telebot import types
from config import TG_API_TOKEN
import random
import requests
import re

jokes = [
    "Настоящий мужчина хочет только одного — стать достаточно богатым, чтобы просто играть в компьютере.",
    "Представьте себе, как трудно будет нашим детям лет через 20 придумать свободное имя пользователя.",
    "Сейчас мама сказала:\n— Да ты скоро с ноутбуком в туалет ходить будешь! Видимо она еще не в курсе…",
    "Пользователям на заметку. Ваша клавиатура прослужит значительно дольше, если перед ее использованием вылечить нервы…",
    "Чисто прибранная квартира и вкусный ужин — это два признака неисправного компьютера.",
    "Медленный компьютер это когда ты знаешь имена всех разработчиков Adobe Photoshop.",
]

LINK_JOKES = "https://www.anekdot.ru/tags/программист/1?type=anekdots"


def math(res):
    if not res:
        global x
        x = random.randint(0, 20)
        a = random.randint(1, 20)
        b = random.randint(1, 10)
        op = mathsOp[random.randint(0, len(mathsOp) - 1)]
        answer = eval(f"{a}*x{op}{b}")

        x1 = x
        x2 = x
        x3 = x

        while x1 == x or x2 == x or x3 == x or x1 == x2 or x1 == x3 or x2 == x3:
            if x1 == x:
                x1 = random.randint(0, 20)
            if x2 == x or x2 == x1:
                x2 = random.randint(0, 20)
            if x3 == x or x3 == x1 or x3 == x2:
                x3 = random.randint(0, 20)

        mathematics = [a, op, b, answer, [x, x1, x2, x3]]
        return mathematics
    else:
        return x


def ParseJokes():
    page = 1
    link = f"https://www.anekdot.ru/tags/программист/{page}?type=anekdots"
    html = requests.get(link).text
    maxPage = int(
        re.findall(
            r"<a href=\"/tags.+\">(\d+)</a>",
            html,
        )[0]
    )

    page = random.randint(1, maxPage)

    html = requests.get(link).text

    joke = random.choice(
        re.findall(r"<div class=\"text\">([\w\s,.<>\-\?:!\"—+«»–()]+)", html)
    ).rstrip("<")

    if "<br>" in joke:
        joke = joke.replace("<br>", "\n")

    return joke


mathsOp = ["+", "-", "*"]

bot = telebot.TeleBot(TG_API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Привет")
    button2 = types.KeyboardButton("Как дела?")
    button3 = types.KeyboardButton("Пока")

    markup.add(button1, button2, button3)

    bot.send_message(
        message.chat.id,
        f"Привет {message.from_user.first_name}, я тестовый бот!",
        reply_markup=markup,
    )


@bot.message_handler(commands=["about"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("ВК", url="https://nti.urfu.ru/")
    markup.add(button1)

    bot.send_message(
        message.chat.id,
        "Бота сделал Сергей К., студент НТИ УРФУ".format(message.from_user),
        reply_markup=markup,
    )


@bot.message_handler(commands=["help"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btnAbout = types.InlineKeyboardButton("/about", callback_data="about")
    btnJoke = types.InlineKeyboardButton("/joke", callback_data="joke")
    btnMath = types.InlineKeyboardButton("/math", callback_data="math")
    btnRnd = types.InlineKeyboardButton("/rnd", callback_data="rnd")

    markup.add(btnAbout, btnJoke, btnMath, btnRnd)
    bot.send_message(
        message.chat.id,
        "О какой комаде хотите получить информацию?",
        reply_markup=markup,
    )


@bot.message_handler(commands=["joke"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btnReply = types.InlineKeyboardButton("Reply", callback_data="reply")
    markup.add(btnReply)
    try:
        bot.send_message(message.chat.id, ParseJokes(), reply_markup=markup)

    except:
        bot.send_message(message.chat.id, random.choice(jokes), reply_markup=markup)


@bot.message_handler(commands=["math"])
def send_welcome(message):
    m = math(False)
    x = m[4][0]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = random.choice(m[4])
    m[4].remove(b1)
    b2 = random.choice(m[4])
    m[4].remove(b2)
    b3 = random.choice(m[4])
    m[4].remove(b3)
    b4 = random.choice(m[4])
    m[4].remove(b4)

    btn1 = types.KeyboardButton(f"x = {b1}")
    btn2 = types.KeyboardButton(f"x = {b2}")
    btn3 = types.KeyboardButton(f"x = {b3}")
    btn4 = types.KeyboardButton(f"x = {b4}")

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(
        message.chat.id,
        f"{m[0]}x\\{m[1]}{m[2]}\\={m[3]}\n||Ответ: x \\= {x}||",
        parse_mode="MarkdownV2",
        reply_markup=markup,
    )


@bot.message_handler(commands=["rnd"])
def echo_all(message):
    bot.reply_to(message, random.randint(0, 100))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Хай")
    elif message.text.lower() == "пока":
        bot.send_message(message.chat.id, "Аривидерчи")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Норм")
    elif "Реши пример: " in message.text:
        bot.send_message(
            message.chat.id, eval(message.text.replace("Реши пример: ", ""))
        )
    elif "x = " in message.text:
        markup = types.ReplyKeyboardMarkup()
        markup.add()
        if int(message.text.replace("x = ", "")) == math(True):
            bot.send_message(message.chat.id, "Ответ верный!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ответ неверный!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda c: True)
def help(c):
    if c.data == "about":
        bot.send_message(c.message.chat.id, "/about - Информация о разработчике")
    elif c.data == "joke":
        bot.send_message(c.message.chat.id, "/joke - Анекдот на тему программистов")
    elif c.data == "math":
        bot.send_message(c.message.chat.id, "/math - Генерация уравнения")
    elif c.data == "rnd":
        bot.send_message(c.message.chat.id, "/rnd - Случайное число от 0 до 100")
    elif c.data == "reply":
        markup = types.InlineKeyboardMarkup()
        btnReply = types.InlineKeyboardButton("Reply", callback_data="reply")
        markup.add(btnReply)
        try:
            bot.send_message(c.message.chat.id, ParseJokes(), reply_markup=markup)

        except:
            bot.send_message(
                c.message.chat.id, random.choice(jokes), reply_markup=markup
            )


bot.infinity_polling()
