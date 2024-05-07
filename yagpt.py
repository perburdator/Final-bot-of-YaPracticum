import requests
import logging
from other import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, IAM_TOKEN, FOLDER_ID


logging.basicConfig(filename=LOGS, level=logging.ERROR,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")


def count_gpt_tokens(text: str) -> int:
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
        json={"modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest", "text": text},
        headers=headers
    )
    logging.info("\n\nТокенов=", response.json())
    return len(response.json()['tokens'])


# запрос к GPT
def ask_gpt(messages):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.8,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": [
            {"role": "system", "text": SYSTEM_PROMPT},
            {"role": "user", "text": messages},
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        # tokens_in_answer = count_gpt_tokens(answer)

        return answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка с GPT"
