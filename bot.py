import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler
import telegram.ext.filters as filters
import re

def start(update: Update, context):
    update.message.reply_text('Бот ишга туширилди ва канал постларини кузатмоқда.')

async def check_post(update: Update, context):
    text = update.channel_post.text
    if is_cyrillic(text):
        keyboard = [
            [InlineKeyboardButton("Лотинчага ўгириш", callback_data='to_latin')],
            [InlineKeyboardButton("Leave a comment", callback_data='leave_comment')]  # Comment button
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Кирилчага ўгириш", callback_data='to_cyrillic')],
            [InlineKeyboardButton("Leave a comment", callback_data='leave_comment')]  # Comment button
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Faqat tugmalarni yangilash
    await update.channel_post.edit_text(
        text=text,  # Foydalanuvchi yuborgan matnni qo'yamiz
        reply_markup=reply_markup  # Tugmalarni qayta yuboramiz
    )

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    text = query.message.text  # Matnni olish
    if query.data == 'to_latin':
        converted_text = cyrillic_to_latin(text)
        keyboard = [
            [InlineKeyboardButton("Кирилчага ўгириш", callback_data='to_cyrillic')],
            [InlineKeyboardButton("Leave a comment", callback_data='leave_comment')]  # Comment button
        ]
    elif query.data == 'to_cyrillic':
        converted_text = latin_to_cyrillic(text)
        keyboard = [
            [InlineKeyboardButton("Лотинчага ўгириш", callback_data='to_latin')],
            [InlineKeyboardButton("Leave a comment", callback_data='leave_comment')]  # Comment button
        ]
    elif query.data == 'leave_comment':
        converted_text = text  # Comment action or any other logic you want to add
        keyboard = [
            [InlineKeyboardButton("Leave a comment", callback_data='leave_comment')]  # Keep comment button
        ]
    
    # Matnni yangilash va tugmani bosishdan keyin natijani yuborish
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(text=converted_text, reply_markup=reply_markup)

def is_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))

# Кирилча матнни лотинчага таржима
def cyrillic_to_latin(text):
    cyrillic_to_latin_map = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
        "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", 
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya"
    }
    for cyrillic, latin in cyrillic_to_latin_map.items():
        text = text.replace(cyrillic, latin).replace(cyrillic.upper(), latin.upper())
    return text

# Лотиндан Кирилга таржима
def latin_to_cyrillic(text):
    latin_to_cyrillic_map = {
        "a": "а", "b": "б", "v": "в", "g": "г", "d": "д", "e": "е", "yo": "ё",
        "j": "ж", "z": "з", "i": "и", "y": "й", "k": "к", "l": "л", "m": "м",
        "n": "н", "o": "о", "p": "п", "r": "р", "s": "с", "t": "т", "u": "у",
        "f": "ф", "x": "х", "ts": "ц", "ch": "ч", "sh": "ш", "shch": "щ", 
        "yu": "ю", "ya": "я", "e": "э"
    }
    
    for latin, cyrillic in latin_to_cyrillic_map.items():
        text = text.replace(latin, cyrillic).replace(latin.upper(), cyrillic.upper())
    return text

async def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_post))
    application.add_handler(CallbackQueryHandler(button))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
