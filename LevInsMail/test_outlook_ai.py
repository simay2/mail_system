
from agent.outlook_reader import get_investment_email
from agent.ai_analyser import analyse_email


def main():
    print("=== LEVINSMAIL — OUTLOOK + AI ===")

    # Извличаме най-новия имейл от Investment
    email = get_investment_email()
    
    print("\n=== ПРИКАЧЕНИ ФАЙЛОВЕ ===")

    if email["attachments"]:
        for attachment in email["attachments"]:
            print(
                f"Тип файл: {attachment['extension']}"
            )
    else:
        print("Няма прикачени файлове.")


    print("Имейлът е извлечен успешно.")
    print("Стартира AI анализ...")

    # Изпращаме имейла към локалния Ollama модел
    result = analyse_email(
        subject=email["subject"],
        body=email["body"],
        received_date=email["received_date"]
    )

    # Български имена на полетата
    field_names = {
        "subject": "Предмет",
        "summary": "Резюме",
        "requested_action": "Искано действие",
        "deadline": "Краен срок",
        "registration_proposal": "Предложение за входиране",
        "priority": "Приоритет",
        "review_status": "Статус на прегледа",
        "incoming_number": "Входящ номер"
    }

    print("\n=== РЕЗУЛТАТ ОТ АНАЛИЗА ===\n")

    for key, label in field_names.items():
        value = result.get(key)
        print(
            f"{label}: "
            f"{value if value is not None else 'Не е посочен'}"
        )


if __name__ == "__main__":
    main()
