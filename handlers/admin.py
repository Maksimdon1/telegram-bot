from json_fun import get_referral_price, change_referral_price
import db
from subscribe_filter import check
from bot import keyboard as keyboard
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from create_bot import dip, bot

class Distribution(StatesGroup):
    post = State()
class ref_price(StatesGroup):
    price = State()


async def admin_start(message: types.Message):
    user_id = message.from_user.id
    user = await db.get_user_by_id(user_id)

    if user and user['System'] =='Admin' :
        await check(user_id)



        def hello(name):
            return f" 👋 Привет, <b>{name} </b>\n⚪️ Добро пожаловать в наш бот\n💵 для заработка!"


        await message.delete()
        await bot.send_message(message.from_user.id, hello(message.chat.first_name), parse_mode=types.ParseMode.HTML,
                               reply_markup=keyboard.home_admin())







async def send_for_every(arr):
    users = await db.get_send_list()
    if arr["file_path"]:
        for i in users:
            img = open(f'./photos/{arr["file_path"]}', 'rb')

            await bot.send_photo(chat_id=i, photo=img, caption=arr['caption'])
    if arr["text"]:
        for i in users:

            await bot.send_message(chat_id=i , text= arr["text"])

#@dip.message_handler(lambda message: message.text and '🔝 Админка' in message.text)
async def admin_comm(message: types.Message):
    user_id = message.from_user.id
    user = await db.get_user_by_id(user_id)
    if user and user['System'] == 'Admin':




        text = f"Админ панель: \n \nПользователей: {await db.get_user_value()} \nПользователей-рефералов: {await db.get_ref_value()} \nВсего заявок: {await db.get_payments_value()} \nСтоимость реферала: {await get_referral_price()}₽\nВыплачено: {await  db.get_paid_sum()} ₽\nВыплаты в ожидании: {await  db.get_await_pay_sum()} ₽\n"
        await message.delete()
        await bot.send_message(message.from_user.id, text,
                               parse_mode=types.ParseMode.HTML, reply_markup=keyboard.admin_btn())






#@dip.callback_query_handler(lambda message:  message.data and message.data.startswith('mail'))
async def mail(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = await db.get_user_by_id(user_id)
    if user and user['System'] == 'Admin':



        # Set state

        await Distribution.post.set()

        await bot.send_message(user_id, "Отправте пост")

#@dip.message_handler( content_types=[ContentType.PHOTO ,  ContentType.TEXT] , state=Distribution.post)
async def distribution_add(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await db.get_user_by_id(user_id)
    if user and user['System'] == 'Admin':
        async with state.proxy() as post:




            data = {
                "text":"",
                "img":"",
                "caption":"",
                "file_path":""

            }
            if message.text:
                data['text'] = message.text
            if message.photo:
                # print(message.photo)
                # data = open('./photos/file_74.jpg','rb')

                # await bot.send_photo(message.from_user.id,data, caption=message.caption)

                await message.photo[3].download()
                img = await message.photo[3].get_file()
                data['img'] = img
                img = await message.photo[3].get_file()
                data['file_path'] = img['file_path'].partition('/')[2]

                if message.caption:
                    data['caption'] = message.caption

            post['post'] = data

            await send_for_every(data)

            await state.finish()






@dip.callback_query_handler(lambda message:  message.data and message.data.startswith('price-settings'))
async def cmd_start(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = await db.get_user_by_id(user_id)

    user_id = callback_query.from_user.id
    user = await db.get_user_by_id(user_id)
    if user and user['System'] == 'Admin':




        # Set state

        await ref_price.price.set()

        await bot.send_message(user_id, "Введите значение")

@dip.message_handler(lambda message: message.text,state=ref_price.price)
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await db.get_user_by_id(user_id)
    if user and user['System'] == 'Admin':
        if message.text.isdigit():
            async with state.proxy() as data:
                data['price'] = message.text
                await change_referral_price(message.text)
                await bot.send_message(user_id, f'Значение изменено на : {message.text} ')







        await state.finish()







def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start,lambda message:  db.get_type_by_id(message.from_user.id) == 'Admin' , commands=['start'] )
    dp.register_message_handler(admin_comm, lambda message: message.text and '🔝 Админка' in message.text and  db.get_type_by_id(message.from_user.id) =='Admin')
    dp.register_callback_query_handler(mail, lambda message:  message.data and message.data.startswith('mail'))
    dp.register_message_handler(distribution_add, lambda message: db.get_type_by_id(message.from_user.id) =='Admin' , content_types=[ContentType.PHOTO ,  ContentType.TEXT] , state=Distribution.post )

