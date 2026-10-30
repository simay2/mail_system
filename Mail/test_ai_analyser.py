
from agent.ai_analyser import analyse_email

# Тестов имейл
subject = "Искане за предоставяне на документи"

body = """
Здравейте,

Моля да предоставите справка за извършените
плащания по договор № 123 до 30.10.2026 г.

Поздрави,
Иван Петров
"""

# Извикваме AI анализатора
result = analyse_email(subject, body)

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

print("\n=== ПРЕДЛОЖЕНИЕ ЗА ВХОДИРАНЕ ===\n")

for key, value in result.items():
    label = field_names.get(key, key)

    if value is None:
        value = "Не е посочен"

    print(f"{label}: {value}")
