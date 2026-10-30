
from datetime import datetime, timedelta

import pythoncom
import win32com.client


# Пощенска кутия, която LevInsMail ще обработва
MAILBOX_NAME = "Head"


def get_head_inbox(namespace):
    """
    Намира пощенската кутия Head
    и нейната папка Inbox.
    """

    head_store = None

    for store in namespace.Stores:
        if store.DisplayName.strip().lower() == MAILBOX_NAME.lower():
            head_store = store
            break

    if head_store is None:
        raise RuntimeError(
            f"Пощенската кутия {MAILBOX_NAME} не е намерена."
        )

    root = head_store.GetRootFolder()
    inbox = None

    for folder in root.Folders:
        if folder.Name.strip().lower() in ("inbox", "входящи"):
            inbox = folder
            break

    if inbox is None:
        raise RuntimeError(
            f"Inbox не е намерен в {MAILBOX_NAME}."
        )

    return head_store, inbox


def get_investment_email(limit=10):
    """
    Запазено е старото име на функцията,
    за да не се нарушат съществуващите тестове.

    Вече чете от Head, не от Investment.
    Връща най-новия имейл.
    """

    pythoncom.CoInitialize()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        head_store, inbox = get_head_inbox(namespace)

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        for message in messages:
            if message.Class != 43:
                continue

            attachments = []

            for attachment in message.Attachments:
                filename = attachment.FileName

                extension = (
                    filename.rsplit(".", 1)[-1].lower()
                    if "." in filename
                    else ""
                )

                attachments.append({
                    "filename": filename,
                    "extension": extension
                })

            return {
                "subject": message.Subject or "",
                "body": message.Body or "",
                "received_date": message.ReceivedTime.date(),
                "attachment_count": message.Attachments.Count,
                "attachments": attachments
            }

        raise RuntimeError(
            f"Няма намерени имейли в {MAILBOX_NAME} → Inbox."
        )

    finally:
        pythoncom.CoUninitialize()


def get_investment_emails(limit=10):
    """
    Връща последните имейли от Head
    за показване в уеб интерфейса.

    Старото име е запазено за съвместимост.
    """

    pythoncom.CoInitialize()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        head_store, inbox = get_head_inbox(namespace)

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        emails = []

        for message in messages:
            if message.Class != 43:
                continue

            emails.append({
                "entry_id": message.EntryID,
                "store_id": head_store.StoreID,
                "subject": message.Subject or "(Без предмет)",
                "sender": message.SenderName or "",
                "received_date": message.ReceivedTime.strftime(
                    "%d.%m.%Y %H:%M"
                ),
                "summary": "Все още не е анализиран",
                "deadline": None,
                "registration_proposal": "За преглед",
                "priority": "Неопределен"
            })

            if len(emails) >= limit:
                break

        return emails

    finally:
        pythoncom.CoUninitialize()


def get_email_by_id(entry_id, store_id):
    """
    Извлича конкретен имейл от Head → Inbox
    чрез EntryID и StoreID.
    """

    pythoncom.CoInitialize()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        head_store, head_inbox = get_head_inbox(namespace)

        # Не допускаме друга пощенска кутия
        if store_id != head_store.StoreID:
            raise RuntimeError(
                "Неразрешено пощенско хранилище."
            )

        message = namespace.GetItemFromID(
            entry_id,
            store_id
        )

        if message is None or message.Class != 43:
            raise RuntimeError(
                "Съобщението не е намерено."
            )

        # Проверяваме дали писмото е в Head → Inbox
        parent_folder = message.Parent

        if parent_folder.EntryID != head_inbox.EntryID:
            raise RuntimeError(
                "Имейлът не принадлежи на Head → Inbox."
            )

        return {
            "subject": message.Subject or "",
            "body": message.Body or "",
            "received_date": message.ReceivedTime.date()
        }

    finally:
        pythoncom.CoUninitialize()


def get_emails_for_analysis(limit=5):
    """
    Извлича последните няколко имейла от Head
    за анализ с Ollama.
    """

    emails = get_investment_emails(limit=limit)
    result = []

    for email in emails:
        full_email = get_email_by_id(
            email["entry_id"],
            email["store_id"]
        )

        result.append({
            "subject": full_email["subject"],
            "body": full_email["body"],
            "received_date": full_email["received_date"]
        })

    return result


def get_emails_last_24_hours():
    """
    Извлича всички имейли от Head → Inbox,
    получени през последните 24 часа.

    Използва се от generate_daily_report.py.
    """

    pythoncom.CoInitialize()

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        head_store, inbox = get_head_inbox(namespace)

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        now = datetime.now().astimezone()
        start_time = now - timedelta(hours=24)

        emails = []

        for message in messages:
            if message.Class != 43:
                continue

            received = message.ReceivedTime.astimezone(
                now.tzinfo
            )

            if received < start_time:
                break

            if received > now:
                continue

            emails.append({
                "subject": message.Subject or "(Без предмет)",
                "body": message.Body or "",
                "received_date": received.date()
            })

        return emails

    finally:
        pythoncom.CoUninitialize()



if __name__ == "__main__":
    print("Проверка на Head за последните 24 часа...")

    emails = get_emails_last_24_hours()

    print(f"Намерени имейли: {len(emails)}")

    print("Проверката приключи успешно.")

