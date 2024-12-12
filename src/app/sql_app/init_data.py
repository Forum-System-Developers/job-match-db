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
        "description": "CodeCraft Ltd. offers innovative and reliable software development services tailored to meet the demands of modern businesses. Our team is dedicated to creating scalable, high-performance solutions that empower companies to succeed in a competitive market. From robust web applications to seamless mobile experiences, we leverage cutting-edge technologies and industry best practices. Our expertise spans various domains, enabling us to understand and address specific client needs effectively. At CodeCraft, collaboration, transparency, and a commitment to excellence are at the heart of our operations. We take pride in delivering projects on time and within budget, ensuring our clients gain a significant competitive advantage. Choose CodeCraft for solutions that turn your business challenges into opportunities.",
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
        "description": "LogicCore Solutions is a dynamic software development company focused on delivering exceptional digital products. With a passion for technology and innovation, we specialize in building secure, scalable, and user-friendly applications for businesses of all sizes. Our team of seasoned developers and project managers works closely with clients to understand their goals, ensuring each solution aligns with their vision. From concept to deployment, we handle every aspect of the development process with professionalism and dedication. By integrating the latest tools and methodologies, LogicCore guarantees efficiency and adaptability in all our projects. Let us help you navigate the complexities of digital transformation and achieve sustained growth in your industry.",
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
        "description": "DialDirect is a premier telemarketing service provider committed to enhancing client outreach and engagement. Our company specializes in crafting targeted campaigns that drive meaningful interactions and foster customer loyalty. With a skilled team and advanced communication tools, we deliver exceptional results across various industries. Whether you’re launching a new product, conducting surveys, or managing inbound and outbound sales, DialDirect tailors its approach to meet your objectives. We prioritize quality, compliance, and a customer-centric ethos in all our services. At DialDirect, we believe in building long-term relationships that yield measurable outcomes for our clients. Partner with us to amplify your marketing efforts and connect with your audience effectively.",
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
        "description": "CallNova GmbH stands as a trusted partner in telemarketing and customer engagement solutions. Our mission is to provide top-tier services that help businesses expand their reach and improve customer satisfaction. We employ a team of highly trained professionals equipped with modern tools to ensure seamless communication at every stage of the customer journey. Our services include lead generation, appointment setting, customer surveys, and more. At CallNova, we are committed to delivering personalized experiences that reflect our clients’ brand values. By focusing on continuous improvement and innovation, we guarantee high-quality results that meet and exceed expectations. Experience the CallNova advantage and transform your telemarketing strategy.",
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
        "description": "BrandBoost Agency is a creative marketing powerhouse dedicated to helping brands achieve unparalleled visibility and growth. We specialize in crafting data-driven strategies and innovative campaigns that resonate with target audiences. From social media management to content creation, we cover a broad spectrum of marketing services designed to amplify your brand’s voice. Our team of experts is passionate about storytelling and leveraging the latest trends to keep your business ahead of the curve. At BrandBoost, we believe in building lasting connections through meaningful engagement and strategic planning. Let us partner with you to unlock your brand’s full potential and achieve remarkable success in a competitive market.",
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
        "description": "PromoJet GmbH is a leading marketing agency renowned for delivering innovative campaigns that leave a lasting impact. With a focus on creativity and precision, we help businesses establish strong brand identities and connect with their audience. Our services range from branding and graphic design to performance marketing and event promotions. Each project at PromoJet is approached with a blend of strategic thinking and artistic flair, ensuring results that exceed expectations. We work closely with clients to understand their goals and tailor our solutions accordingly. Choose PromoJet to experience marketing excellence and drive your brand toward greater recognition and profitability.",
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
        "description": "UX Vision Studio is dedicated to designing user experiences that captivate and inspire. Our team of seasoned designers focuses on creating intuitive and visually appealing interfaces that enhance usability and satisfaction. We employ a collaborative process that combines user research, wireframing, prototyping, and testing to ensure every design meets the highest standards. Whether you need a complete UI/UX overhaul or specific interface enhancements, UX Vision Studio delivers solutions tailored to your needs. We believe in the power of design to solve problems and drive business success. Partner with us to elevate your digital presence and leave a lasting impression on your audience.",
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
        "description": "UI Designs Co. is your go-to partner for all things UI/UX. We pride ourselves on delivering innovative designs that bridge the gap between aesthetics and functionality. Our expert team collaborates with clients to understand their unique challenges and create solutions that align with their brand identity. From wireframes to polished interfaces, we prioritize user needs and business objectives in every project. At UI Designs Co., we embrace the latest design trends and technologies to deliver results that stand out in a competitive market. Let us transform your digital vision into reality with designs that engage, inform, and inspire.",
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
        "description": "EditorsHub Ltd. provides professional editing and proofreading services designed to elevate your content to the highest standards. Our team of experienced editors works meticulously to refine grammar, structure, and style while preserving your unique voice. Whether you’re crafting business documents, academic papers, or creative writing, we ensure every piece is polished and error-free. At EditorsHub, we understand the power of words and strive to help clients communicate effectively. Our services are tailored to meet diverse needs, with a commitment to quality and attention to detail. Choose EditorsHub for exceptional editing solutions that enhance clarity and impact.",
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
        "description": "Red Pen Editing is a trusted name in content refinement, offering comprehensive editing and proofreading services. Our expertise spans various domains, from academic research to business communications. We pride ourselves on our meticulous approach, ensuring every detail is perfected and every message resonates. At Red Pen Editing, we go beyond correcting errors; we enhance tone, coherence, and overall readability. Our dedicated team collaborates with clients to understand their goals and deliver tailored solutions. Whether you need quick proofreading or in-depth editing, Red Pen is here to ensure your content makes a lasting impression. Experience precision and professionalism with every project.",
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
        "description": "AccountPlus Solutions specializes in delivering streamlined accounting services that simplify financial management for businesses. Our team of skilled professionals offers expertise in bookkeeping, tax preparation, payroll, and more. We tailor our services to meet the specific needs of each client, ensuring compliance and accuracy at every step. With a commitment to transparency and efficiency, AccountPlus helps businesses save time and focus on growth. Our state-of-the-art tools and processes guarantee reliable results and data security. At AccountPlus, we believe in building strong client relationships based on trust and mutual success. Partner with us to achieve financial clarity and peace of mind.",
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
        "description": "FinTrack GmbH is a premier provider of financial management solutions designed to empower businesses. We offer a wide range of services, including accounting, financial planning, and compliance support. Our team of experts combines technical proficiency with a client-centric approach to deliver personalized solutions that drive success. At FinTrack, we understand the challenges of managing finances in a dynamic market. That’s why we focus on providing clear insights and actionable strategies to help clients stay ahead. Whether you’re a startup or an established enterprise, we’re committed to supporting your financial goals with precision and dedication. Discover the FinTrack difference today.",
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
        "description": "I’m Lewis Boyle, and I’m driven by a deep passion for problem-solving and creating impactful results. My career is built on a foundation of curiosity and a constant desire to learn and grow. I approach every challenge with a mindset focused on collaboration and efficiency. My strengths lie in my ability to adapt to different environments, working well both independently and as part of a team. I take pride in delivering high-quality work that exceeds expectations, and I’m always looking for opportunities to improve. I believe that success comes from perseverance, creativity, and building strong relationships with colleagues and clients.",
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
        "description": "My name is Sam Smith, and I am a dedicated professional with a passion for innovation. I thrive when presented with challenges that push my limits and allow me to explore new solutions. I have always believed in the power of collaboration and see teamwork as essential for achieving success. By listening to others and offering my ideas, I aim to contribute positively to every project I’m involved in. I am always looking for ways to refine my skills and expand my knowledge. For me, professional growth is just as important as achieving results, and I am committed to continuing this journey.",
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
        "description": "Hi, I’m Katie Jones. I’m a professional with a passion for innovation and a strong focus on achieving excellence. I enjoy working in dynamic environments where I can learn, adapt, and apply new ideas. I believe in the importance of collaboration and always strive to foster a positive and productive atmosphere with my team. My experience has taught me the value of perseverance and dedication. I’m always excited about new opportunities that challenge my creativity and allow me to expand my skill set. By remaining flexible and focused, I aim to contribute to projects that deliver real value and drive meaningful change.",
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
        "description": "I’m Nathan Hill, and my professional journey is defined by a commitment to both personal and team success. I enjoy working on projects that require both strategic thinking and hands-on execution. My approach combines creativity and practicality, ensuring that I can deliver innovative solutions while maintaining focus on the bigger picture. I pride myself on my resilience and ability to adapt to changing circumstances, which I believe is crucial in today’s fast-paced world. I am always eager to connect with like-minded professionals who share my values and work ethic to create opportunities that benefit everyone involved.",
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
        "description": "Hi, I’m Tom Brown, and I’m passionate about delivering high-quality work that adds value to every project I’m part of. With a keen eye for detail and a love for problem-solving, I thrive in environments where I can push the boundaries of what’s possible. My approach to work is methodical and focused, but I also value creativity and the freedom to explore new ideas. I believe that professional success is built on continuous learning and collaboration, and I’m always looking for ways to improve and expand my capabilities. Ultimately, I aim to build lasting relationships and contribute to impactful projects.",
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
        "description": "My name is George Lee, and I’m driven by a deep sense of responsibility to both my work and my colleagues. I am a firm believer in the power of teamwork and communication to drive success, and I always strive to bring positivity and energy to every project. I thrive on challenges that require strategic thinking, problem-solving, and effective execution. My career so far has taught me the importance of being adaptable and proactive, and I’m always looking for ways to learn new skills. I believe that the most rewarding achievements come from working together to create something meaningful and lasting.",
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
        "description": "I’m Ben King, and I’m always looking for ways to innovate and drive progress. My passion lies in tackling complex challenges and coming up with creative solutions that benefit everyone involved. I am known for my ability to work under pressure, maintaining a positive attitude even in the most demanding situations. Whether I’m working independently or as part of a team, I pride myself on my ability to remain focused and deliver quality results. I believe that success is a result of hard work, perseverance, and a willingness to learn and grow continuously.",
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
        "description": "My name is Michael Parker, and I’m a dedicated professional who strives for excellence in everything I do. I enjoy taking on challenging projects that require creativity, strategic thinking, and a strong work ethic. I’m constantly looking for opportunities to refine my skills and expand my expertise. I value collaboration and believe that great things happen when diverse perspectives come together. I approach my work with a sense of accountability and always seek to contribute meaningfully to every project. For me, success is not only about achieving goals but also about fostering strong relationships and contributing to the success of my team.",
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
        "description": "I’m Anna Perry, and I take pride in being a professional who values integrity and collaboration. I approach every project with a focus on efficiency, quality, and communication, ensuring that all stakeholders are aligned and that goals are met. My experience has taught me the importance of balancing attention to detail with the ability to think strategically. I’m constantly striving to improve my skills and remain adaptable to changing circumstances. For me, growth is key to achieving long-term success, and I’m always eager to embrace new challenges and explore new opportunities.",
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
        "description": "My name is Angela Baker, and I’m a professional driven by my desire to learn and grow. I am passionate about tackling challenges that allow me to innovate and contribute to meaningful outcomes. I value the opportunity to work with others and believe that teamwork is an essential part of success. My professional approach is rooted in a commitment to excellence and a focus on delivering value. I’m always looking for new ways to improve processes and enhance my skill set. I strive to build strong professional relationships and contribute to an environment that fosters creativity and success.",
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
        "description": "I’m John Doe, and I thrive in environments where I can make a tangible impact. I’m driven by the belief that meaningful results come from collaboration, innovation, and persistence. My approach to work is hands-on, and I always aim to bring fresh ideas to the table. I take pride in my ability to stay focused and organized, even under pressure. I’m always eager to learn from others and contribute to projects that push boundaries. For me, success is a team effort, and I’m committed to fostering relationships that lead to lasting achievements.",
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
        "description": "My name is Jane Kane, and I’m a results-oriented professional with a passion for delivering high-quality work. I believe that every challenge is an opportunity to learn and grow, and I’m always eager to take on projects that allow me to innovate and think critically. My approach is grounded in a strong work ethic and a commitment to achieving excellence. I enjoy collaborating with others and believe that teamwork is essential to overcoming obstacles and achieving success. I’m excited about the future and the opportunities that will allow me to continue contributing to meaningful projects.",
        "email": "jane.kane@gmail.com",
        "status": ProfessionalStatus.ACTIVE,
        "active_application_count": 0,
        "has_private_matches": False,
        "created_at": random_date_within_last_month(),
    },
]

