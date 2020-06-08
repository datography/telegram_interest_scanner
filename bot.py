import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from SQLighter import SQLighter

# logging
logging.basicConfig(level=logging.INFO)

# bot initializing
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# Initializing connection with database
db = SQLighter('db.db')

# Subscription activation


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # If there is no user with such id, we add him to database
        db.add_subscriber(message.from_user.id)
    else:
        # If he is there already, we update his status
        db.update_subscription(message.from_user.id, True)

    await message.answer("You have successfully subscribed to the Crypto Interest Scanner!")


# Subscription deactivation
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # If there is no user with such id, we add him to database but with deacivated status
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Yoy're not subscribed anyway, why are you clicking this button?")
    else:
        # If he is subscribed, we update his status to "Unsubscribed"
        db.update_subscription(message.from_user.id, False)
        await message.answer("You have unsubscribed from the Crypto Interest Scanner! We will miss you =(")

# Long polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
