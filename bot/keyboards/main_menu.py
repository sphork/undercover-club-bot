from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text='Присоединиться к игре', callback_data='join_game')
    kb.button(text='Создать игру', callback_data='create_game')
    kb.button(text='Руководство', callback_data='help')
    kb.button(text='Баланс', callback_data='balance')
    kb.button(text='Задания', callback_data='tasks')
    kb.adjust(2)
    return kb.as_markup()
