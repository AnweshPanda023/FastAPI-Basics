from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    debug: bool

    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    password_reset_token_expire_minutes: int
    smtp_host: str
    smtp_port: int
    smtp_username: str | None = None
    smtp_password: str | None = None

    email_from: str
    frontend_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
