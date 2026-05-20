from openai import OpenAI

from app.settings import Settings


def ask_openai(question: str, settings: Settings) -> str:
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.openai_model,
        instructions=settings.bot_system_prompt,
        input=question,
    )
    answer = response.output_text.strip()
    return answer or "我沒有產生可回覆的內容，請再試一次。"
