from aiogram import types, Bot
import config
import db
from json_fun import get_partner_channels
bot = Bot(token=config.token)










async def check(user_id):
  user = await db.get_user_by_id(user_id)

  not_sub = []
  channel = await get_partner_channels()
  for i in range(0 , len(channel)):
    user_channel_status = await bot.get_chat_member(chat_id=channel[i][0]['id'], user_id=user_id)
    if user_channel_status["status"] != 'left':
      channel[i][0]['is_sub'] = True




    else:
      not_sub.append(channel[i][0])
  if len(not_sub) == 0:
        is_sub_all = True
  else:
        is_sub_all = False

  if user['Is_paid'] == 0 and is_sub_all:
    await db.set_is_paid(user_id)
  return {
    "is_sub_all": is_sub_all,
    "sub_await" :not_sub
  }


  print(channel)

