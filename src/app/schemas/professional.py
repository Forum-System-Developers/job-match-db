import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.custom_types import Username
from app.schemas.job_ad import JobAdPreview
from app.sql_app.professional.professional import Professional
from app.sql_app.professional.professional_status import ProfessionalStatus


class PrivateMatches(BaseModel):
    status: bool


class ProfessionalBase(BaseModel):
    first_name: str
    last_name: str
    description: str
    city_id: UUID


class ProfessionalCreate(ProfessionalBase):
    """
    ProfessionalCreate schema for creating a new professional user.

    Attributes:
        username (Username): The username of the professional user.
        password_hash (str): The hashed password of the professional user.
        email (EmailStr): The email address of the professional user.
    """

    username: Username  # type: ignore
    password_hash: str
    email: EmailStr

    @field_validator("password")
    def _validate_password(cls, value: str) -> str:
        if not re.match(
            r"^(?=.*\d)(?=.*[!@#$%^&*()\-_=+\\|;:'\",.<>/?]).{8,}$",
            value,
        ):
            raise ValueError(
                "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return value

    class Config:
        from_attributes = True


class ProfessionalUpdate(BaseModel):
    first_name: str | None = Field(examples=["Jane"], default=None)
    last_name: str | None = Field(examples=["Doe"], default=None)
    description: str | None = Field(
        examples=["A seasoned web developer with expertise in FastAPI"], default=None
    )
    city: str | None = Field(examples=["Sofia"], default=None)


class ProfessionalResponse(ProfessionalBase):
    """
    Pydantic schema representing the FastAPI response for Professional.

    Attributes:
        first_name (str): First name of the professional.
        last_name (str): Last name of the professional.
        description (str): Description of the professional.
        photo bytes | None: Photo of the professional.
        active_application_count (int): Number of active applications.
        city (str): The city the professional is located in.

    """

    id: UUID
    email: EmailStr
    photo: bytes | None = None
    status: ProfessionalStatus
    active_application_count: int
    matched_ads: list[JobAdPreview] | None = None

    @classmethod
    def create(
        cls,
        professional: Professional,
        matched_ads: list[JobAdPreview] | None = None,
    ) -> "ProfessionalResponse":
        return cls(
            id=professional.id,
            first_name=professional.first_name,
            last_name=professional.last_name,
            email=professional.email,
            city_id=professional.city_id,
            description=professional.description,
            photo=professional.photo,
            status=professional.status,
            active_application_count=professional.active_application_count,
            matched_ads=matched_ads if not professional.has_private_matches else None,
        )

    class Config:
        json_encoders = {bytes: lambda v: "<binary data>"}
