# The reason to ignore "assignment" https://github.com/pydantic/pydantic/issues/3143
# mypy: disable-error-code="assignment"
from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str
    DATABASE_URL: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    VERSION: str = "9.9.9.9"

    @field_validator("BACKEND_CORS_ORIGINS", check_fields=False)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        else:
            return v

    PROJECT_NAME: str = "JobMatchDB"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        allow_extra = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
