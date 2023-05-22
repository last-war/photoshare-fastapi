from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@server:5432/database'
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    cloudinary_name: str = 'name'
    cloudinary_api_key: str = 'key'
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
