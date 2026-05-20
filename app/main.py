import asyncio
import logging

from fastapi import FastAPI, Header, HTTPException, Request
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent

from app.line_service import reply_text, should_respond
from app.openai_service import ask_openai
from app.settings import get_settings

logger = logging.getLogger(__name__)

app = FastAPI(title="LINE OpenAI Bot")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(default="")) -> dict[str, str]:
    settings = get_settings()
    body = (await request.body()).decode("utf-8")
    parser = WebhookParser(settings.line_channel_secret)

    try:
        events = parser.parse(body, x_line_signature)
    except InvalidSignatureError as exc:
        raise HTTPException(status_code=400, detail="Invalid LINE signature") from exc

    for event in events:
        if not isinstance(event, MessageEvent):
            continue

        respond, question = should_respond(event, settings)
        if not respond:
            continue

        try:
            answer = await asyncio.to_thread(ask_openai, question, settings)
            await asyncio.to_thread(reply_text, event.reply_token, answer, settings)
        except Exception:
            logger.exception("Failed to process LINE message")
            await asyncio.to_thread(
                reply_text,
                event.reply_token,
                "處理訊息時發生錯誤，請稍後再試。",
                settings,
            )

    return {"status": "ok"}
