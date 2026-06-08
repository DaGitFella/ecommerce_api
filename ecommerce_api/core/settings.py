from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # Application settings
    APP_NAME: str = 'E-commerce API'
    APP_VERSION: str = '0.1.0'
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str 
    