# LINE OpenAI Bot

FastAPI app for a LINE Messaging API bot that can be invited into LINE groups and answer questions with the OpenAI API.

## Features

- FastAPI webhook endpoint for LINE Messaging API.
- LINE SDK v3 signature validation and reply messages.
- OpenAI Responses API integration.
- Group chat control: replies in 1:1 chats by default, and in groups only when triggered by `/ask` or a configured bot mention.

## Setup

1. Create and activate a Python virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in:

   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`

4. Run the app.

   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Expose the local server while developing, for example with ngrok.

   ```powershell
   ngrok http 8000
   ```

6. In the LINE Developers console, set the webhook URL to:

   ```text
   https://your-public-domain.example/callback
   ```

## Group Usage

Invite the LINE bot into a group and send:

```text
/ask 幫我摘要這段文字...
```

Direct 1:1 messages always receive a reply. Group or room messages only receive a reply when:

- the text starts with `BOT_TRIGGER_PREFIX`, default `/ask`;
- or `LINE_BOT_USER_ID` / `LINE_BOT_MENTION_NAME` is configured and the bot is mentioned.

## Health Check

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```

## References

- OpenAI Responses API: https://platform.openai.com/docs/api-reference/responses
- OpenAI quickstart: https://platform.openai.com/docs/quickstart
- LINE Python SDK: https://github.com/line/line-bot-sdk-python
