import logging
import os
from html import escape

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# Можно задать через переменную окружения GIF_URL
GIF_URL = os.getenv(
    "GIF_URL",
    "https://media.giphy.com/media/ASd0Ukj0y3qMM/giphy.gif",
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветствие и GIF при входе новых пользователей в группу."""
    if not update.message or not update.message.new_chat_members:
        return

    chat = update.effective_chat
    if not chat or chat.type not in {"group", "supergroup"}:
        return

    for new_user in update.message.new_chat_members:
        mention = new_user.mention_html()
        first_name = escape(new_user.first_name or "друг")
        welcome_text = (
            f"👋 Добро пожаловать, {mention}!\n"
            f"Рады видеть тебя в чате, {first_name}!"
        )

        try:
            await context.bot.send_animation(
                chat_id=chat.id,
                animation=GIF_URL,
                caption=welcome_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=update.message.message_id,
            )
            logger.info(
                "Sent welcome GIF to user_id=%s in chat_id=%s",
                new_user.id,
                chat.id,
            )
        except Exception:
            logger.exception(
                "Failed to send welcome GIF to user_id=%s in chat_id=%s",
                new_user.id,
                chat.id,
            )


async def on_startup(application: Application) -> None:
    bot = application.bot
    me = await bot.get_me()
    logger.info("Bot started as @%s (id=%s)", me.username, me.id)
    logger.info("GIF_URL=%s", GIF_URL)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не задан. Установите переменную окружения BOT_TOKEN.")

    application = Application.builder().token(token).build()

    # Реагируем только на событие входа новых пользователей
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members)
    )

    application.post_init = on_startup

    logger.info("Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
