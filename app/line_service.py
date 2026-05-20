from linebot.v3.messaging import ApiClient, Configuration, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.settings import Settings


def should_respond(event: MessageEvent, settings: Settings) -> tuple[bool, str]:
    if not isinstance(event.message, TextMessageContent):
        return False, ""

    text = event.message.text.strip()
    if not text:
        return False, ""

    source_type = getattr(event.source, "type", "")
    if source_type == "user":
        return True, text

    prefixed = text.startswith(settings.bot_trigger_prefix)
    mentioned = _mentions_bot(event, text, settings)

    if not prefixed and not mentioned:
        return False, ""

    cleaned = text
    if prefixed:
        cleaned = cleaned[len(settings.bot_trigger_prefix) :].strip()
    if settings.line_bot_mention_name:
        cleaned = cleaned.replace(f"@{settings.line_bot_mention_name}", "").strip()

    return bool(cleaned), cleaned


def reply_text(reply_token: str, text: str, settings: Settings) -> None:
    configuration = Configuration(access_token=settings.line_channel_access_token)
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=_fit_line_text(text))],
            )
        )


def _mentions_bot(event: MessageEvent, text: str, settings: Settings) -> bool:
    if settings.line_bot_mention_name and f"@{settings.line_bot_mention_name}" in text:
        return True

    if not settings.line_bot_user_id:
        return False

    mention = getattr(event.message, "mention", None)
    mentions = getattr(mention, "mentionees", []) if mention else []
    return any(getattr(item, "user_id", "") == settings.line_bot_user_id for item in mentions)


def _fit_line_text(text: str) -> str:
    # LINE text messages are limited; keep a small suffix budget for truncation text.
    limit = 4900
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n（回覆過長，已截斷）"
