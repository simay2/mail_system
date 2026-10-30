
from agent.ai_analyser import analyse_email
print("СТАРТИРАМ ТЕСТА")
test_emails = [
    {
        "subject": "Жалба за начислена сума",
        "body": (
            "Здравейте, оспорвам начислената сума "
            "по фактура № 456. Моля за проверка "
            "и писмен отговор."
        )
    },
    {
        "subject": "Искане за справка",
        "body": (
            "Моля да предоставите справка за "
            "извършените плащания по договор № 123 "
            "до 30.10.2026 г."
        )
    },
    {
        "subject": "Представяне на услуги",
        "body": (
            "Здравейте, предлагаме маркетингови "
            "услуги за вашата компания. "
            "Свържете се с нас при интерес."
        )
    },
    {
        "subject": "Спешен технически проблем",
        "body": (
            "Системата ни не работи и не можем "
            "да обработваме заявки. Моля за "
            "незабавно съдействие."
        )
    },
    {
        "subject": "Информационно уведомление",
        "body": (
            "Уведомяваме ви, че от следващия месец "
            "ще използваме нов фирмен телефонен номер. "
            "Не се изисква отговор."
        )
    },
    {
    "subject": "Искане за документи",
    "body": (
        "Здравейте, моля да предоставите "
        "необходимите документи до 5 работни дни."
    )
    }
]

field_names = {
    "subject": "Предмет",
    "summary": "Резюме",
    "requested_action": "Искано действие",
    "deadline": "Краен срок",
    "registration_proposal": "Предложение за входиране",
    "priority": "Приоритет"
}

for number, email in enumerate(test_emails, start=1):
    print(f"\n{'=' * 55}")
    print(f"ИМЕЙЛ № {number}")
    print(f"{'=' * 55}")

    try:
        result = analyse_email(
            email["subject"],
            email["body"]
        )

        for key, label in field_names.items():
            value = result.get(key)
            print(
                f"{label}: "
                f"{value if value is not None else 'Не е посочен'}"
            )

    except Exception as error:
        print(f"Грешка при анализа: {error}")
