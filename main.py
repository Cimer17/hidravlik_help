import telebot
import os
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")
tokenBot = config["bot"]["bot_token"]


bot = telebot.TeleBot(tokenBot)
list_menu = ['Дроссели', 'МногомассовыеСилы', 'РГР']


def generator_keyboards(ListNameBTN, NumberColumns = 2):
    keyboards = telebot.types.ReplyKeyboardMarkup(row_width=NumberColumns, resize_keyboard=True)
    btn_names = [telebot.types.KeyboardButton(text=x) for x in ListNameBTN]
    keyboards.add(*btn_names)
    return keyboards


def clean_name(item):
    return item[:-4]


def variant(message, type_work):
    photo = open(f'img/{type_work}/{message.text}.png', 'rb')
    bot.send_document(message.chat.id, photo, caption='Ваше решение:', reply_markup=generator_keyboards(list_menu))


@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, 'Выберите задание:', reply_markup=generator_keyboards(list_menu))


@bot.message_handler(func= lambda m : m.text)
def generator(message):
    text = message.text
    if text in list_menu:
        photo = open(f'img/{text}.png', 'rb')
        files = os.listdir(f'img/{text}')
        send = bot.send_photo(message.chat.id, photo, caption='Выберите номер задания:', reply_markup=generator_keyboards(sorted(sorted(list(map(int, list(map(clean_name, files))))))))
        bot.register_next_step_handler(send, variant, type_work = f'{text}')
    else:
        bot.send_message(message.chat.id, 'Выберите задание:', reply_markup=generator_keyboards(list_menu))

# тест
bot.polling()