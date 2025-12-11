from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str
    memory_id: str
    model: str
