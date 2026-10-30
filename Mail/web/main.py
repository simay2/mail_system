
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from httpx import request
from agent.outlook_reader import get_investment_emails
from uuid import uuid4
from fastapi import HTTPException
from agent.outlook_reader import get_email_by_id
from agent.ai_analyser import analyse_email

app = FastAPI(title="LevInsMail")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# Временен регистър за избор на имейли.
# Съдържа само Outlook идентификатори,
# а не текстовете на съобщенията.
email_registry = {}



def prepare_emails_for_display(emails):

    prepared_emails = []

    for email in emails:

        # Проверяваме дали вече имаме идентификатор
        # за този конкретен Outlook имейл
        temporary_id = None

        for existing_id, stored_email in email_registry.items():

            if (
                stored_email["entry_id"] == email["entry_id"]
                and stored_email["store_id"] == email["store_id"]
            ):
                temporary_id = existing_id
                break

        # Създаваме нов само ако не съществува
        if temporary_id is None:
            temporary_id = str(uuid4())

            email_registry[temporary_id] = {
                "entry_id": email["entry_id"],
                "store_id": email["store_id"]
            }

        display_email = {
            key: value
            for key, value in email.items()
            if key not in {"entry_id", "store_id"}
        }

        display_email["temporary_id"] = temporary_id

        prepared_emails.append(display_email)

    return prepared_emails


# Измислени имейли за тестване на интерфейса
test_emails = [
    {
        "subject": "Искане за справка",
        "summary": "Клиент иска справка за плащания по договор №123.",
        "requested_action": "Предоставяне на справка",
        "deadline": "30.10.2026",
        "registration_proposal": "Не е за входиране",
        "priority": "Много висок"
    },
    {
        "subject": "Жалба за фактура",
        "summary": "Клиент оспорва начислена сума по фактура.",
        "requested_action": "Проверка и писмен отговор",
        "deadline": None,
        "registration_proposal": "Необходима проверка",
        "priority": "Среден"
    },
    {
        "subject": "Рекламно предложение",
        "summary": "Предложение за маркетингови услуги.",
        "requested_action": "Не се изисква действие",
        "deadline": None,
        "registration_proposal": "Не е за входиране",
        "priority": "Нисък"
    }
]




@app.get("/")
def home(request: Request):
    emails = get_investment_emails(limit=5)

    prepared_emails = prepare_emails_for_display(
        emails
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"emails": prepared_emails}
    )



@app.post("/analyse/{temporary_id}")
def analyse_selected_email(
    request: Request,
    temporary_id: str
):
    selected_email = email_registry.get(temporary_id)

    if selected_email is None:
        raise HTTPException(
            status_code=404,
            detail="Имейлът не е намерен. Обновете страницата."
        )

    # Извличаме конкретния имейл от Outlook
    email = get_email_by_id(
        selected_email["entry_id"],
        selected_email["store_id"]
    )

    # Анализираме имейла чрез Ollama
    result = analyse_email(
        subject=email["subject"],
        body=email["body"],
        received_date=email["received_date"]
    )

    # Показваме анализа в новата HTML страница
    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context={
            "request": request,
            "analysis": result
        }
    )

