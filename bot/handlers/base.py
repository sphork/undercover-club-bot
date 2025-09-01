from typing import Dict, List
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.keyboards.main_menu import build_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в Undercover Club!\nВыберите действие:', reply_markup=build_main_menu())


@router.callback_query(F.data == 'help')
async def process_help(callback_query: CallbackQuery):
    text = (
        'Руководство по командам и кнопкам:\n'
        '/start — главное меню\n'
        '/newgame — создать новую игру\n'
        '/join — присоединиться к игре\n'
        '/leave — выйти из игры\n'
        '/vote — голосование\n'
        '/balance — баланс валюты\n'
        '/tasks — открыть чек-лист заданий\n'
        '/shop — магазин\n'
        '/stats — статистика игрока\n'
        '\n'
        'Основные действия доступны через кнопки под сообщениями.'
    )
    await callback_query.message.answer(text)
    await callback_query.answer()


@router.callback_query(F.data == 'join_game')
async def process_join_game(callback_query: CallbackQuery):
    await callback_query.message.answer('Вы присоединились к лобби! Ожидайте начала игры.')
    await callback_query.answer()


@router.callback_query(F.data == 'create_game')
async def process_create_game(callback_query: CallbackQuery):
    await callback_query.message.answer('Создана новая игра! Ждём игроков...')
    await callback_query.answer()


@router.callback_query(F.data == 'balance')
async def process_balance(callback_query: CallbackQuery):
    await callback_query.message.answer('Ваш баланс: 0 монет (функция в разработке)')
    await callback_query.answer()


# ======== Tasks checklist (simple demo) ========
user_tasks: Dict[int, List[bool]] = {}


def get_user_tasks(user_id: int) -> List[bool]:
    tasks = user_tasks.get(user_id)
    if tasks is None:
        tasks = [False, False, False]
        user_tasks[user_id] = tasks
    return tasks


def format_tasks_text(tasks: List[bool]) -> str:
    icons = ['✅' if t else '⬜' for t in tasks]
    return (
        'Чек-лист (демо):\n'
        f'1. Базовое знакомство — {icons[0]}\n'
        f'2. Присоединиться к лобби — {icons[1]}\n'
        f'3. Сделать первое действие — {icons[2]}\n'
        '\nНажмите на пункты, чтобы отметить/снять отметку.'
    )


from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_tasks_kb(tasks: List[bool]):
    kb = InlineKeyboardBuilder()
    labels = [f'1 {"✅" if tasks[0] else "⬜"}', f'2 {"✅" if tasks[1] else "⬜"}', f'3 {"✅" if tasks[2] else "⬜"}']
    kb.button(text=labels[0], callback_data='task:1')
    kb.button(text=labels[1], callback_data='task:2')
    kb.button(text=labels[2], callback_data='task:3')
    kb.adjust(3)
    kb.button(text='Сбросить', callback_data='reset_tasks')
    kb.button(text='Назад', callback_data='back_to_menu')
    kb.adjust(2)
    return kb.as_markup()


@router.callback_query(F.data == 'tasks')
async def open_tasks(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    tasks = get_user_tasks(uid)
    await callback_query.message.answer(format_tasks_text(tasks), reply_markup=build_tasks_kb(tasks))
    await callback_query.answer()


@router.callback_query(F.data.startswith('task:'))
async def toggle_task(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    tasks = get_user_tasks(uid)
    try:
        idx = int(callback_query.data.split(':', 1)[1]) - 1
        if 0 <= idx < len(tasks):
            tasks[idx] = not tasks[idx]
    except Exception:
        pass
    try:
        await callback_query.message.edit_text(format_tasks_text(tasks), reply_markup=build_tasks_kb(tasks))
    except Exception:
        await callback_query.message.answer(format_tasks_text(tasks), reply_markup=build_tasks_kb(tasks))
    await callback_query.answer()


@router.callback_query(F.data == 'reset_tasks')
async def reset_tasks(callback_query: CallbackQuery):
    uid = callback_query.from_user.id
    user_tasks[uid] = [False, False, False]
    tasks = user_tasks[uid]
    try:
        await callback_query.message.edit_text(format_tasks_text(tasks), reply_markup=build_tasks_kb(tasks))
    except Exception:
        await callback_query.message.answer(format_tasks_text(tasks), reply_markup=build_tasks_kb(tasks))
    await callback_query.answer('Чек-лист сброшен')


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback_query: CallbackQuery):
    from bot.keyboards.main_menu import build_main_menu
    try:
        await callback_query.message.edit_text('Главное меню:', reply_markup=build_main_menu())
    except Exception:
        await callback_query.message.answer('Главное меню:', reply_markup=build_main_menu())
    await callback_query.answer()
