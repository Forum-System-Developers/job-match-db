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
        "city_id": cities[0]["id"],  # Sofia
        "username": "devtech1",
        "password_hash": hash_password("DevTech1pwd!"),
        "name": "CodeCraft Ltd.",
        "description": "Innovative software development services.",
        "address_line": "Tech Park Blvd, Sofia",
        "email": "contact@codecraft.bg",
        "phone_number": "1234567890",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],  # Berlin
        "username": "devlogic2",
        "password_hash": hash_password("DevLogic2pwd!"),
        "name": "LogicCore Solutions",
        "description": "Specialists in custom app development.",
        "address_line": "StartHub Strasse, Berlin",
        "email": "hello@logiccore.de",
        "phone_number": "0987654321",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],  # Paris
        "username": "telecast1",
        "password_hash": hash_password("TeleCast1pwd!"),
        "name": "DialDirect",
        "description": "Professional telemarketing and outreach.",
        "address_line": "Rue Telecontact, Paris",
        "email": "info@dialdirect.fr",
        "phone_number": "1357924680",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],  # Vienna
        "username": "callnova2",
        "password_hash": hash_password("CallNova2pwd!"),
        "name": "CallNova GmbH",
        "description": "Customer-focused telemarketing solutions.",
        "address_line": "Market Square 12, Vienna",
        "email": "support@callnova.at",
        "phone_number": "2468135790",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],  # Sofia
        "username": "brandboost1",
        "password_hash": hash_password("BrandBoost1pwd!"),
        "name": "BrandBoost Agency",
        "description": "Marketing strategies that drive results.",
        "address_line": "Creative Hub Blvd, Sofia",
        "email": "contact@brandboost.bg",
        "phone_number": "9876543210",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],  # Berlin
        "username": "promojet2",
        "password_hash": hash_password("PromoJet2pwd!"),
        "name": "PromoJet GmbH",
        "description": "Creative marketing campaigns and branding.",
        "address_line": "Branding Alley, Berlin",
        "email": "info@promojet.de",
        "phone_number": "3216549870",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],  # Paris
        "username": "uxvision1",
        "password_hash": hash_password("UXVision1pwd!"),
        "name": "UX Vision Studio",
        "description": "Crafting exceptional user experiences.",
        "address_line": "Design District, Paris",
        "email": "studio@uxvision.fr",
        "phone_number": "1928374650",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],  # Vienna
        "username": "uidesigns2",
        "password_hash": hash_password("UIDesigns2pwd!"),
        "name": "UI Designs Co.",
        "description": "Expertise in UI/UX and interface design.",
        "address_line": "Innovation Street, Vienna",
        "email": "hello@uidesigns.at",
        "phone_number": "4567891230",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[0]["id"],  # Sofia
        "username": "editorshub1",
        "password_hash": hash_password("EditorsHub1pwd!"),
        "name": "EditorsHub Ltd.",
        "description": "Professional editing and proofreading.",
        "address_line": "Writers Avenue, Sofia",
        "email": "contact@editorshub.bg",
        "phone_number": "7891234560",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[1]["id"],  # Berlin
        "username": "redpen2",
        "password_hash": hash_password("RedPen2pwd!"),
        "name": "Red Pen Editing",
        "description": "Refining your content with precision.",
        "address_line": "Edit Lane, Berlin",
        "email": "info@redpen.de",
        "phone_number": "6543217890",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[3]["id"],  # Paris
        "username": "accountplus1",
        "password_hash": hash_password("AccountPlus1pwd!"),
        "name": "AccountPlus Solutions",
        "description": "Streamlined accounting services.",
        "address_line": "Finance Plaza, Paris",
        "email": "service@accountplus.fr",
        "phone_number": "1237894560",
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "city_id": cities[2]["id"],  # Vienna
        "username": "fintrack2",
        "password_hash": hash_password("FinTrack2pwd!"),
        "name": "FinTrack GmbH",
        "description": "Your partner in financial management.",
        "address_line": "Profit Street, Vienna",
        "email": "info@fintrack.at",
        "phone_number": "9873216540",
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
