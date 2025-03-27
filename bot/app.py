import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_NAME = os.getenv('DATABASE_NAME')

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text='Загрузить файл')
    await message.answer(
        "Загрузите список сайтов для парсинга",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


# Обработка загруженного файла
@dp.message(F.document)
async def handle_document(message: Message):
    downloaded_file_name = 'uploaded_file.xlsx'
    file = await bot.get_file(message.document.file_id)
    await bot.download(file=file, destination=downloaded_file_name)
    df = pd.read_excel(downloaded_file_name)
    dict_list = df.to_dict(orient='records')
    with sqlite3.connect(DATABASE_NAME) as conn:
        for record in dict_list:
            conn.execute(
                'INSERT INTO parser_data (title, url, xpath) VALUES (?, ?, ?)',
                (record['title'], record['url'], record['xpath'])
            )
        conn.commit()
    await message.answer(df.head().to_csv())
    os.remove(downloaded_file_name)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
