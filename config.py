from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional

class Message(BaseModel):
    role : str 
    content : str
    timestamp : Optional[str] = None
    
    @field_validator('role')
    def role_must_be_valid(cls, value):
        if value not in ['user', 'assistant', 'system']:
            raise ValueError('role must be user, assistant or system!')
        return value

class ChatRequest(BaseModel):
    user_name : str
    message : str
    max_tokens : int = Field(default=1000,gt=1, lt=4000)

class ChatResponse(BaseModel):
    user_name : str
    user_message : str
    ai_response : str
    tokens_used : int

class PersonalityRequest(ChatRequest):
    personality : str

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = Field(default=1000, gt=1, lt=4000)
    database_url: str = "postgresql://postgres:secret@db:5432/chatdb"

    @field_validator("database_url")
    def fix_database_url(cls, value):
        # Railway uses postgres:// but SQLAlchemy needs postgresql://
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql://", 1)
        return value                    

    class Config:
        env_file = ".env"

settings = Settings()
