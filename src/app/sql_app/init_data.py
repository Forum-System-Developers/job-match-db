import random
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.sql_app import (
    Category,
    City,
    Company,
    JobAd,
    JobAdSkill,
    JobApplication,
    JobApplicationSkill,
    Match,
    PendingSkill,
    Professional,
    Skill,
)
from app.sql_app.job_ad.job_ad_status import JobAdStatus
from app.sql_app.job_application.job_application_status import JobStatus
from app.sql_app.job_requirement.skill_level import SkillLevel
from app.sql_app.match.match_status import MatchStatus
from app.sql_app.professional.professional_status import ProfessionalStatus
from app.utils.password_utils import hash_password


def random_date_within_last_month() -> datetime:
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)
    return one_month_ago + (now - one_month_ago) * random.random()


def ensure_valid_created_at(target_date: datetime) -> datetime:
    while (valid_datetime := random_date_within_last_month()) <= target_date:
        pass
    return valid_datetime


cities = [
    {
        "id": uuid4(),
        "name": "Sofia",
    },
    {
        "id": uuid4(),
        "name": "Berlin",
    },
    {
        "id": uuid4(),
        "name": "Vienna",
    },
    {
        "id": uuid4(),
        "name": "Paris",
    },
]

categories = [
    {
        "id": uuid4(),
        "title": "Development",
        "description": "Category for development jobs",
    },
    {
        "id": uuid4(),
        "title": "Telemarketing",
        "description": "Category for telemarketing jobs",
    },
    {
        "id": uuid4(),
        "title": "Marketing",
        "description": "Category for marketing jobs",
    },
    {
        "id": uuid4(),
        "title": "UI/UX Design",
        "description": "Category for UI/UX design jobs",
    },
    {
        "id": uuid4(),
        "title": "Editing",
        "description": "Category for editing jobs",
    },
    {
        "id": uuid4(),
        "title": "Accounting",
        "description": "Category for accounting jobs",
    },
]

companies: list[dict[str, Any]] = [
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "username": "company1",
        "password_hash": hash_password("Company1pwd!"),
        "name": "Uplers",
        "description": "Company 1 description",
        "address_line": "Company 1 address",
        "email": "company1@gmail.com",
        "phone_number": "1234567890",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "username": "company2",
        "password_hash": hash_password("Company2pwd!"),
        "name": "Designit",
        "description": "Company 2 description",
        "address_line": "Company 2 address",
        "email": "company2@exmaple.com",
        "phone_number": "0987654321",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "username": "company3",
        "password_hash": hash_password("Company3pwd!"),
        "name": "Company 3",
        "description": "Company 3 description",
        "address_line": "Company 3 address",
        "email": "company3@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "username": "company4",
        "password_hash": hash_password("Company4pwd!"),
        "name": "Company 4",
        "description": "Company 4 description",
        "address_line": "Company 4 address",
        "email": "company4@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "username": "company5",
        "password_hash": hash_password("Company5pwd!"),
        "name": "Company 5",
        "description": "Company 5 description",
        "address_line": "Company 5 address",
        "email": "company5@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "username": "company6",
        "password_hash": hash_password("Company6pwd!"),
        "name": "Company 6",
        "description": "Company 6 description",
        "address_line": "Company 6 address",
        "email": "company6@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "username": "company7",
        "password_hash": hash_password("Company7pwd!"),
        "name": "Company 7",
        "description": "Company 7 description",
        "address_line": "Company 7 address",
        "email": "company7@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "username": "company8",
        "password_hash": hash_password("Company8pwd!"),
        "name": "Company 8",
        "description": "Company 8 description",
        "address_line": "Company 8 address",
        "email": "company8@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "username": "company9",
        "password_hash": hash_password("Company9pwd!"),
        "name": "Company 9",
        "description": "Company 9 description",
        "address_line": "Company 9 address",
        "email": "company9@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "username": "company10",
        "password_hash": hash_password("Company10pwd!"),
        "name": "Company 10",
        "description": "Company 10 description",
        "address_line": "Company 10 address",
        "email": "company10@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "username": "company11",
        "password_hash": hash_password("Company11pwd!"),
        "name": "Company 11",
        "description": "Company 11 description",
        "address_line": "Company 11 address",
        "email": "company11@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "username": "company12",
        "password_hash": hash_password("Company12pwd!"),
        "name": "Company 12",
        "description": "Company 12 description",
        "address_line": "Company 12 address",
        "email": "company12@gmail.com",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
]

