# Telegram Welcome Bot (python-telegram-bot v20+)

Бот отслеживает вход новых пользователей в **группу/супергруппу** и отправляет приветственное GIF-сообщение с mention.

## Возможности

- Отслеживание новых участников через `new_chat_members`
- Приветствие как **ответ** на сервисное сообщение о входе
- Mention пользователя в тексте приветствия
- Отправка GIF по `GIF_URL`
- `async/await` стиль для `python-telegram-bot v20+`
- Конфигурация через environment variables
- Логирование (`INFO`)
- Обработка ошибок при отправке сообщения (`try/except`)

## Требования

- Python 3.10+

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка

Обязательная переменная:

- `BOT_TOKEN` — токен вашего бота от BotFather

Опциональная:

- `GIF_URL` — URL (или `file_id`) GIF для приветствия

Пример:

```bash
export BOT_TOKEN="123456:ABC-DEF..."
export GIF_URL="https://media.giphy.com/media/ASd0Ukj0y3qMM/giphy.gif"
```

## Запуск

```bash
python bot.py
```

## Важно для работы в группах

1. Добавьте бота в группу.
2. Отключите Privacy Mode в BotFather (`/setprivacy -> Disable`), чтобы бот получал сервисные сообщения о новых участниках.
3. Дайте боту право отправки сообщений в группу.
