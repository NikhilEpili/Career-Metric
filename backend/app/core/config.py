import json
from functools import lru_cache
from typing import Any, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_parse_none_str="None",
    )

    PROJECT_NAME: str = Field(default="Career Metric")
    VERSION: str = Field(default="0.1.0")
    API_V1_STR: str = Field(default="/v1")
    # Accept as string from env, will be converted to List[str] by validator
    BACKEND_CORS_ORIGINS: str | List[str] = Field(
        default="http://localhost,http://localhost:3000,http://localhost:5173"
    )

    SECRET_KEY: str = Field(default="change-me")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)

    POSTGRES_SERVER: str = Field(default="db")
    POSTGRES_USER: str = Field(default="career_metric")
    POSTGRES_PASSWORD: str = Field(default="career_metric")
    POSTGRES_DB: str = Field(default="career_metric")
    POSTGRES_PORT: str = Field(default="5432")

    REDIS_URL: str | None = Field(default=None)

    FIRST_SUPERUSER_EMAIL: str = Field(default="admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = Field(default="ChangeMe123!")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: Any) -> List[str]:
        """Parse CORS origins from string or list format."""
        # Handle None or empty values
        if value is None or value == "":
            return [
                "http://localhost",
                "http://localhost:3000",
                "http://localhost:5173",
            ]
        
        # If it's already a list, ensure all items are strings
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        
        # If it's a string, try to parse it
        if isinstance(value, str):
            # Try JSON parsing first (for array format)
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(origin).strip() for origin in parsed if str(origin).strip()]
            except (json.JSONDecodeError, TypeError):
                pass
            
            # Fall back to comma-separated string
            origins = [origin.strip() for origin in value.split(",") if origin.strip()]
            if origins:
                return origins
        
        # Last resort: convert to string and try to parse
        try:
            str_value = str(value)
            origins = [origin.strip() for origin in str_value.split(",") if origin.strip()]
            if origins:
                return origins
        except Exception:
            pass
        
        # Final fallback: return defaults
        return [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list of strings."""
        if isinstance(self.BACKEND_CORS_ORIGINS, list):
            return [str(origin) for origin in self.BACKEND_CORS_ORIGINS]
        # It's a string, parse it
        return self.assemble_cors_origins(self.BACKEND_CORS_ORIGINS)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
