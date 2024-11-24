from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from API import token
import os
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инлайн кнопки для продуктов
product_kp = InlineKeyboardMarkup(row_width=2)
products = [
    InlineKeyboardButton(text='Product1', callback_data='product_buying'),
    InlineKeyboardButton(text='Product2', callback_data='product_buying'),
    InlineKeyboardButton(text='Product3', callback_data='product_buying'),
    InlineKeyboardButton(text='Product4', callback_data='product_buying'),
]
product_kp.add(*products)

# Главное меню
start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.username if message.from_user.username else message.from_user.first_name
    await message.answer(f'Привет, {user_name}! Я бот, помогающий твоему здоровью!',
                         reply_markup=start_menu)

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products_info = [
        ("Product1", "описание 1", 100, '1.png'),
        ("Product2", "описание 2", 200, '2.png'),
        ("Product3", "описание 3", 300, '3.png'),
        ("Product4", "описание 4", 400, '4.png')
    ]


    file_paths = ['files/1.png', 'files/2.png', 'files/3.png', 'files/4.png']

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"{file_path} существует")
        else:
            print(f"{file_path} не найден")

    for index, (name, description, price, image_path) in enumerate(products_info, start=1):
        await message.answer(f'Название: {name} | Описание: {description} | Цена: {price * 100}₽')
        try:
            with open(image_path, "rb") as img:
                await bot.send_photo(chat_id=message.chat.id, photo=img)
        except Exception as e:
            await message.answer(f"Ошибка при отправке изображения {name}: {e}")

    await message.answer("Выберите продукт для покупки:", reply_markup=product_kp)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()  # Убираем уведомление
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kp)
    await message.answer('Клавиатура скрыта.', reply_markup=None)  # Скрываем клавиатуру

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)