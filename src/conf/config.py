from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'samlpe'
    #database_drive: str = 'postgresql+psycopg2:/postgres'
    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'secret'
    postgres_server: str = 'localhost'
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    cloudinary_name: str = 'name'
    cloudinary_api_key: str = 'key'
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
