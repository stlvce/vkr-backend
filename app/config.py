from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, case_sensitive=True):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


class AppSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int


class DatabaseSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="MYSQL_")

    HOST: str
    USER: str
    PASSWORD: str
    DB: str

    @property
    def db_url(self):
        return f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DB}"


app_settings = AppSettings()
db_settings = DatabaseSettings()
