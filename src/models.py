from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class InterestCategory(Enum):
    STEM = "STEM"
    ARTS = "Arts & Creative"
    BUSINESS = "Business & Finance"
    HEALTHCARE = "Healthcare & Medicine"
    EDUCATION = "Education & Training"
    SPORTS = "Sports & Recreation"
    SOCIAL_SERVICES = "Social Services"
    TECHNOLOGY = "Technology & IT"
    LAW = "Law & Legal"
    ENVIRONMENT = "Environment & Sustainability"

class AcademicLevel(Enum):
    EXCELLENT = "Excellent (90-100%)"
    GOOD = "Good (80-89%)"
    AVERAGE = "Average (70-79%)"
    BELOW_AVERAGE = "Below Average (60-69%)"
    NEEDS_IMPROVEMENT = "Needs Improvement (<60%)"

class StudentProfile(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade_level: Optional[str] = None
    interests: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
    academic_scores: Dict[str, str] = Field(default_factory=dict)
    preferred_subjects: List[str] = Field(default_factory=list)
    career_goals: Optional[str] = None
    learning_style: Optional[str] = None
    extracurricular_activities: List[str] = Field(default_factory=list)
    work_environment_preference: Optional[str] = None

class CareerPath(BaseModel):
    title: str
    category: InterestCategory
    description: str
    required_skills: List[str]
    education_requirements: str
    average_salary: str
    job_outlook: str
    related_careers: List[str]
    match_score: float = Field(ge=0.0, le=1.0)
    explanation: str

class ConversationState(BaseModel):
    current_step: str = "greeting"
    student_profile: StudentProfile = Field(default_factory=StudentProfile)
    missing_info: List[str] = Field(default_factory=list)
    career_recommendations: List[CareerPath] = Field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    
class CareerSuggestion(BaseModel):
    title: str
    category: str
    description: str
    required_skills: List[str]
    education_requirements: str
    average_salary: str
    job_outlook: str
    explanation: str
    match_score: float
    work_environment: str
    personalized_match_reason: str
    salary_range: str
    demand_level: str
    education_path: str
    experience_required: str
    key_skills: List[Dict[str, Any]]
