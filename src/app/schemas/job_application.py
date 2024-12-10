from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator
from sqlalchemy.orm import Session

from app.schemas.city import City
from app.schemas.custom_types import Salary
from app.schemas.professional import ProfessionalResponse
from app.schemas.skill import SkillBase, SkillResponse
from app.sql_app.job_application.job_application import JobApplication
from app.sql_app.professional.professional import Professional


class JobStatus(str, Enum):
    """

    Attributes:
        ACTIVE: Appears in Company searches.
        PRIVATE: Can only be seen by the Creator.
        HIDDEN: Accessible only by ID.
    """

    ACTIVE = "active"
    PRIVATE = "private"
    HIDDEN = "hidden"


class JobSearchStatus(str, Enum):
    """

    Attributes:
        ACTIVE: Appears in Company searches.
        MATCHED: Matched with Job Ad.
    """

    ACTIVE = "active"
    MATCHED = "matched"


class MatchResponseRequest(BaseModel):
    accept_request: bool


class JobAplicationBase(BaseModel):
    """
    Pydantic model for creating or updating a professional's job application.

    This model is used to capture the basic information required to reate or update a job application. It includes the required attributes description, application status, and a list of Applicant skills. Optional attributes are minimum and maximum salary range, an city for the application. The data should be passed as a JSON object in the request body.

    Attributes:
        min_salary (int): The lower boundary for the salary range.
        max_salary (int): The upper boundary for the salary range.
        description (str): Description of the professional.
        skills (list[str]): List of Professional Skills.
        city (str): The city the professional is located in.
    """

    name: str = Field(examples=["Job Application"])
    min_salary: float | None = Field(
        ge=0, description="Minimum salary (>= 0)", default=None
    )
    max_salary: float | None = Field(
        ge=0, description="Maximum salary (>= 0)", default=None
    )

    description: str = Field(
        examples=["A seasoned web developer with expertise in FastAPI"]
    )

    @model_validator(mode="before")
    def validate_salary_range(cls, values):
        min_salary = values.get("min_salary")
        max_salary = values.get("max_salary")
        if (min_salary and max_salary) and min_salary > max_salary:
            raise ValueError("min_salary must be less than or equal to max_salary")
        return values

    class Config:
        from_attributes = True


class JobApplicationCreate(JobAplicationBase):
    category_id: UUID
    professional_id: UUID
    city_id: UUID
    is_main: bool
    skills: list[SkillBase]
    status: JobStatus


class JobApplicationUpdate(BaseModel):
    name: str | None = None
    min_salary: Salary | None = None  # type: ignore
    max_salary: Salary | None = None  # type: ignore
    description: str | None = None
    city_id: UUID | None = None
    skills: list[SkillBase] | None = None
    is_main: bool | None = None
    application_status: JobStatus | None = None


class JobApplicationResponse(JobAplicationBase):
    """
    Pydantic schema representing the FastAPI response for Job Application.

    Attributes:
        min_salary (int): The lower boundary for the salary range.
        max_salary (int): The upper boundary for the salary range.
        description (str): Description of the professional.
        skills (list[str]): List of Professional Skills.
        city (str): The city the professional is located in.
        id (UUID): The identifier of the professional.
        first_name (str): First name of the professional.
        last_name (str): Last name of the professional.
        email (EmailStr): Email of the professional.
        description (str): Description of the professional.
        photo bytes | None: Photo of the professional.
    """

    application_id: UUID
    professional_id: UUID
    created_at: datetime
    first_name: str
    last_name: str
    city: str
    email: EmailStr
    photo: bytes | None = None
    status: str
    skills: list[SkillResponse] | None = None
    category_id: UUID
    category_title: str

    @classmethod
    def create(
        cls,
        job_application: JobApplication,
    ) -> "JobApplicationResponse":
        professional = job_application.professional
        return cls(
            application_id=job_application.id,
            name=job_application.name,
            professional_id=professional.id,
            created_at=job_application.created_at,
            category_id=job_application.category_id,
            category_title=job_application.category.title,
            photo=professional.photo,
            first_name=professional.first_name,
            last_name=professional.last_name,
            email=professional.email,
            status=job_application.status.value,
            min_salary=job_application.min_salary,
            max_salary=job_application.max_salary,
            description=job_application.description,
            city=professional.city.name,
            skills=[SkillResponse.create(skill) for skill in job_application.skills],
        )

    class Config:
        json_encoders = {bytes: lambda v: "<binary data>"}
