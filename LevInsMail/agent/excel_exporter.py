
from pathlib import Path
from datetime import date
import xlsxwriter


def export_to_excel(emails):
    """
    Създава Excel отчет с анализираните имейли.

    Подредба:
    №, Подател, Предмет, Резюме, Искано действие,
    Краен срок, Предложение за входиране,
    Приоритет, Статус на преглед, Входящ номер.
    """

    # Папка за готовите отчети
    output_folder = Path("reports")
    output_folder.mkdir(parents=True, exist_ok=True)

    # Име на Excel файла с текущата дата
    filename = f"LevInsMail_{date.today():%Y-%m-%d}.xlsx"
    filepath = output_folder / filename

    # Създаваме Excel документа
    workbook = xlsxwriter.Workbook(str(filepath))
    worksheet = workbook.add_worksheet("Кореспонденция")

    # Заглавия на колоните
    headers = [
        "№",
        "Подател",
        "Предмет",
        "Резюме",
        "Искано действие",
        "Краен срок",
        "Предложение за входиране",
        "Приоритет",
        "Статус на преглед",
        "Входящ номер"
    ]

    # Формат на заглавията
    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#1F4E78",
        "font_color": "#FFFFFF",
        "border": 1,
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True
    })

    # Формат на обикновените клетки
    cell_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "text_wrap": True
    })

    # Цветове за приоритетите
    priority_colors = {
        "Много висок": "#F4B7B7",
        "Висок": "#F8CACA",
        "Среден": "#FFF2B3",
        "Нисък": "#D5EED5"
    }

    # Създаваме отделен формат за всеки приоритет
    priority_formats = {}

    for priority, color in priority_colors.items():
        priority_formats[priority] = workbook.add_format({
            "bg_color": color,
            "border": 1,
            "valign": "top",
            "text_wrap": True
        })

    # Записваме заглавията на първия ред
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Записваме информацията за всеки имейл
    for row, email in enumerate(emails, start=1):

        values = [
            row,
            email.get("sender", ""),
            email.get("subject", ""),
            email.get("summary", ""),
            email.get("requested_action", ""),
            email.get("deadline") or "",
            email.get("registration_proposal", ""),
            email.get("priority", ""),
            email.get("review_status", "За преглед"),
            email.get("incoming_number") or ""
        ]

        for col, value in enumerate(values):

            # По подразбиране използваме обикновен формат
            fmt = cell_format

            # Приоритетът е в колона H (индекс 7)
            if col == 7:
                fmt = priority_formats.get(
                    value,
                    cell_format
                )

            # Записваме текста като данни,
            # без Excel да го интерпретира като формула
            worksheet.write_string(
                row,
                col,
                str(value),
                fmt
            )

        # Височина на редовете
        worksheet.set_row(row, 48)

    # Ширина на колоните
    widths = [
        7,    # A - №
        32,   # B - Подател
        38,   # C - Предмет
        55,   # D - Резюме
        38,   # E - Искано действие
        18,   # F - Краен срок
        29,   # G - Предложение за входиране
        17,   # H - Приоритет
        22,   # I - Статус на преглед
        18    # J - Входящ номер
    ]

    for col, width in enumerate(widths):
        worksheet.set_column(col, col, width)

    # Височина на заглавния ред
    worksheet.set_row(0, 35)

    # Добавяме филтри
    worksheet.autofilter(
        0,
        0,
        max(len(emails), 1),
        len(headers) - 1
    )

    # Заключваме заглавния ред при превъртане
    worksheet.freeze_panes(1, 0)

    # Настройки за печат
    worksheet.set_landscape()
    worksheet.fit_to_pages(1, 0)
    worksheet.repeat_rows(0)

    # Затваряме и записваме Excel файла
    workbook.close()

    return filepath
