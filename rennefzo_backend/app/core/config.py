from typing import List
from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import json
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Rennefzo API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings - store as string to avoid pydantic_settings JSON parsing issues
    # Use Field with validation_alias to map from BACKEND_CORS_ORIGINS env var
    BACKEND_CORS_ORIGINS_RAW: str = Field(
        default='["*"]',
        validation_alias='BACKEND_CORS_ORIGINS'
    )
    
    @field_validator('BACKEND_CORS_ORIGINS_RAW', mode='before')
    @classmethod
    def parse_cors_origins_raw(cls, v):
        """Handle CORS origins from environment variable."""
        # Handle None or empty string
        if v is None or (isinstance(v, str) and not v.strip()):
            return '["*"]'
        # If already a list (from default), convert to JSON string
        if isinstance(v, list):
            return json.dumps(v)
        # Return as string
        return str(v)
    
    @computed_field
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        """Parse CORS origins from string to list."""
        try:
            parsed = json.loads(self.BACKEND_CORS_ORIGINS_RAW)
            if isinstance(parsed, list):
                return parsed
            # Single value, wrap in list
            return [str(parsed)]
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, treat as single origin string
            return [self.BACKEND_CORS_ORIGINS_RAW] if self.BACKEND_CORS_ORIGINS_RAW else ["*"]
    
    # Database settings - MySQL
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/rennefzo"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()