professionals: list[dict[str, Any]] = [
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "first_name": "Lewis",
        "last_name": "Boyle",
        "username": "Lewisreally",
        "password_hash": hash_password("Lewisboyle1!"),
        "description": "Professional 1 description",
        "email": "lewis.boyle@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "first_name": "Sam",
        "last_name": "Smith",
        "username": "BigSam",
        "password_hash": hash_password("Samsmith1!"),
        "description": "Professional 2 description",
        "email": "sam.smith@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "first_name": "Katie",
        "last_name": "Jones",
        "username": "CutyKatie",
        "password_hash": hash_password("Katiejones1!"),
        "description": "Professional 3 description",
        "email": "katie.jones@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "first_name": "Nathan",
        "last_name": "Hill",
        "username": "NateHill",
        "password_hash": hash_password("Nathanhill1!"),
        "description": "Professional 4 description",
        "email": "nathan.hill@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "first_name": "Tom",
        "last_name": "Brown",
        "username": "YoungTom",
        "password_hash": hash_password("Tombrown1!"),
        "description": "Professional 5 description",
        "email": "tom.brown@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "first_name": "George",
        "last_name": "Lee",
        "username": "GoodGeorge",
        "password_hash": hash_password("Georgelee1!"),
        "description": "Professional 6 description",
        "email": "george.lee@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "first_name": "Ben",
        "last_name": "King",
        "username": "Kingsman",
        "password_hash": hash_password("Benking1!"),
        "description": "Professional 7 description",
        "email": "ben.king@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "first_name": "Michael",
        "last_name": "Parker",
        "username": "ParkerMike",
        "password_hash": hash_password("Michaelparker1!"),
        "description": "Professional 8 description",
        "email": "michael.parker@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],
        "first_name": "Anna",
        "last_name": "Perry",
        "username": "AnnaPerry",
        "password_hash": hash_password("Annaperry1!"),
        "description": "Professional 9 description",
        "email": "anna.perry@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],
        "first_name": "Angela",
        "last_name": "Baker",
        "username": "crazyAngela",
        "password_hash": hash_password("Angelabaker1!"),
        "description": "Professional 10 description",
        "email": "angela.baker@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],
        "first_name": "John",
        "last_name": "Doe",
        "username": "CrazyMegaHell",
        "password_hash": hash_password("Johndoe1!"),
        "description": "Professional 11 description",
        "email": "john.doe@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],
        "first_name": "Jane",
        "last_name": "Kane",
        "username": "KaneJane",
        "password_hash": hash_password("Janekane1!"),
        "description": "Professional 12 description",
        "email": "jane.kane@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
]

skills = [
    {
        "id": uuid4(),
        "name": "Skill 1",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "Skill 2",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Skill 3",
        "category_id": categories[2]["id"],
    },
]

pending_skills = [
    {
        "id": uuid4(),
        "category_id": categories[0]["id"],
        "submitted_by": companies[0]["id"],
        "name": "Pending Skill 1",
        "created_at": ensure_valid_created_at(companies[0]["created_at"]),
    },
]

job_ads = [
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],
        "category_id": categories[0]["id"],
        "location_id": cities[0]["id"],
        "title": "Job Ad 1",
        "description": "Job Ad 1 description",
        "min_salary": 1000.0,
        "max_salary": 2000.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],
        "category_id": categories[1]["id"],
        "location_id": cities[1]["id"],
        "title": "Job Ad 2",
        "description": "Job Ad 2 description",
        "min_salary": 2000.0,
        "max_salary": 3000.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "company_id": companies[2]["id"],
        "category_id": categories[2]["id"],
        "location_id": cities[2]["id"],
        "title": "Job Ad 3",
        "description": "Job Ad 3 description",
        "min_salary": 3000.0,
        "max_salary": 4000.0,
        "skill_level": SkillLevel.EXPERT,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
]

job_ad_skills = [
    {
        "job_ad_id": job_ads[0]["id"],
        "skill_id": skills[0]["id"],
    },
    {
        "job_ad_id": job_ads[1]["id"],
        "skill_id": skills[1]["id"],
    },
    {
        "job_ad_id": job_ads[2]["id"],
        "skill_id": skills[2]["id"],
    },
]

