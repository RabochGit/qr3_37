import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6461773683:AAHShlO-2XVviou-k-ygSi919yzgD9XOnbc",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "тык"
text_button_1 = "ВАРИАНТЫ 80-90-Х(зарубежные)"
text_button_2 = "РЕЛАКС(good night)"
text_button_3 = "НА МОЙ ВКУС(неоклассика)"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привеет, милый друг! Как ты? Готов покорять вершины? (знаю, что готов) Чем поинтересуешься сегодня? 🙂',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Мне нравится ход твоих мыслей! *Ваше* _имя_?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Какое красивое имя! [Ваш](https://www.example.com/) возраст?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за ответы, приятно познакомиться, dear friend!', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Ссылка](https://www.youtube.com/watch?v=3JWTaaS7LdU&list=PL9jFdX20KVfyJnL9-3FejPa8sKohmOXsX)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Ссылка](https://www.youtube.com/watch?v=k7XqU_BrXbQ&pp=ygVA0YHQv9C-0LrQvtC50L3QsNGPINCy0LDQudCx0L7QstCw0Y8g0LzRg9C30YvQutCwINCx0LXQtyDRgdC70L7Qsg%3D%3D)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Ссылка](https://www.youtube.com/watch?v=q5PjWMqaujc&pp=ygUW0L3QtdC-0LrQu9Cw0YHRgdC40LrQsA%3D%3D)", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()