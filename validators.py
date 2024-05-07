import math
from db import count_all_limits

MAX_USER_STT_BLOCKS = 6

def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / 15)  # округление в большую сторону
    all_blocks = count_all_limits(user_id) + audio_blocks

    if duration >= 30:
        return None, "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"

    if all_blocks > MAX_USER_STT_BLOCKS:
        return None, f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}"

    return audio_blocks, ""
