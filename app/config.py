# pydantic for performing the validation for our environment variables
from pydantic_settings import BaseSettings

# it is to validate the datas that we are getting from environment variables


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = ".env"


settings = Settings()
