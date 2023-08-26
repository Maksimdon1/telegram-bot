import aiogram.utils.markdown as md
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from create_bot import dip, bot
from bot import keyboard
import time
import cofig
import rocket
class Form(StatesGroup):
    currency = State()
    value = State()  # Will be represented in storage as 'Form:name'
    ispaid =  State()
    pay_id = State()
    user_id = State()

#@dip.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id


    await bot.send_message(user_id, "Привет, это бот обменник где вы можете купить DEATH", reply_markup=keyboard.buy())

async def back(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.finish()
    await bot.send_message(user_id, "Привет, это бот обменник где вы можете купить DEATH", reply_markup=keyboard.buy())


#@dip.message_handler(commands=['start'])
async def buy(message: types.Message):
    user_id = message.from_user.id

    await bot.send_message(user_id, f"Вы собираетесь купить DEATH Coin за валюту TON\n1 💎 = {cofig.course} ☠️")
    time.sleep(0.5)
    await bot.send_message(user_id, "Выберите в чем укажите стоимость:", reply_markup=keyboard.currency())
    await Form.currency.set()



async def currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:




        user_id = message.from_user.id

        if message.text == 'Toncoin 💎':
            currency = 'Ton'
            data['currency'] = currency

            await bot.send_message(user_id, f"Укажите на сколько Ton вы хотите приобрести:", reply_markup=keyboard.back())
            await Form.next()
        elif message.text == 'DEATH Coin ☠️':
            currency = 'Death'
            data['currency'] = currency
            await bot.send_message(user_id, f"Укажите сколько вы хотите приобрести:",reply_markup=keyboard.back())
            await Form.next()


        print(currency)




async def value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        user_id = message.from_user.id
        user_name = message.from_user.username


        if message.text.isdigit() and int(message.text) >= 10:
            value = float(message.text)


            pay = 0
            death = 0




            if data['currency'] == 'Death':
                pay = value * cofig.course
                death = value
            if data['currency'] == 'Ton':
                pay = value
                death = value / cofig.course

            post = rocket.createInvoice(death=death, amount=pay)

            data['value'] = [{'pay_id': post['data']['id'], 'user_id': 'user_id', 'username': user_name}]









            await bot.send_message(user_id, f"$ ЧЕК $\n\nTON ➡️ DEATH\nКурс: 1 💎 = {cofig.course} ☠️ \nСумма к оплате в TON: {pay}\nВы получаете: {death} Death", reply_markup=keyboard.url(post['data']['link']))
            await bot.send_message(user_id,'После оплаты нажмите на кнопку подтвердить и ожидайте пополнения', reply_markup=keyboard.proff())

            await Form.next()





@dip.message_handler(state='*', commands='cancel')
@dip.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


#@dip.message_handler(lambda message: message.text, state=Form.verify)
async def verify(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_name = message.from_user.username
        payment = (data['value'])
        pay_id = data['value'][0]['pay_id']

        is_paid = rocket.get_invoice(pay_id)['data']['paid']
        pay_value = rocket.get_invoice(pay_id)['data']['amount']
        print(pay_value)
        print(data)
        print(payment)
        print(is_paid)




        user_id = message.from_user.id
        if is_paid:



            await bot.send_message(user_id, 'Операция подтверждена ',reply_markup=keyboard.buy())
            await send_pay(user_id=user_id, username=user_name, death=pay_value)
            await state.finish()
        else:
            await bot.send_message(user_id, 'Попробуйте подождать пару минут ')
            await Form.next()








    user_id = message.from_user.id

    await state.finish()







async def send_pay(user_id, death, username):
    await bot.send_message(-976090627, f'Произведена покупка нужно отправить {death}  пользователю {username} ')








def register_handlers_user(dp: Dispatcher):

    dp.register_message_handler(start, commands=['start'] )
    dp.register_message_handler(value, lambda message: message.text, state=Form.value)
    dp.register_message_handler(verify, lambda message: message.text and 'Подтвердить' in message.text  , state=Form.ispaid)
    dp.register_message_handler(buy,lambda message: message.text and 'Купить DEATH' in message.text )
    dp.register_message_handler(back,lambda message: message.text and '🔙 Назад' in message.text )
#   dp.register_callback_query_handler(cmd_start, lambda message: message.data and message.data.startswith('ton'))
    dp.register_message_handler(currency,  lambda message: message.text and 'Toncoin 💎' in message.text or  'DEATH Coin ☠️' in message.text, state=Form.currency)
