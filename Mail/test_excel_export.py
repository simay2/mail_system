
from agent.excel_exporter import export_to_excel

# Примерни резултати от AI анализ
test_emails = [
    {
        "subject": "Жалба относно начислена сума",
        "summary": "Клиент оспорва начислена сума по договор.",
        "requested_action": "Проверка и писмен отговор.",
        "deadline": "30.10.2026",
        "registration_proposal": "За входиране",
        "priority": "Много висок",
        "review_status": "За преглед",
        "incoming_number": None
    },
    {
        "subject": "Искане за справка по договор",
        "summary": "Клиент иска справка за извършени плащания.",
        "requested_action": "Изготвяне на справка.",
        "deadline": None,
        "registration_proposal": "Не е за входиране",
        "priority": "Среден",
        "review_status": "За преглед",
        "incoming_number": None
    },
    {
        "subject": "Представяне на услуги",
        "summary": "Фирма предлага нови услуги.",
        "requested_action": "Не се изисква действие.",
        "deadline": None,
        "registration_proposal": "Не е за входиране",
        "priority": "Нисък",
        "review_status": "За преглед",
        "incoming_number": None
    },
    {
        "subject": "Уведомление с кратък срок",
        "summary": "Получено е уведомление, изискващо реакция.",
        "requested_action": "Проверка на съдържанието и предприемане на действия.",
        "deadline": "04.11.2026",
        "registration_proposal": "Необходима проверка",
        "priority": "Висок",
        "review_status": "За преглед",
        "incoming_number": None
    }
]

filepath = export_to_excel(test_emails)

print("Excel файлът е създаден успешно:")
print(filepath)
