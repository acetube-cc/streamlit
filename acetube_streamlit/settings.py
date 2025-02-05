from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str | None = Field(None)
    github_token: str | None = Field(None)
    google_api_key: str | None = Field(None)
    supabase_url: str
    supabase_key: str
    runtime_env: Literal["local", "prod-digitalocean"] = Field("dev")