skills = [
    # Development
    {
        "id": uuid4(),
        "name": "Python Programming",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "Web Development",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "Database Management",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "JavaScript",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "Version Control (Git)",
        "category_id": categories[0]["id"],
    },
    {
        "id": uuid4(),
        "name": "API Development",
        "category_id": categories[0]["id"],
    },
    
    # Telemarketing
    {
        "id": uuid4(),
        "name": "Cold Calling",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Lead Generation",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Customer Relationship Management",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Script Writing",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Negotiation Skills",
        "category_id": categories[1]["id"],
    },
    {
        "id": uuid4(),
        "name": "Market Research",
        "category_id": categories[1]["id"],
    },

    # Marketing
    {
        "id": uuid4(),
        "name": "Digital Marketing",
        "category_id": categories[2]["id"],
    },
    {
        "id": uuid4(),
        "name": "Content Creation",
        "category_id": categories[2]["id"],
    },
    {
        "id": uuid4(),
        "name": "SEO Optimization",
        "category_id": categories[2]["id"],
    },
    {
        "id": uuid4(),
        "name": "Social Media Marketing",
        "category_id": categories[2]["id"],
    },
    {
        "id": uuid4(),
        "name": "Email Marketing",
        "category_id": categories[2]["id"],
    },
    {
        "id": uuid4(),
        "name": "Brand Strategy",
        "category_id": categories[2]["id"],
    },
    
    # UI/UX Design
    {
        "id": uuid4(),
        "name": "Wireframing",
        "category_id": categories[3]["id"],
    },
    {
        "id": uuid4(),
        "name": "Prototyping",
        "category_id": categories[3]["id"],
    },
    {
        "id": uuid4(),
        "name": "User Research",
        "category_id": categories[3]["id"],
    },
    {
        "id": uuid4(),
        "name": "Interaction Design",
        "category_id": categories[3]["id"],
    },
    {
        "id": uuid4(),
        "name": "Visual Design",
        "category_id": categories[3]["id"],
    },
    {
        "id": uuid4(),
        "name": "Usability Testing",
        "category_id": categories[3]["id"],
    },
    
    # Editing
    {
        "id": uuid4(),
        "name": "Copy Editing",
        "category_id": categories[4]["id"],
    },
    {
        "id": uuid4(),
        "name": "Proofreading",
        "category_id": categories[4]["id"],
    },
    {
        "id": uuid4(),
        "name": "Content Editing",
        "category_id": categories[4]["id"],
    },
    {
        "id": uuid4(),
        "name": "Technical Editing",
        "category_id": categories[4]["id"],
    },
    {
        "id": uuid4(),
        "name": "Transcription",
        "category_id": categories[4]["id"],
    },
    {
        "id": uuid4(),
        "name": "Subtitling",
        "category_id": categories[4]["id"],
    },
    
    # Accounting
    {
        "id": uuid4(),
        "name": "Financial Reporting",
        "category_id": categories[5]["id"],
    },
    {
        "id": uuid4(),
        "name": "Tax Preparation",
        "category_id": categories[5]["id"],
    },
    {
        "id": uuid4(),
        "name": "Bookkeeping",
        "category_id": categories[5]["id"],
    },
    {
        "id": uuid4(),
        "name": "Budgeting",
        "category_id": categories[5]["id"],
    },
    {
        "id": uuid4(),
        "name": "Auditing",
        "category_id": categories[5]["id"],
    },
    {
        "id": uuid4(),
        "name": "Financial Analysis",
        "category_id": categories[5]["id"],
    },
]


