
import json
from datetime import date, datetime

from ollama import Client
from agent.deadline_manager import (
    determine_deadline_priority,
    extract_relative_deadline
)

# Връзка с локалния Ollama сървър
client = Client(host="http://127.0.0.1:11434")


# Подредба на приоритетите
PRIORITY_LEVELS = {
    "Нисък": 1,
    "Среден": 2,
    "Висок": 3,
    "Много висок": 4
}


def parse_deadline(deadline_text):
    """
    Преобразува текстов краен срок в Python дата.
    """

    if deadline_text is None:
        return None

    deadline_text = deadline_text.strip()
    deadline_text = deadline_text.removesuffix("г.").strip()

    date_formats = [
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%d/%m/%Y"
    ]

    for date_format in date_formats:
        try:
            return datetime.strptime(
                deadline_text,
                date_format
            ).date()
        except ValueError:
            continue

    raise ValueError(
        f"Неразпознат формат на краен срок: {deadline_text}"
    )


def analyse_email(subject, body, received_date=None):
    if received_date is None:
        received_date = date.today()

    # JSON схема за отговора на AI
    schema = {
        "type": "object",
        "properties": {
            "subject": {"type": "string"},
            "summary": {"type": "string"},
            "requested_action": {"type": "string"},
            "deadline": {"type": ["string", "null"]},
            "registration_proposal": {
                "type": "string",
                "enum": [
                    "За входиране",
                    "Не е за входиране",
                    "Необходима проверка"
                ]
            },
            "priority": {
                "type": "string",
                "enum": [
                    "Много висок",
                    "Висок",
                    "Среден",
                    "Нисък"
                ]
            }
        },
        "required": [
            "subject",
            "summary",
            "requested_action",
            "deadline",
            "registration_proposal",
            "priority"
        ],
        "additionalProperties": False
    }

    # Данни от имейла
    email_data = {
        "subject": subject,
        "body": body
    }

    # Изпращаме имейла към AI
    response = client.chat(
        model="company-bg",
        messages=[
            {
                "role": "user",
                "content": (
                    "Анализирай следния имейл. "
                    "Използвай зададените правила. "
                    "Върни само JSON:\n"
                    + json.dumps(
                        email_data,
                        ensure_ascii=False
                    )
                )
            }
        ],
        format=schema,
        options={"temperature": 0},
        think=False
    )

    # Преобразуваме отговора в Python речник
    result = json.loads(response.message.content)

    # Проверка за задължителните полета
    for field in schema["required"]:
        if field not in result:
            raise ValueError(
                f"Липсва задължително поле: {field}"
            )

    # Проверка на предложението за входиране
    if result["registration_proposal"] not in {
        "За входиране",
        "Не е за входиране",
        "Необходима проверка"
    }:
        raise ValueError(
            "Невалидно предложение за входиране."
        )

    # Проверка на приоритета
    if result["priority"] not in PRIORITY_LEVELS:
        raise ValueError("Невалиден приоритет.")

   
    # Проверка за относителен срок в имейла
    relative_deadline = extract_relative_deadline(
        body,
        received_date
    )
     

    if relative_deadline is not None:
        # Преобразуваме датата в единен формат
        result["deadline"] = relative_deadline.strftime(
            "%d.%m.%Y"
        )

    # Проверка и обработка на крайния срок
    deadline_text = result["deadline"]

    if deadline_text is not None:

        try:
            deadline_date = parse_deadline(deadline_text)

            deadline_priority = determine_deadline_priority(
                date.today(),
                deadline_date
            )

            # Запазваме по-високия от двата приоритета
            ai_priority = result["priority"]

            if (
                PRIORITY_LEVELS[deadline_priority]
                > PRIORITY_LEVELS[ai_priority]
            ):
                result["priority"] = deadline_priority

        except (ValueError, TypeError):
            # Непознат срок: сигнал за човешка проверка
            result["registration_proposal"] = (
                "Необходима проверка"
            )
            result["priority"] = "Много висок"

            print(
                f"ВНИМАНИЕ: Неразпознат краен срок: "
                f"{deadline_text}"
            )

    # Полета за човешки преглед
    result["review_status"] = "За преглед"
    result["incoming_number"] = None

    return result
