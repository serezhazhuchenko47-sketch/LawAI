from openai import OpenAI

from config import OPENAI_API_KEY
from prompts import LAWYER_PROMPT


client = OpenAI(api_key=OPENAI_API_KEY)


def ask_ai(history, system_prompt=LAWYER_PROMPT):
    """
    Надсилає історію повідомлень до OpenAI.
    За замовчуванням використовує LAWYER_PROMPT,
    але можна передати будь-який інший промпт.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            *history,
        ],
    )

    return response.choices[0].message.content