pending_skills = []

job_ads = [
    # UI/UX Design Category (2 job_ads)
    {
        "id": uuid4(),
        "company_id": companies[4]["id"],  # DesignGurus
        "category_id": categories[3]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "UI/UX Designer",
        "description": "Join DesignGurus as a UI/UX Designer. Work on innovative projects that improve user experiences and interfaces.",
        "min_salary": 1800.0,
        "max_salary": 2700.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    {
        "id": uuid4(),
        "company_id": companies[4]["id"],  # DesignGurus
        "category_id": categories[3]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "UX Researcher",
        "description": "DesignGurus is looking for a UX Researcher to conduct usability testing and help shape the design process.",
        "min_salary": 2000.0,
        "max_salary": 2900.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
        # Job Ad 1 (Sofia, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Backend Developer",
        "description": "Join CodeCraft Ltd. as a Backend Developer to build high-performance applications with scalable architecture.",
        "min_salary": 2500.0,
        "max_salary": 3500.0,
        "skill_level": SkillLevel.EXPERT,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 2 (Berlin, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Full-stack Developer",
        "description": "As a Full-stack Developer at CodeCraft Ltd., you'll work with a team to create modern web applications from frontend to backend.",
        "min_salary": 2200.0,
        "max_salary": 3300.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 3 (Vienna, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Frontend Developer",
        "description": "CodeCraft Ltd. is looking for a talented Frontend Developer to craft user interfaces that stand out in the industry.",
        "min_salary": 2100.0,
        "max_salary": 3000.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 4 (Paris, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[0]["id"],
        "location_id": cities[3]["id"],  # Paris
        "title": "DevOps Engineer",
        "description": "Looking for a DevOps Engineer at LogicCore Solutions to streamline continuous integration and deployment processes.",
        "min_salary": 2800.0,
        "max_salary": 3800.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 5 (Sofia, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Mobile Developer",
        "description": "CodeCraft Ltd. is hiring a Mobile Developer to create cutting-edge applications for iOS and Android.",
        "min_salary": 2400.0,
        "max_salary": 3500.0,
        "skill_level": SkillLevel.EXPERT,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 6 (Berlin, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Software Engineer",
        "description": "CodeCraft Ltd. is looking for a Software Engineer to contribute to developing world-class solutions.",
        "min_salary": 2300.0,
        "max_salary": 3200.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 7 (Vienna, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[0]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Systems Architect",
        "description": "LogicCore Solutions is searching for a Systems Architect to help design robust and scalable systems for our clients.",
        "min_salary": 2600.0,
        "max_salary": 3700.0,
        "skill_level": SkillLevel.EXPERT,
        "status": JobAdStatus.ARCHIVED,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 8 (Paris, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[0]["id"],
        "location_id": cities[3]["id"],  # Paris
        "title": "Cloud Engineer",
        "description": "Join CodeCraft Ltd. as a Cloud Engineer to manage cloud-based infrastructure and deploy applications.",
        "min_salary": 2700.0,
        "max_salary": 3700.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 1 (Sofia, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[1]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Telemarketing Specialist",
        "description": "LogicCore Solutions is looking for a motivated Telemarketing Specialist to help promote our products and services.",
        "min_salary": 1500.0,
        "max_salary": 2200.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 2 (Berlin, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[1]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Telemarketing Executive",
        "description": "Join LogicCore Solutions as a Telemarketing Executive and drive our growth by reaching out to potential customers.",
        "min_salary": 1600.0,
        "max_salary": 2300.0,
        "skill_level": SkillLevel.INTERN,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 3 (Vienna, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[1]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Customer Service Representative",
        "description": "Looking for a Customer Service Representative to handle calls and ensure excellent customer service for LogicCore Solutions.",
        "min_salary": 1700.0,
        "max_salary": 2400.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 4 (Paris, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[1]["id"],
        "location_id": cities[3]["id"],  # Paris
        "title": "Inbound Telemarketing Agent",
        "description": "CodeCraft Ltd. seeks an Inbound Telemarketing Agent to manage customer inquiries and assist in sales campaigns.",
        "min_salary": 1800.0,
        "max_salary": 2500.0,
        "skill_level": SkillLevel.INTERN,
        "status": JobAdStatus.ARCHIVED,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 5 (Sofia, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[1]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Telemarketing Manager",
        "description": "Join LogicCore Solutions as a Telemarketing Manager to lead a team and oversee the telemarketing operations.",
        "min_salary": 2200.0,
        "max_salary": 3000.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 1 (Sofia, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[2]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Marketing Coordinator",
        "description": "CodeCraft Ltd. is looking for a Marketing Coordinator to manage campaigns and help increase brand awareness.",
        "min_salary": 1800.0,
        "max_salary": 2500.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 2 (Berlin, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[2]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Digital Marketing Specialist",
        "description": "Join LogicCore Solutions as a Digital Marketing Specialist to drive our online presence through SEO and content strategies.",
        "min_salary": 2000.0,
        "max_salary": 2800.0,
        "skill_level": SkillLevel.EXPERT,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 3 (Vienna, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[2]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Content Marketing Manager",
        "description": "CodeCraft Ltd. is looking for a Content Marketing Manager to oversee content creation and strategy for our brand.",
        "min_salary": 2200.0,
        "max_salary": 3000.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 4 (Paris, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[2]["id"],
        "location_id": cities[3]["id"],  # Paris
        "title": "Social Media Marketing Strategist",
        "description": "LogicCore Solutions is hiring a Social Media Marketing Strategist to create and execute social media campaigns.",
        "min_salary": 2500.0,
        "max_salary": 3200.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 1 (Sofia, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[4]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Video Editor",
        "description": "CodeCraft Ltd. is looking for a creative Video Editor to work on high-quality video projects for digital marketing.",
        "min_salary": 1800.0,
        "max_salary": 2300.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 2 (Berlin, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[4]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Content Editor",
        "description": "Join LogicCore Solutions as a Content Editor to create and edit content for websites, blogs, and marketing campaigns.",
        "min_salary": 2100.0,
        "max_salary": 2600.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ARCHIVED,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 3 (Vienna, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[4]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Proofreader",
        "description": "CodeCraft Ltd. is hiring a Proofreader to ensure high-quality written content and correct any grammatical errors.",
        "min_salary": 1900.0,
        "max_salary": 2400.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 1 (Paris, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[5]["id"],
        "location_id": cities[3]["id"],  # Paris
        "title": "Financial Analyst",
        "description": "CodeCraft Ltd. is seeking a Financial Analyst to help prepare financial statements and analyze financial data.",
        "min_salary": 2500.0,
        "max_salary": 3000.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 2 (Berlin, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[5]["id"],
        "location_id": cities[1]["id"],  # Berlin
        "title": "Accountant",
        "description": "We are looking for an experienced Accountant to manage all accounting functions at LogicCore Solutions.",
        "min_salary": 2200.0,
        "max_salary": 2700.0,
        "skill_level": SkillLevel.INTERMEDIATE,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 3 (Vienna, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[5]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Tax Specialist",
        "description": "LogicCore Solutions is looking for a Tax Specialist to assist with tax filings and advise on tax compliance.",
        "min_salary": 2400.0,
        "max_salary": 2900.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 4 (Vienna, CodeCraft Ltd.)
    {
        "id": uuid4(),
        "company_id": companies[0]["id"],  # CodeCraft Ltd.
        "category_id": categories[5]["id"],
        "location_id": cities[2]["id"],  # Vienna
        "title": "Junior Accountant",
        "description": "CodeCraft Ltd. is hiring a Junior Accountant to assist in daily accounting operations and maintain financial records.",
        "min_salary": 1800.0,
        "max_salary": 2300.0,
        "skill_level": SkillLevel.INTERN,
        "status": JobAdStatus.ACTIVE,
        "created_at": random_date_within_last_month(),
    },
    # Job Ad 5 (Sofia, LogicCore Solutions)
    {
        "id": uuid4(),
        "company_id": companies[1]["id"],  # LogicCore Solutions
        "category_id": categories[5]["id"],
        "location_id": cities[0]["id"],  # Sofia
        "title": "Payroll Manager",
        "description": "We are looking for a Payroll Manager to oversee all payroll functions for employees at LogicCore Solutions.",
        "min_salary": 2300.0,
        "max_salary": 2800.0,
        "skill_level": SkillLevel.ADVANCED,
        "status": JobAdStatus.ARCHIVED,
        "created_at": random_date_within_last_month(),
    },
]

job_ad_skills = [
    # UI/UX Designer (Sofia, DesignGurus)
    {
        "job_ad_id": job_ads[0]["id"],
        "skill_id": skills[18]["id"],  # Wireframing
    },
    {
        "job_ad_id": job_ads[0]["id"],
        "skill_id": skills[19]["id"],  # Prototyping
    },
    {
        "job_ad_id": job_ads[0]["id"],
        "skill_id": skills[20]["id"],  # User Research
    },
    {
        "job_ad_id": job_ads[0]["id"],
        "skill_id": skills[22]["id"],  # Visual Design
    },
    
    # UX Researcher (Vienna, DesignGurus)
    {
        "job_ad_id": job_ads[1]["id"],
        "skill_id": skills[20]["id"],  # User Research
    },
    {
        "job_ad_id": job_ads[1]["id"],
        "skill_id": skills[23]["id"],  # Usability Testing
    },
    {
        "job_ad_id": job_ads[1]["id"],
        "skill_id": skills[21]["id"],  # Interaction Design
    },
    {
        "job_ad_id": job_ads[1]["id"],
        "skill_id": skills[18]["id"],  # Wireframing
    },

    # Backend Developer (Sofia, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[2]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[2]["id"],
        "skill_id": skills[2]["id"],  # Database Management
    },
    {
        "job_ad_id": job_ads[2]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_ad_id": job_ads[2]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },

    # Full-stack Developer (Berlin, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[3]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[3]["id"],
        "skill_id": skills[3]["id"],  # JavaScript
    },
    {
        "job_ad_id": job_ads[3]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_ad_id": job_ads[3]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },

    # Frontend Developer (Vienna, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[4]["id"],
        "skill_id": skills[3]["id"],  # JavaScript
    },
    {
        "job_ad_id": job_ads[4]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_ad_id": job_ads[4]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[4]["id"],
        "skill_id": skills[21]["id"],  # Interaction Design
    },

    # DevOps Engineer (Paris, LogicCore Solutions)
    {
        "job_ad_id": job_ads[5]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_ad_id": job_ads[5]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[5]["id"],
        "skill_id": skills[6]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[5]["id"],
        "skill_id": skills[7]["id"],  # Lead Generation
    },

    # Mobile Developer (Sofia, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[6]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[6]["id"],
        "skill_id": skills[3]["id"],  # JavaScript
    },
    {
        "job_ad_id": job_ads[6]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[6]["id"],
        "skill_id": skills[8]["id"],  # Script Writing
    },

    # Software Engineer (Berlin, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[7]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[7]["id"],
        "skill_id": skills[3]["id"],  # JavaScript
    },
    {
        "job_ad_id": job_ads[7]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[7]["id"],
        "skill_id": skills[9]["id"],  # Negotiation Skills
    },

    # Systems Architect (Vienna, LogicCore Solutions)
    {
        "job_ad_id": job_ads[8]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[8]["id"],
        "skill_id": skills[2]["id"],  # Database Management
    },
    {
        "job_ad_id": job_ads[8]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[8]["id"],
        "skill_id": skills[10]["id"],  # Market Research
    },

    # Cloud Engineer (Paris, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[9]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_ad_id": job_ads[9]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_ad_id": job_ads[9]["id"],
        "skill_id": skills[6]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[9]["id"],
        "skill_id": skills[11]["id"],  # Script Writing
    },

    # Telemarketing Specialist (Sofia, LogicCore Solutions)
    {
        "job_ad_id": job_ads[10]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[10]["id"],
        "skill_id": skills[13]["id"],  # Customer Service
    },

    # Telemarketing Executive (Berlin, LogicCore Solutions)
    {
        "job_ad_id": job_ads[11]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[11]["id"],
        "skill_id": skills[14]["id"],  # Problem Solving
    },

    # Customer Service Representative (Vienna, LogicCore Solutions)
    {
        "job_ad_id": job_ads[12]["id"],
        "skill_id": skills[13]["id"],  # Customer Service
    },
    {
        "job_ad_id": job_ads[12]["id"],
        "skill_id": skills[14]["id"],  # Problem Solving
    },

    # Inbound Telemarketing Agent (Paris, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[13]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[13]["id"],
        "skill_id": skills[13]["id"],  # Customer Service
    },
    {
        "job_ad_id": job_ads[13]["id"],
        "skill_id": skills[14]["id"],  # Problem Solving
    },
    {
        "job_ad_id": job_ads[13]["id"],
        "skill_id": skills[15]["id"],  # Time Management
    },

    # Telemarketing Manager (Sofia, LogicCore Solutions)
    {
        "job_ad_id": job_ads[14]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_ad_id": job_ads[14]["id"],
        "skill_id": skills[16]["id"],  # Leadership
    },
    {
        "job_ad_id": job_ads[14]["id"],
        "skill_id": skills[17]["id"],  # Strategic Planning
    },

    # Marketing Coordinator (Sofia, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[15]["id"],
        "skill_id": skills[18]["id"],  # Wireframing
    },
    {
        "job_ad_id": job_ads[15]["id"],
        "skill_id": skills[19]["id"],  # Prototyping
    },
    {
        "job_ad_id": job_ads[15]["id"],
        "skill_id": skills[20]["id"],  # User Research
    },
    {
        "job_ad_id": job_ads[15]["id"],
        "skill_id": skills[21]["id"],  # Interaction Design
    },

    # Digital Marketing Specialist (Berlin, LogicCore Solutions)
    {
        "job_ad_id": job_ads[16]["id"],
        "skill_id": skills[22]["id"],  # Visual Design
    },
    {
        "job_ad_id": job_ads[16]["id"],
        "skill_id": skills[23]["id"],  # Usability Testing
    },
    {
        "job_ad_id": job_ads[16]["id"],
        "skill_id": skills[24]["id"],  # SEO
    },
    {
        "job_ad_id": job_ads[16]["id"],
        "skill_id": skills[25]["id"],  # Content Strategy
    },

    # Content Marketing Manager (Vienna, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[17]["id"],
        "skill_id": skills[24]["id"],  # SEO
    },
    {
        "job_ad_id": job_ads[17]["id"],
        "skill_id": skills[25]["id"],  # Content Strategy
    },
    {
        "job_ad_id": job_ads[17]["id"],
        "skill_id": skills[26]["id"],  # Copywriting
    },
    {
        "job_ad_id": job_ads[17]["id"],
        "skill_id": skills[27]["id"],  # Email Marketing
    },

    # Social Media Marketing Strategist (Paris, LogicCore Solutions)
    {
        "job_ad_id": job_ads[18]["id"],
        "skill_id": skills[26]["id"],  # Copywriting
    },
    {
        "job_ad_id": job_ads[18]["id"],
        "skill_id": skills[27]["id"],  # Email Marketing
    },
    {
        "job_ad_id": job_ads[18]["id"],
        "skill_id": skills[28]["id"],  # Social Media Management
    },
    {
        "job_ad_id": job_ads[18]["id"],
        "skill_id": skills[29]["id"],  # Analytics
    },

    # Video Editor (Sofia, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[19]["id"],
        "skill_id": skills[30]["id"],  # Video Editing
    },
    {
        "job_ad_id": job_ads[19]["id"],
        "skill_id": skills[31]["id"],  # Motion Graphics
    },
    {
        "job_ad_id": job_ads[19]["id"],
        "skill_id": skills[32]["id"],  # Color Correction
    },
    {
        "job_ad_id": job_ads[19]["id"],
        "skill_id": skills[33]["id"],  # Sound Design
    },

    # Content Editor (Berlin, LogicCore Solutions)
    {
        "job_ad_id": job_ads[20]["id"],
        "skill_id": skills[34]["id"],  # Editing
    },
    {
        "job_ad_id": job_ads[20]["id"],
        "skill_id": skills[35]["id"],  # Proofreading
    },

    #generate skills within the range of existing skills!
    # Proofreader (Vienna, CodeCraft Ltd.)
    # DONT GENEREATE SKILLS with 36 INDEX ID AND MORE
    {
        "job_ad_id": job_ads[21]["id"],
        "skill_id": skills[35]["id"],  # Proofreading
    },

    # Financial Analyst (Paris, CodeCraft Ltd.)
    {
        "job_ad_id": job_ads[22]["id"],
        "skill_id": skills[35]["id"],  # Financial Analysis
    },

    # Accountant (Berlin, LogicCore Solutions)
    {
        "job_ad_id": job_ads[23]["id"],
        "skill_id": skills[34]["id"],  # Accounting
    },

    # Tax Specialist (Vienna, LogicCore Solutions)
    {
        "job_ad_id": job_ads[24]["id"],
        "skill_id": skills[33]["id"],  # Tax Compliance
    },

    # Junior Accountant (Vienna, CodeCraft Ltd.)

    {
        "job_ad_id": job_ads[25]["id"],
        "skill_id": skills[34]["id"],  # Accounting
    },

    # Payroll Manager (Sofia, LogicCore Solutions)

    {
        "job_ad_id": job_ads[26]["id"],
        "skill_id": skills[34]["id"],  # Accounting
    },
]

job_applications = [
    {
        "id": uuid4(),
        "category_id": categories[0]["id"],
        "city_id": cities[0]["id"],
        "professional_id": professionals[0]["id"],
        "name": "Backend Developer Application",
        "description": "This is a sample application for the Backend Developer position. I have experience with Python, and RESTful APIs.",
        "min_salary": 1000.0,
        "max_salary": 2000.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[0]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[0]["id"],
        "city_id": cities[1]["id"],
        "professional_id": professionals[0]["id"],
        "name": "Frontend Developer Application",
        "description": "Here is my application for the Frontend Developer position. I have experience with JavaScript and React.",
        "min_salary": 1000.0,
        "max_salary": 2200.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[0]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[0]["id"],
        "city_id": cities[2]["id"],
        "professional_id": professionals[0]["id"],
        "name": "DevOps Engineer Application",
        "description": "I am applying for the DevOps Engineer position. I have experience with Docker, Kubernetes, and CI/CD pipelines.",
        "min_salary": 2000.0,
        "max_salary": 2750.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[0]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[1]["id"],
        "city_id": cities[3]["id"],
        "professional_id": professionals[0]["id"],
        "name": "Telemarketing Specialist Application",
        "description": "This is a sample application for the Telemarketing Specialist position. I have experience with cold calling and customer service.",
        "min_salary": 2400.0,
        "max_salary": 3500.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[0]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[1]["id"],
        "city_id": cities[0]["id"],
        "professional_id": professionals[1]["id"],
        "name": "Telemarketing Executive Application",
        "description": "I have experience with cold calling and problem solving. Here is my application for the Telemarketing Executive position.",
        "min_salary": 1900.0,
        "max_salary": 2200.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[1]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[2]["id"],
        "city_id": cities[1]["id"],
        "professional_id": professionals[1]["id"],
        "name": "Digital Marketing Specialist Application",
        "description": "My application for the Digital Marketing Specialist position. I have experience with SEO and content strategies.",
        "min_salary": 2900.0,
        "max_salary": 3200.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[1]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[3]["id"],
        "city_id": cities[2]["id"],
        "professional_id": professionals[1]["id"],
        "name": "UX Designer Application",
        "description": "Here is my application for the UX Designer position. I have experience with wireframing and prototyping.",
        "min_salary": 1200.0,
        "max_salary": 1800.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[1]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[4]["id"],
        "city_id": cities[3]["id"],
        "professional_id": professionals[2]["id"],
        "name": "Content Editor Application",
        "description": "I have experience with editing and proofreading. Here is my application for the Content Editor position.",
        "min_salary": 1000.0,
        "max_salary": 2600.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[2]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[5]["id"],
        "city_id": cities[0]["id"],
        "professional_id": professionals[2]["id"],
        "name": "Financial Analyst Application",
        "description": "This is a sample application for the Financial Analyst position. I have experience with financial analysis and reporting.",
        "min_salary": 1000.0,
        "max_salary": 2000.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[2]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[5]["id"],
        "city_id": cities[1]["id"],
        "professional_id": professionals[2]["id"],
        "name": "Accountant Application",
        "description": "I have experience with accounting and financial reporting. Here is my application for the Accountant position.",
        "min_salary": 1300.0,
        "max_salary": 1700.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[2]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[4]["id"],
        "city_id": cities[3]["id"],
        "professional_id": professionals[3]["id"],
        "name": "Proofreader Application",
        "description": "Here is my application for the Proofreader position. I have experience with editing and proofreading.",
        "min_salary": 1650.0,
        "max_salary": 2125.0,
        "status": JobStatus.ACTIVE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[3]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[3]["id"],
        "city_id": cities[0]["id"],
        "professional_id": professionals[3]["id"],
        "name": "UI Designer Application",
        "description": "I have experience with wireframing and prototyping. Here is my application for the UI Designer position.",
        "min_salary": 3150.0,
        "max_salary": 3500.0,
        "status": JobStatus.HIDDEN,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[3]["created_at"]),
    },
    {
        "id": uuid4(),
        "category_id": categories[2]["id"],
        "city_id": cities[1]["id"],
        "professional_id": professionals[3]["id"],
        "name": "Marketing Coordinator Application",
        "description": "Hello! I have experience with wireframing. Here is my application for the Marketing Coordinator position.",
        "min_salary": 1250.0,
        "max_salary": 2100.0,
        "status": JobStatus.PRIVATE,
        "is_main": False,
        "created_at": ensure_valid_created_at(professionals[3]["created_at"]),
    },
]

job_application_skills = [

    # Backend Developer Application

    {
        "job_application_id": job_applications[0]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_application_id": job_applications[0]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },
    {
        "job_application_id": job_applications[0]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_application_id": job_applications[0]["id"],
        "skill_id": skills[2]["id"],  # Database Management
    },

    # Frontend Developer Application

    {
        "job_application_id": job_applications[1]["id"],
        "skill_id": skills[3]["id"],  # JavaScript
    },
    {
        "job_application_id": job_applications[1]["id"],
        "skill_id": skills[21]["id"],  # Interaction Design
    },
    {
        "job_application_id": job_applications[1]["id"],
        "skill_id": skills[4]["id"],  # Version Control (Git)
    },
    {
        "job_application_id": job_applications[1]["id"],
        "skill_id": skills[5]["id"],  # API Development
    },

    # DevOps Engineer Application

    {
        "job_application_id": job_applications[2]["id"],
        "skill_id": skills[6]["id"],  # Cold Calling
    },
    {
        "job_application_id": job_applications[2]["id"],
        "skill_id": skills[7]["id"],  # Lead Generation
    },
    {
        "job_application_id": job_applications[2]["id"],
        "skill_id": skills[0]["id"],  # Python Programming
    },
    {
        "job_application_id": job_applications[2]["id"],
        "skill_id": skills[9]["id"],  # Negotiation Skills
    },

    # Telemarketing Specialist Application

    {
        "job_application_id": job_applications[3]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_application_id": job_applications[3]["id"],
        "skill_id": skills[13]["id"],  # Customer Service
    },

    # Telemarketing Executive Application

    {
        "job_application_id": job_applications[4]["id"],
        "skill_id": skills[12]["id"],  # Cold Calling
    },
    {
        "job_application_id": job_applications[4]["id"],
        "skill_id": skills[14]["id"],  # Problem Solving
    },

    # Digital Marketing Specialist Application

    {
        "job_application_id": job_applications[5]["id"],
        "skill_id": skills[22]["id"],  # Visual Design
    },
    {
        "job_application_id": job_applications[5]["id"],
        "skill_id": skills[23]["id"],  # Usability Testing
    },
    {
        "job_application_id": job_applications[5]["id"],
        "skill_id": skills[24]["id"],  # SEO
    },
    {
        "job_application_id": job_applications[5]["id"],
        "skill_id": skills[25]["id"],  # Content Strategy
    },

    # UX Designer Application
    
    {
        "job_application_id": job_applications[6]["id"],
        "skill_id": skills[18]["id"],  # Wireframing
    },
    {
        "job_application_id": job_applications[6]["id"],
        "skill_id": skills[19]["id"],  # Prototyping
    },
    {
        "job_application_id": job_applications[6]["id"],
        "skill_id": skills[20]["id"],  # User Research
    },
    {
        "job_application_id": job_applications[6]["id"],
        "skill_id": skills[21]["id"],  # Interaction Design
    },

    # Content Editor Application
    
    {
        "job_application_id": job_applications[7]["id"],
        "skill_id": skills[34]["id"],  # Editing
    },
    {
        "job_application_id": job_applications[7]["id"],
        "skill_id": skills[35]["id"],  # Proofreading
    },

    # Financial Analyst Application

    {
        "job_application_id": job_applications[8]["id"],
        "skill_id": skills[35]["id"],  # Financial Analysis
    },

    # Accountant Application
    
    {
        "job_application_id": job_applications[9]["id"],
        "skill_id": skills[34]["id"],  # Accounting
    },

    # Proofreader Application
    
    {
        "job_application_id": job_applications[10]["id"],
        "skill_id": skills[35]["id"],  # Proofreading
    },
    {
        "job_application_id": job_applications[10]["id"],
        "skill_id": skills[34]["id"],  # Accounting
    }
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
    job_application_models = []
    for job_application in job_applications:
        job_application_model = JobApplication(**job_application) 
        job_application_models.append(job_application_model)
        db.add(job_application_model)
        db.commit()
        db.refresh(job_application_model)

    for job_application in job_application_models:
        job_application.professional.active_application_count += 1
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
