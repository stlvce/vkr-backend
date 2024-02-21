from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, MySQLDsn


class Settings(BaseSettings, case_sensitive=True):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class DatabaseSettings(Settings):
    model_config = SettingsConfigDict(env_prefix="MYSQL_")

    HOST: str
    USER: str
    PASSWORD: str
    DB: str

    @property
    def db_url(self):
        # return MySQLDsn.build(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB)
        return f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DB}"


db_settings = DatabaseSettings()
