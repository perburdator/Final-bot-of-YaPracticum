from db import create_table, insert_row, count_all_symbol
from stt_func import speech_to_text, text_to_speech  # tts is unused func
import telebot
import logging
from other import bot_token, MAX_USER_TTS_SYMBOLS, MAX_TTS_SYMBOLS, LOGS_BOT, MAX_USER_SESSIONS, ADMIN_ID
from validators import is_stt_block_limit
from yagpt import count_gpt_tokens, ask_gpt
import os

bot = telebot.TeleBot(token=bot_token)

create_table('messages')

logging.basicConfig(filename=LOGS_BOT, level=logging.ERROR,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

users = {}  # словарь для определения количества сессий пользователя


def is_tts_symbol_limit(message, text):
    user_id = message.from_user.id
    text_symbols = len(text)

    all_symbols = count_all_symbol(user_id) + text_symbols

    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит Speechkit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        bot.send_message(user_id, msg)
        return None

    if text_symbols >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит Speechkit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(text)

@bot.message_handler(commands=['about'])
def about_func(message):
    with open("README.md", "rb") as f:
        bot.send_document(message.chat.id, f)

@bot.message_handler(commands=['start'])
def start_func(message):
    user_id = message.from_user.id
    insert_row(user_id, 'start', 0)
    bot.send_message(message.chat.id, 'Отправь команду /stt , чтобы распознать текст вашего аудиосообщения')
    logging.info(f'{user_id} started chat!')


@bot.message_handler(commands=['send_logs'])
def send_all_logs(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        if os.path.exists('log_about_gpt'):
            with open("logs_about_gpt", "rb") as f:
                bot.send_document(message.chat.id, f)
        if os.path.exists('logs_bot.txt'):
            with open("logs_bot", "rb") as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, 'File not found')
            logging.error(f'Cant find this files ')


# -----------------------------------------starting--------------------------------------------------------------------
'''
Handler of voice
'''


@bot.message_handler(content_types=["voice"])
def handle_voice_message(message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id] == MAX_USER_SESSIONS:
            bot.send_message(user_id, "Вы уже сделали 5 запросов(")
            return
    else:
        users[user_id] = 0

    stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)
    if not stt_blocks:
        bot.send_message(user_id, error_message)
        return
    if message.voice.duration > 15:
        bot.send_message(user_id, "Сообщение не должно быть дольше 15 секунд")
        return

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    status, text = speech_to_text(file)
    ''' This is sending to user text of his audio, not necessary
    if not status:
        insert_row(user_id, text, stt_blocks)
        bot.send_message(user_id, text)
        return
    '''
    if len(text.split()) > 100:
        bot.send_message(user_id, "Сообщение превысило лимит 100 слов")
        return
    gpt_ans = ask_gpt(text)
    used_tokens = count_gpt_tokens(gpt_ans)
    insert_row(user_id, gpt_ans, used_tokens)
    users[user_id] += 1
    status, content = text_to_speech(gpt_ans)
    if status:
        bot.send_voice(user_id, content)
    else:
        bot.send_message(user_id, status)
    logging.info(f'User got this gpt_answer {gpt_ans}')


'''
Handler of text
'''


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_id = message.from_user.id
    text_from_user = message.text

    text_symbol = is_tts_symbol_limit(message, text_from_user)
    if text_symbol is None:
        return

    insert_row(user_id, text_from_user, text_symbol)
    gpt_ans = ask_gpt(text_from_user)
    used_tokens = count_gpt_tokens(gpt_ans)
    insert_row(user_id, gpt_ans, used_tokens)
    users[user_id] += 1
    bot.send_message(user_id, gpt_ans)
    logging.info(f'User got this gpt_answer {gpt_ans}')


# Entry point
if __name__ == "__main__":
    logging.info('Bot is now running')
    bot.infinity_polling()
