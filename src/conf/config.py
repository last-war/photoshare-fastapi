from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str = 'PythonStudent@meta.ua'
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    origins: str
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
