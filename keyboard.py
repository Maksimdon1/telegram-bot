from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def home_user():
    button1 = KeyboardButton(text='🔐 Кошелек',  callback_data='btn')
    button2 = KeyboardButton(text='📊 Инфо')

    panel = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2).add(KeyboardButton(text='💎 Заработать'))




    return  panel

def home_admin():
    button1 = KeyboardButton(text='🔐 Кошелек', callback_data='btn')
    button2 = KeyboardButton(text='📊 Инфо')

    panel = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2).add(KeyboardButton(text='💎 Заработать'))


    panel.add('🔝 Админка')
    return panel
def back():
    button1 = KeyboardButton(text='◀️ Назад')


    panel = ReplyKeyboardMarkup(resize_keyboard=True)




    panel.add(button1)
    return panel

def verify_pay():
    button1 = KeyboardButton(text='Подтвердить',  callback_data='verify')
    button2 = KeyboardButton(text='Отмена' ,  callback_data='cancel')

    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    panel.row(button1, button2)
    return panel

def registration():
    button1 = KeyboardButton(text='Зарегистрироваться', callback_data='start')


    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    panel.add(button1)
    return panel
def admin_btn():
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    mail = InlineKeyboardButton('📩 Рассылка', callback_data='mail')
    payments = InlineKeyboardButton('💳 Выплаты в ожидании', callback_data='payments')
    pay_img = InlineKeyboardButton('🧾 История выплат', callback_data='pay-img')
    price_settings = InlineKeyboardButton('⚙️ Настройка цены', callback_data='price-settings')


    inline_kb_full.add(mail,payments,pay_img,price_settings)
    return inline_kb_full
def info():
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    mail = InlineKeyboardButton('📩 Рассылка', callback_data='mail')
    payments = InlineKeyboardButton('💳 Выплаты в ожидании', callback_data='payments')
    pay_img = InlineKeyboardButton('🧾 История выплат', callback_data='pay-img')
    price_settings = InlineKeyboardButton('⚙️ Настройка цены', callback_data='price-settings')

    inline_kb_full.add(mail, payments, pay_img, price_settings)
    return inline_kb_full

def buy():


    panel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Купить DEATH'))
    return panel
def currency():
    button1 = KeyboardButton(text='Toncoin 💎')
    button2 = KeyboardButton(text='DEATH Coin ☠️')

    panel = ReplyKeyboardMarkup(resize_keyboard=True).row(button2).add(KeyboardButton(text='🔙 Назад'))
    return panel
def back():

    panel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='🔙 Назад'))
    return panel

def url(url):
    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    pay = InlineKeyboardButton('Оплатить $$$', url=url)
    inline_kb_full.add(pay)
    return inline_kb_full
def proff():

    panel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Подтвердить'))
    return panel
