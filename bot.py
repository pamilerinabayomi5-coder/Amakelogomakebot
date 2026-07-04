import os
import re
import logging
from collections import Counter
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]


# ── Helpers ──────────────────────────────────────────────────────────────────

def analyze_text(text: str) -> dict:
    """Return word/char/sentence/top-word stats for *text*."""
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    chars_no_spaces = len(text.replace(" ", ""))
    top = Counter(words).most_common(5)
    avg_len = (sum(len(w) for w in words) / len(words)) if words else 0

    return {
        "words": len(words),
        "chars": len(text),
        "chars_no_spaces": chars_no_spaces,
        "sentences": len(sentences),
        "paragraphs": len([p for p in text.split("\n") if p.strip()]),
        "avg_word_len": avg_len,
        "top_words": top,
        "unique_words": len(set(words)),
    }


def format_report(stats: dict) -> str:
    top_str = "\n".join(
        f"  {i+1}. *{word}* — {count}x"
        for i, (word, count) in enumerate(stats["top_words"])
    )
    return (
        "📊 *Word Count Report*\n\n"
        f"📝 Words: *{stats['words']:,}*\n"
        f"🔤 Unique words: *{stats['unique_words']:,}*\n"
        f"🔡 Characters \\(with spaces\\): *{stats['chars']:,}*\n"
        f"🔡 Characters \\(no spaces\\): *{stats['chars_no_spaces']:,}*\n"
        f"📄 Sentences: *{stats['sentences']:,}*\n"
        f"📑 Paragraphs: *{stats['paragraphs']:,}*\n"
        f"📏 Avg word length: *{stats['avg_word_len']:.1f}* chars\n\n"
        + (f"🏆 *Top {len(stats['top_words'])} words:*\n{top_str}" if stats["top_words"] else "")
    )


# ── Handlers ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 *Welcome to Word Counter Bot\\!*\n\n"
        "Just send me any text and I'll give you a full breakdown:\n"
        "• Word & character count\n"
        "• Unique words\n"
        "• Sentence & paragraph count\n"
        "• Top 5 most\\-used words\n\n"
        "📎 You can also *forward messages* or *send a text file*\\.\n\n"
        "Commands:\n"
        "/start — show this message\n"
        "/help  — usage tips\n"
        "/count — count the text you reply to",
        parse_mode="MarkdownV2",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💡 *How to use*\n\n"
        "1\\. *Send any text* directly — I'll count it immediately\\.\n"
        "2\\. *Reply to a message* with /count — I'll count that message\\.\n"
        "3\\. *Send a \\.txt file* — I'll extract and count its text\\.\n"
        "4\\. *Forward messages* — works too\\!",
        parse_mode="MarkdownV2",
    )


async def count_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Count words in a plain-text message."""
    text = update.message.text or ""
    if not text.strip():
        await update.message.reply_text("⚠️ Please send some text for me to count.")
        return

    stats = analyze_text(text)
    await update.message.reply_text(format_report(stats), parse_mode="MarkdownV2")


async def count_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/count command: count the replied-to message."""
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "↩️ Reply to any message with /count to count its words."
        )
        return

    text = update.message.reply_to_message.text or update.message.reply_to_message.caption or ""
    if not text.strip():
        await update.message.reply_text("⚠️ The replied message has no countable text.")
        return

    stats = analyze_text(text)
    await update.message.reply_text(format_report(stats), parse_mode="MarkdownV2")


async def count_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Count words in an uploaded .txt file."""
    doc = update.message.document
    if not doc.file_name.endswith(".txt"):
        await update.message.reply_text("📎 Please send a plain *.txt* file.", parse_mode="Markdown")
        return

    if doc.file_size > 1_000_000:  # 1 MB guard
        await update.message.reply_text("⚠️ File too large (max 1 MB).")
        return

    await update.message.reply_text("⏳ Reading file…")
    tg_file = await doc.get_file()
    raw = await tg_file.download_as_bytearray()

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    stats = analyze_text(text)
    await update.message.reply_text(
        f"📄 *File:* `{doc.file_name}`\n\n" + format_report(stats),
        parse_mode="MarkdownV2",
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("count", count_reply))
    app.add_handler(MessageHandler(filters.Document.FileExtension("txt"), count_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_text))

    logger.info("Bot is running…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
