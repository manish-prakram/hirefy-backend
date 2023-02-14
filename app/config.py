from pydantic import BaseSettings


class Setting(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    email_host: str
    email_port: int
    email_username: str
    email_password: str
    email_from: str

    cd_cloud_name: str
    cd_api_key: str
    cd_api_secret: str

    class Config:
        env_file = ".env"


settings = Setting()
