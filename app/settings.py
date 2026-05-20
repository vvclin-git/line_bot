from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    line_channel_access_token: str
    line_channel_secret: str
    openai_api_key: str
    openai_model: str = "gpt-5.2"
    bot_trigger_prefix: str = "/ask"
    line_bot_user_id: str = ""
    line_bot_mention_name: str = ""
    bot_system_prompt: str = (
        "You are a helpful assistant in a LINE group chat. "
        "Reply in Traditional Chinese by default unless the user asks for another language."
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
