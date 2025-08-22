from app import db
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Student(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)
    education_level = Column(String(50), nullable=False)
    preferred_language = Column(String(20), default='en')
    
    # Assessment scores
    technical_skills = Column(Float, default=0.0)
    communication_skills = Column(Float, default=0.0)
    analytical_skills = Column(Float, default=0.0)
    creative_skills = Column(Float, default=0.0)
    leadership_skills = Column(Float, default=0.0)
    
    # Interests (0-5 scale)
    interest_technology = Column(Float, default=0.0)
    interest_arts = Column(Float, default=0.0)
    interest_business = Column(Float, default=0.0)
    interest_healthcare = Column(Float, default=0.0)
    interest_education = Column(Float, default=0.0)
    interest_agriculture = Column(Float, default=0.0)
    interest_government = Column(Float, default=0.0)
    
    # Personality traits (0-5 scale)
    extroversion = Column(Float, default=0.0)
    conscientiousness = Column(Float, default=0.0)
    openness = Column(Float, default=0.0)
    agreeableness = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("CareerRecommendation", back_populates="student")

class Career(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    
    # Required skill weights (0-1)
    technical_weight = Column(Float, default=0.0)
    communication_weight = Column(Float, default=0.0)
    analytical_weight = Column(Float, default=0.0)
    creative_weight = Column(Float, default=0.0)
    leadership_weight = Column(Float, default=0.0)
    
    # Interest alignment weights (0-1)
    technology_alignment = Column(Float, default=0.0)
    arts_alignment = Column(Float, default=0.0)
    business_alignment = Column(Float, default=0.0)
    healthcare_alignment = Column(Float, default=0.0)
    education_alignment = Column(Float, default=0.0)
    agriculture_alignment = Column(Float, default=0.0)
    government_alignment = Column(Float, default=0.0)
    
    # Personality fit
    extroversion_fit = Column(Float, default=0.0)
    conscientiousness_fit = Column(Float, default=0.0)
    openness_fit = Column(Float, default=0.0)
    agreeableness_fit = Column(Float, default=0.0)
    
    # Additional info
    average_salary = Column(String(50))
    job_growth = Column(String(50))
    education_required = Column(String(100))
    rural_opportunities = Column(Boolean, default=False)

class Course(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    provider = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text)
    duration = Column(String(50))
    level = Column(String(20))  # Beginner, Intermediate, Advanced
    is_free = Column(Boolean, default=True)
    career_id = Column(Integer, ForeignKey('career.id'))
    career = relationship("Career")

class Scholarship(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    provider = Column(String(100), nullable=False)
    description = Column(Text)
    amount = Column(String(50))
    eligibility = Column(Text)
    application_url = Column(String(500))
    deadline = Column(String(100))
    for_rural_students = Column(Boolean, default=False)

class CareerRecommendation(db.Model):
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    career_id = Column(Integer, ForeignKey('career.id'), nullable=False)
    match_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="recommendations")
    career = relationship("Career")