job_applications = [
    {
        "id": uuid4(),
        "category_id": categories[0]["id"],
        "city_id": cities[0]["id"],
        "professional_id": professionals[0]["id"],
        "name": "Job Application 1",
        "description": "Job Application 1",
        "min_salary": 1000.0,
        "max_salary": 2000.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[0]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[1]["id"],
        "city_id": cities[1]["id"],
        "professional_id": professionals[1]["id"],
        "name": "Job Application 2",
        "description": "Job Application 2",
        "min_salary": 2000.0,
        "max_salary": 3000.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[1]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[2]["id"],
        "city_id": cities[2]["id"],
        "professional_id": professionals[2]["id"],
        "name": "Job Application 3",
        "description": "Job Application 3",
        "min_salary": 3000.0,
        "max_salary": 4000.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[2]["created_at"]),
    },
]

job_application_skills = [
    {
        "job_application_id": job_applications[0]["id"],
        "skill_id": skills[0]["id"],
    },
    {
        "job_application_id": job_applications[1]["id"],
        "skill_id": skills[1]["id"],
    },
    {
        "job_application_id": job_applications[2]["id"],
        "skill_id": skills[2]["id"],
    },
]

category_job_applications = [
    {
        "category_id": categories[0]["id"],
        "job_application_id": job_applications[0]["id"],
    },
    {
        "category_id": categories[1]["id"],
        "job_application_id": job_applications[1]["id"],
    },
    {
        "category_id": categories[2]["id"],
        "job_application_id": job_applications[2]["id"],
    },
]

matches = [
    {
        "job_ad_id": job_ads[0]["id"],
        "job_application_id": job_applications[0]["id"],
        "status": MatchStatus.REQUESTED_BY_JOB_AD,
        "created_at": ensure_valid_created_at(
            max(job_applications[0]["created_at"], job_ads[0]["created_at"])
        ),
    },
    {
        "job_ad_id": job_ads[1]["id"],
        "job_application_id": job_applications[1]["id"],
        "status": MatchStatus.REQUESTED_BY_JOB_APP,
        "created_at": ensure_valid_created_at(
            max(job_applications[1]["created_at"], job_ads[1]["created_at"])
        ),
    },
    {
        "job_ad_id": job_ads[2]["id"],
        "job_application_id": job_applications[2]["id"],
        "status": MatchStatus.ACCEPTED,
        "created_at": ensure_valid_created_at(
            max(job_applications[2]["created_at"], job_ads[2]["created_at"])
        ),
    },
]


def insert_cities(db: Session) -> None:
    for city in cities:
        city_model = City(**city)
        db.add(city_model)
    db.commit()


def insert_categories(db: Session) -> None:
    for category in categories:
        category_model = Category(**category)
        db.add(category_model)
    db.commit()


def insert_companies(db: Session) -> None:
    for company in companies:
        company_model = Company(**company)
        db.add(company_model)
    db.commit()


def insert_professionals(db: Session) -> None:
    for professional in professionals:
        professional_model = Professional(**professional)
        db.add(professional_model)
    db.commit()


def insert_job_ads(db: Session) -> None:
    for job_ad in job_ads:
        job_ad_model = JobAd(**job_ad)
        db.add(job_ad_model)
    db.commit()


# TODO: incremenet number of job ads for companies
def insert_job_ad_skills(db: Session) -> None:
    for job_ad_skill in job_ad_skills:
        job_ad_skill_model = JobAdSkill(**job_ad_skill)
        db.add(job_ad_skill_model)
    db.commit()


def insert_job_applications(db: Session) -> None:
    for job_application in job_applications:
        job_application_model = JobApplication(**job_application)
        job_application_model.professional.active_application_count += 1
        db.add(job_application_model)
    db.commit()


def insert_skills(db: Session) -> None:
    for skill in skills:
        skill_model = Skill(**skill)
        db.add(skill_model)
    db.commit()


def insert_pending_skills(db: Session) -> None:
    for pending_skill in pending_skills:
        pending_skill_model = PendingSkill(**pending_skill)
        db.add(pending_skill_model)
    db.commit()


def insert_job_application_skills(db: Session) -> None:
    for job_application_skill in job_application_skills:
        job_application_skill_model = JobApplicationSkill(**job_application_skill)
        db.add(job_application_skill_model)
    db.commit()


def insert_matches(db: Session) -> None:
    for match in matches:
        match_model = Match(**match)
        db.add(match_model)
    db.commit()


def is_initialized(db: Session) -> bool:
    return db.query(City).count() > 0


def insert_data(db: Session) -> None:
    if is_initialized(db):
        return
    insert_cities(db)
    insert_categories(db)
    insert_companies(db)
    insert_professionals(db)
    insert_skills(db)
    insert_pending_skills(db)
    insert_job_ads(db)
    insert_job_ad_skills(db)
    insert_job_applications(db)
    insert_job_application_skills(db)
    insert_matches(db)
