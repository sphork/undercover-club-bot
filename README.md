# Undercover Club — Telegram Bot (aiogram v3)

Телеграм-бот для игр в группе (начиная с демо-функций и чек-листа). Стек: Python 3.13, aiogram 3.x.

## Быстрый старт
1. Скопируйте `.env.example` в `.env` и укажите `API_TOKEN`.
2. Создайте и активируйте виртуальное окружение.
3. Установите зависимости: `pip install -r requirements.txt`.
4. Запуск: `python main.py`.

## Структура
- `main.py` — точка входа, запуск бота.
- `bot/handlers/` — хендлеры команд и кнопок.
- `bot/keyboards/` — инлайн-клавиатуры.
- `.env.example` — пример env-файла (секреты не коммитим).
- `.gitignore` — исключения для Git.

## Лицензия
MIT
