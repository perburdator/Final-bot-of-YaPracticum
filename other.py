bot_token = 'Ваш токен для телеграмм бота'  # 7047335998:AAEdrIdjTc1ED_bXuo2XGQp0IHGmBiNcTVQ

DB_NAME = 'database.db'
TABLE_NAME = 'texts'

ADMIN_ID = 'Ваш айди от телеграмма'

IAM_TOKEN = 'Ваш иам токен для аутентификации'
FOLDER_ID = 'Ваш фолдер айди от яндекс клауд'

MAX_USER_TTS_SYMBOLS = 100
MAX_TTS_SYMBOLS = 1000
MAX_GPT_TOKENS = 1000
MAX_USER_SESSIONS = 5

SYSTEM_PROMPT = 'Ты умный помощник по многим вопросам. Отвечай на вопросы вежливо.'

LOGS = 'logs_about_gpt'
LOGS_BOT = 'logs_bot'

text_starting = ('Привет! Данный бот умеет распознавать ваш голос, а затем отправлять вопрос из голосового сообщения в '
                 'нейросеть. Также, если вы отправите просто текстовый вопрос, то бот сможет ответить и на него.'
                 'Главная фишка - как вы зададите вопрос, так вы и получите ответ(аудио-аудио_ответ, текст-текстовый_ответ)'
                 'Для получения логов программы нажмите сюда --> /send_logs')
