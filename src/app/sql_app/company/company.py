import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.sql_app.database import Base

if TYPE_CHECKING:
    from app.sql_app import City, JobAd


class Company(Base):
    """
    Represents a company entity in the database.

    Attributes:
        id (uuid.UUID): Unique identifier for the company.
        city_id (uuid.UUID): Foreign key referencing the city where the company is located.
        username (str): Unique username for the company.
        password_hash (str): Hashed password for the company.
        name (str): Name of the company.
        description (str): Description of the company.
        address_line (str): Address of the company.
        email (str): Unique email address of the company.
        phone_number (str): Unique phone number of the company.
        website_url (str, optional): URL of the company's website.
        youtube_video_id (str, optional): YouTube video ID of the company.
        logo (bytes): Logo of the company.
        active_job_count (int, optional): Number of active job postings by the company.
        successfull_matches_count (int, optional): Number of successful matches made by the company.
        created_at (datetime): Timestamp when the company record was created.
        updated_at (datetime, optional): Timestamp when the company record was last updated.

    Relationships:
        city (City): The city where the company is located.
        job_ads (list[JobAd]): List of job advertisements posted by the company.
    """

    __tablename__ = "company"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("city.id"), nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    address_line: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    website_url: Mapped[str] = mapped_column(String, nullable=True)
    youtube_video_id: Mapped[str] = mapped_column(String, nullable=True)
    logo: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    active_job_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=expression.text("0")
    )
    successfull_matches_count: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    )

    city: Mapped["City"] = relationship("City", back_populates="companies")
    job_ads: Mapped[list["JobAd"]] = relationship(
        "JobAd", back_populates="company", uselist=True, collection_class=list
    )
