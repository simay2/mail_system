
from datetime import date
from agent.ai_analyser import analyse_email

# Имейл, получен преди няколко дни
subject = "Искане за документи"

body = """
Здравейте,

Моля да предоставите документите
до 5 работни дни от получаването
на настоящия имейл.

Поздрави
"""

# Дата на получаване, а не дата на обработка
received_date = date(2026, 10, 20)

result = analyse_email(
    subject,
    body,
    received_date=received_date
)

print("=== ПРОВЕРКА НА ДАТАТА НА ПОЛУЧАВАНЕ ===")
print(f"Получен на: {received_date}")
print(f"Краен срок: {result['deadline']}")
print(f"Приоритет: {result['priority']}")
print(f"Предложение за входиране: {result['registration_proposal']}")
