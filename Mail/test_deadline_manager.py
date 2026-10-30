from datetime import date
from agent.deadline_manager import extract_relative_deadline
from agent.deadline_manager import (
    calculate_working_days,
    add_working_days
)

# ТЕСТ 1: Изчисляване на работни дни
start_date = date(2026, 12, 23)
end_date = date(2026, 12, 31)

days = calculate_working_days(start_date, end_date)

print("=== ТЕСТ 1: РАБОТНИ ДНИ ===")
print(f"Начална дата: {start_date}")
print(f"Краен срок: {end_date}")
print(f"Оставащи работни дни: {days}")


# ТЕСТ 2: Изчисляване на относителен срок
received_date = date(2026, 10, 27)

calculated_deadline = add_working_days(
    received_date,
    5
)

print("\n=== ТЕСТ 2: ОТНОСИТЕЛЕН СРОК ===")
print(f"Получен имейл: {received_date}")
print("Посочен срок: 5 работни дни")
print(f"Изчислен краен срок: {calculated_deadline}")


email_text = (
    "Здравейте, моля да предоставите "
    "справката до 5 работни дни."
)

received_date = date(2026, 10, 27)

deadline = extract_relative_deadline(
    email_text,
    received_date
)

print("\n=== ТЕСТ 3: СРОК ОТ ИМЕЙЛ ===")
print(f"Извлечен краен срок: {deadline}")