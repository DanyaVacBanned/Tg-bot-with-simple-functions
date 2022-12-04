from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

sub_btn_yes = KeyboardButton('Да')
sub_btn_no = KeyboardButton('Нет')

sub_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(sub_btn_yes).add(sub_btn_no)

sub_btn = KeyboardButton('-Подписаться на рассылку-')
meme_btn = KeyboardButton('-Прислать 3 картинки по запросу-')
unsub_btn = KeyboardButton('-Отписаться от рассылки-')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(sub_btn).add(meme_btn)
main_keyboard_with_sub = ReplyKeyboardMarkup(resize_keyboard=True).add(sub_btn).add(meme_btn).add(unsub_btn)
