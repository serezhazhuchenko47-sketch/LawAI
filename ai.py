from datetime import datetime

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

    today = datetime.now().strftime("%d.%m.%Y")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    f"{system_prompt}\n\n"
                    f"Поточна дата: {today}.\n"
                    "Вважай цю дату актуальною. "
                    "Якщо користувач запитує про 'сьогодні', 'зараз', "
                    "'чинний', 'на даний момент' або про строки, "
                    "орієнтуйся саме на цю дату. "
                    "Не припускай, що зараз 2024 рік."
                ),
            },
            *history,
        ],
    )

    return response.choices[0].message.content