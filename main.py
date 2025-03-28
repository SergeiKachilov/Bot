import telebot
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
    bot.send_message(message.chat.id, f"Видно ||Не видно||", parse_mode="MarkdownV2")


@bot.message_handler(commands=["about"])
def send_welcome(message):
    bot.reply_to(message, "Бота сделал Сергей К., студент НТИ УРФУ")


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "/about - Информация об авторе\n/joke - Шутка\n/math - Случайное уравнение\n/rnd - случайное число\n\nРеши пример: (пример) - Решение мат. примера",
    )


@bot.message_handler(commands=["joke"])
def send_welcome(message):
    bot.send_message(message.chat.id, ParseJokes())


@bot.message_handler(commands=["math"])
def send_welcome(message):
    x = random.randint(0, 20)
    a = random.randint(1, 20)
    b = random.randint(1, 10)
    op = mathsOp[random.randint(0, len(mathsOp) - 1)]
    answer = eval(f"{a}*x{op}{b}")

    bot.send_message(
        message.chat.id,
        f"{a}x\\{op}{b}\\={answer}\n||Ответ: x \\= {x}||",
        parse_mode="MarkdownV2",
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
    else:
        bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
