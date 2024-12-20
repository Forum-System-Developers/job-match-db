import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.custom_types import Username
from app.schemas.job_ad import JobAdPreview
from app.schemas.match import MatchRequestAd
from app.schemas.skill import SkillResponse
from app.sql_app.professional.professional import Professional
from app.sql_app.professional.professional_status import ProfessionalStatus


class PrivateMatches(BaseModel):
    status: bool


class ProfessionalBase(BaseModel):
    first_name: str
    last_name: str
    description: str
    city: str


class ProfessionalCreate(BaseModel):
    """
    ProfessionalCreate schema for creating a new professional user.

    Attributes:
        username (Username): The username of the professional user.
        password_hash (str): The hashed password of the professional user.
        email (EmailStr): The email address of the professional user.
    """

    sub: str | None = None
    first_name: str
    last_name: str
    description: str
    city_id: UUID
    username: Username  # type: ignore
    password_hash: str
    email: EmailStr

    class Config:
        from_attributes = True


class ProfessionalUpdate(BaseModel):
    first_name: str | None = Field(examples=["Jane"], default=None)
    last_name: str | None = Field(examples=["Doe"], default=None)
    description: str | None = Field(
        examples=["A seasoned web developer with expertise in FastAPI"], default=None
    )
    city_id: UUID | None = Field(description="City ID", default=None)
    status: ProfessionalStatus | None = Field(examples=["active"], default=None)


class ProfessionalResponse(ProfessionalBase):
    """
    Pydantic schema representing the FastAPI response for Professional.

    Attributes:
        id (UUID): The identifier of the professional.
        first_name (str): First name of the professional.
        last_name (str): Last name of the professional.
        description (str): Description of the professional.
        photo bytes | None: Photo of the professional.
        active_application_count (int): Number of active applications.
        city (str): The city the professional is located in.
        status (ProfessionalStatus): The status of the professional.
        skills (list[SkillResponse]): List of Professional Skills.
        matched_ads (list[JobAdPreview] | None): List of matched job ads.

    """

    id: UUID
    email: EmailStr
    photo: bytes | None = None
    status: ProfessionalStatus
    skills: list[SkillResponse] = []
    active_application_count: int
    matched_ads: list[JobAdPreview] | None = None
    sent_match_requests: list[MatchRequestAd] | None = None

    @classmethod
    def create(
        cls,
        professional: Professional,
        skills: list[SkillResponse] = [],
        matched_ads: list[JobAdPreview] | None = None,
        sent_match_requests: list[MatchRequestAd] | None = None,
    ) -> "ProfessionalResponse":
        return cls(
            id=professional.id,
            first_name=professional.first_name,
            last_name=professional.last_name,
            email=professional.email,
            city=professional.city.name,
            description=professional.description,
            photo=professional.photo,
            status=professional.status,
            skills=skills,
            active_application_count=professional.active_application_count,
            matched_ads=matched_ads if not professional.has_private_matches else None,
            sent_match_requests=sent_match_requests,
        )

    class Config:
        json_encoders = {bytes: lambda v: "<binary data>"}
