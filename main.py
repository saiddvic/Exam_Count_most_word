import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from config import conf
from model import Order
from base import db as database

dp = Dispatcher()

@dp.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await database.create_all()


    await Order.create(word=message.text, counter=0)


@dp.message(Command('recentword'), F.chat.type == ChatType.PRIVATE)
async def recent_word_handler(message: Message, bot: Bot) -> None:
    orders = await Order.get_all()
    user_id = message.from_user.id
    c = 1
    word = ''
    for order in orders:
        c = order.counter
        for order2 in orders:
            if order2.counter > c:
                c = order2.counter
                word = order2.word
    await bot.send_message(chat_id=user_id, text=f"Eng kop yozilgan soz bu {word}: {c} martta")

@dp.message(F.chat.type == ChatType.PRIVATE)
async def message_handler(message: Message) -> None:
    await Order.create(word=message.text, counter=0)
    orders = await Order.get_all()
    for order in orders:
        if order.word == message.text:
            await Order.update(order.id, counter=order.counter + 1)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await database.create_all()
    commands_list = [
        BotCommand(command='start', description='Botni ishga tushurish'),
        BotCommand(command='recentword', description='Botga eng kop yozilgan sozni korish'),
    ]
    await bot.set_my_commands(commands_list)

async def main() -> None:
    dp.startup.register(on_startup)
    bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())