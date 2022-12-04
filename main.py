from time import sleep
from aiogram import Bot, Dispatcher, executor, types
import logging
import configparser
from aiogram.dispatcher import FSMContext
from FSM import Request, Sub, Unsub, Sendall
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from bs4 import BeautifulSoup as b
from fake_useragent import UserAgent
import nav
from database import Database
#-------------BOT INITIALIZING-----------------
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
config = configparser.ConfigParser() #В файле config.ini лежит токен бота и телеграмм id админа
config.read('config.ini')
token = config['Telegram']['bot_token']        
admin_id = config['Telegram']['admin_id']
bot = Bot(token=token)
db = Database()
dp = Dispatcher(bot, storage=storage)
#---------------------------------------------------

@dp.message_handler(commands=['start', 'help'])
async def on_start(message: types.Message):
    with open('welcome_text.txt','r', encoding='utf-8') as f:
        if db.select_user_by_id(message.from_user.id) == None:
            await bot.send_message(message.chat.id, f.read(), reply_markup=nav.main_keyboard)
        else:
            await bot.send_message(message.chat.id, f.read(), reply_markup=nav.main_keyboard_with_sub)

@dp.message_handler(text='-Подписаться на рассылку-', state = None)
async def sub_func(message: types.Message):
    await Sub.subApprove.set()
    await bot.send_message(message.chat.id, 'Вы хотите подписаться на сервис?\nДанная функция позволит вам получать сообщения из общей рассылки!', reply_markup=nav.sub_keyboard)

@dp.message_handler(state=Sub.subApprove)
async def sub_handle_func(message: types.Message, state=FSMContext):
    if message.text == 'Да':
        if db.select_user_by_id(int(message.from_user.id)) == None:
            db.add_user(int(message.from_user.id), str(message.from_user.first_name))
            await bot.send_message(message.chat.id, 'Поздравляю, вы подписались на сервис!', reply_markup=nav.main_keyboard_with_sub)
            await state.finish()
        else:
            await bot.send_message(message.chat.id, 'Вы уже подписанны на рассылку', reply_markup=nav.main_keyboard_with_sub)
    elif message.text == 'Нет':
        await bot.send_message(message.chat.id,'Вы не подписались на сервис.', reply_markup=nav.main_keyboard)
        await state.finish()
    else:
        await bot.send_message(message.chat.id,'Некорректный ввод', reply_markup=nav.sub_keyboard)


@dp.message_handler(text='-Отписаться от рассылки-', state=None)
async def unsub_func(message:types.Message):
    await Unsub.unsubApprove.set()
    await bot.send_message(message.chat.id,'Вы уверенны, что хотите отписаться? У нас есть печеньки..', reply_markup=nav.sub_keyboard)
@dp.message_handler(state=Unsub.unsubApprove)
async def unsub_handle(message:types.Message, state=FSMContext):
    if message.text == 'Да':
        if db.select_user_by_id(message.from_user.id) != None: 
            db.delete_user_by_id(message.from_user.id)
            await bot.send_message(message.chat.id, 'Вы успешно отписались от рассылки', reply_markup=nav.main_keyboard)
            await state.finish()
        else:
            await bot.send_message(message.chat.id, 'Вы не подписанны на рассылку', reply_markup=nav.main_keyboard)
            await state.finish()

    elif message.text == 'Нет':
        await state.finish()
        await bot.send_message(message.chat.id, 'Вы всё еще подписанны',reply_markup=nav.main_keyboard_with_sub)
    else:
        await bot.send_message(message.chat.id, 'Некорректный ввод')

@dp.message_handler(text='-Прислать 3 картинки по запросу-', state=None)
async def pic_request(message: types.Message):
    await Request.user_request.set()
    await message.answer('Пришли мне запрос и я пришлю тебе первые 3 картинки')

@dp.message_handler(state=Request.user_request)
async def pic_request_handle(message:types.Message, state=FSMContext):
    ua = UserAgent()

    req = requests.get(f'https://yandex.ru/images/search?text={message.text}&from=tabbar', headers={'User-Agent':ua.random})
    print(req.status_code)
    sleep(2)
    soup = b(req.text, 'lxml')
    imgs = soup.find_all('div', {'class':'serp-item__preview'}, limit=3)
    for div in imgs:
        a = div.find('a',{'class':'serp-item__link'})
        single_img = a.find('img')
        await bot.send_message(message.chat.id, single_img.get('src'))
    await state.finish()


@dp.message_handler(commands=['sendall'], state=None)
async def send_all(message:types.Message):
    if message.from_user.id == int(admin_id):
        await Sendall.mailing.set()
        await bot.send_message(message.from_user.id, 'Ввод')
    else:
        await bot.send_message(message.from_user.id, 'Вы не являетесь администратором')
@dp.message_handler(state=Sendall.mailing)
async def send_all_handler(message: types.Message, state=FSMContext):
    for i in db.select_all_users():
        await bot.send_message(i, message.text)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
