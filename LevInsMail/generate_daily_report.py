
from datetime import datetime

from agent.outlook_reader import get_emails_last_24_hours
from agent.ai_analyser import analyse_email
from agent.excel_exporter import export_to_excel


def generate_daily_report():
    print("=== LevInsMail: Генериране на Excel отчет ===")

    # За първия тест обработваме само 5 имейла
    emails = get_emails_last_24_hours()

    print(f"Намерени имейли: {len(emails)}")

    analysed_emails = []

    for index, email in enumerate(emails, start=1):
        print(f"\nАнализиране на имейл {index}/{len(emails)}")

        try:
            analysis = analyse_email(
                subject=email["subject"],
                body=email["body"],
                received_date=email["received_date"]
            )

            analysed_emails.append(analysis)

            print("Успешно анализиран.")

        except Exception as error:
            print(f"Грешка при анализа: {error}")

            # Запазваме имейла в отчета,
            # дори когато AI анализът е неуспешен.
            analysed_emails.append({
                "subject": email["subject"],
                "summary": "AI анализът не е завършен.",
                "requested_action": "Необходим е ръчен преглед.",
                "deadline": None,
                "registration_proposal": "Необходима проверка",
                "priority": "Много висок",
                "review_status": "За преглед",
                "incoming_number": None
            })

    filepath = export_to_excel(analysed_emails)

    print("\n=== ОТЧЕТЪТ Е ГОТОВ ===")
    print(f"Файл: {filepath}")
    print(f"Дата на генериране: {datetime.now():%d.%m.%Y %H:%M}")


if __name__ == "__main__":
    generate_daily_report()
