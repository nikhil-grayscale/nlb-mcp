"""Environment configuration for the NLB MCP server."""

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    nlb_api_key: str = Field(..., alias="NLB_API_KEY")
    nlb_app_code: str = Field(..., alias="NLB_APP_CODE")
    nlb_api_base: AnyUrl = Field(
        "https://openweb.nlb.gov.sg/api/v2/Catalogue", alias="NLB_API_BASE"
    )
    request_timeout_ms: int = Field(10_000, alias="REQUEST_TIMEOUT_MS", gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Singleton settings instance
settings = Settings()
