
from ollama import Client

# Връзка с локалния Ollama сървър
client = Client(host="http://127.0.0.1:11434")

# Измислен тестов имейл
test_email = """
Здравейте,

Имам неправилно начислена сума по фактура.
Моля за спешна проверка и съдействие.

Поздрави,
Иван Петров
"""

# Изпращаме имейла за анализ
response = client.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "system",
            "content": (
                "Ти си AI асистент за анализ на фирмени имейли. "
                "Отговаряй само на български език. "
                "Определи категория, приоритет и кратко резюме."
            )
        },
        {
            "role": "user",
            "content": test_email
        }
    ],
    options={
        "temperature": 0
    },
    think=False
)

print("=== AI АНАЛИЗ ===")
print(response.message.content)
