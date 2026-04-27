import logging
import os
from html import escape

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.new_chat_members:
        return

    chat = update.effective_chat
    if not chat or chat.type not in {"group", "supergroup"}:
        return

    for new_user in update.message.new_chat_members:
        mention = new_user.mention_html()
        first_name = escape(new_user.first_name or "уебище")
        welcome_text = (
            f"Пошел нахуй, тебе тут не рады"
        )

        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=welcome_text,
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

def main() -> None:
    token = "TOKEN"
    application = Application.builder().token(token).build()
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members)
    )

    application.post_init = on_startup

    logger.info("Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
