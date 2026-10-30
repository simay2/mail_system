from datetime import date, timedelta
import holidays
import re


def calculate_working_days(start_date, end_date):
    working_days = 0
    current_date = start_date

    # Официални празници в България
    bg_holidays = holidays.country_holidays(
        "BG",
        observed=True
    )

    while current_date < end_date:
        current_date += timedelta(days=1)

        is_weekday = current_date.weekday() < 5
        is_holiday = current_date in bg_holidays

        if is_weekday and not is_holiday:
            working_days += 1

    return working_days


def determine_deadline_priority(start_date, end_date):

    # Проверка за просрочен срок
    if end_date < start_date:
        return "Много висок"

    # Изчисляване на оставащите работни дни
    days = calculate_working_days(
        start_date,
        end_date
    )

    if days <= 3:
        return "Много висок"

    elif days <= 7:
        return "Висок"

    else:
        return "Среден"


def add_working_days(start_date, number_of_days):
    """
    Изчислява крайна дата след определен
    брой работни дни.
    """

    if number_of_days < 0:
        raise ValueError(
            "Броят работни дни не може да е отрицателен."
        )

    bg_holidays = holidays.country_holidays(
        "BG",
        observed=True
    )

    current_date = start_date
    counted_days = 0

    while counted_days < number_of_days:
        current_date += timedelta(days=1)

        is_weekday = current_date.weekday() < 5
        is_holiday = current_date in bg_holidays

        if is_weekday and not is_holiday:
            counted_days += 1

    return current_date


def extract_relative_deadline(text, received_date):
    """
    Разпознава срок от вида:
    'до 5 работни дни'
    и изчислява крайната дата.
    """

    pattern = r"(?:до|в срок до)\s+(\d+)\s+работни\s+дни"

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    if match is None:
        return None

    number_of_days = int(match.group(1))

    return add_working_days(
        received_date,
        number_of_days
    )
