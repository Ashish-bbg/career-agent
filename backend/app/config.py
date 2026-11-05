from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_provider: str
    llm_model: str
    
    gemini_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()