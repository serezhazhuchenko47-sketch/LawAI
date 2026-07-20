from datetime import datetime
import base64

from openai import OpenAI

from config import OPENAI_API_KEY
from prompts import LAWYER_PROMPT


client = OpenAI(api_key=OPENAI_API_KEY)


def ask_ai(history, system_prompt=LAWYER_PROMPT):
    """
    Надсилає історію повідомлень до OpenAI.
    """
    print(system_prompt)
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
                    "Вважай цю дату актуальною."
                ),
            },
            *history,
        ],
    )

    return response.choices[0].message.content


def ask_ai_image(image_path, prompt):
    """
    Аналізує фотографію документа.
    """

    with open(image_path, "rb") as f:
        image = base64.b64encode(f.read()).decode("utf-8")

    if image_path.lower().endswith(".png"):
        mime = "image/png"
    else:
        mime = "image/jpeg"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{image}"
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content