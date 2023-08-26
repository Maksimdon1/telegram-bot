from aiogram.utils import executor
from create_bot import dip
from handlers import user,admin
async def start(_):
    pass

user.register_handlers_user(dip)
admin.register_handlers_admin(dip)


if __name__ == '__main__':
    executor.start_polling(dip, skip_updates=True, on_startup=start)







