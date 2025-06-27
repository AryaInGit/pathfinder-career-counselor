from typing import List, Dict, Any
import re
from src.models import StudentProfile, CareerPath, InterestCategory
from src.career_database import CareerDatabase
from src.llm_client import LLMClient

class CareerMatcher:
    def __init__(self, career_db: CareerDatabase, llm_client: LLMClient):
        self.career_db = career_db
        self.llm_client = llm_client
        
        # Define comprehensive interest-to-category mappings
        self.interest_mappings = {
            # STEM & Technology - Enhanced mappings
            'programming': InterestCategory.TECHNOLOGY,
            'coding': InterestCategory.TECHNOLOGY,
            'computer': InterestCategory.TECHNOLOGY,
            'technology': InterestCategory.TECHNOLOGY,
            'software': InterestCategory.TECHNOLOGY,
            'web development': InterestCategory.TECHNOLOGY,
            'app development': InterestCategory.TECHNOLOGY,
            'artificial intelligence': InterestCategory.TECHNOLOGY,
            'ai': InterestCategory.TECHNOLOGY,
            'machine learning': InterestCategory.TECHNOLOGY,
            'ml': InterestCategory.TECHNOLOGY,
            'nlp': InterestCategory.TECHNOLOGY,
            'natural language processing': InterestCategory.TECHNOLOGY,
            'data science': InterestCategory.STEM,
            'algorithms': InterestCategory.TECHNOLOGY,
            'python': InterestCategory.TECHNOLOGY,
            'javascript': InterestCategory.TECHNOLOGY,
            'react': InterestCategory.TECHNOLOGY,
            'streamlit': InterestCategory.TECHNOLOGY,
            'llm': InterestCategory.TECHNOLOGY,
            'large language models': InterestCategory.TECHNOLOGY,
            
            'math': InterestCategory.STEM,
            'mathematics': InterestCategory.STEM,
            'science': InterestCategory.STEM,
            'physics': InterestCategory.STEM,
            'chemistry': InterestCategory.STEM,
            'biology': InterestCategory.STEM,
            'engineering': InterestCategory.STEM,
            'data': InterestCategory.STEM,
            'statistics': InterestCategory.STEM,
            'analytics': InterestCategory.STEM,
            
            # Arts & Creative - Enhanced mappings
            'art': InterestCategory.ARTS,
            'arts': InterestCategory.ARTS,
            'creative': InterestCategory.ARTS,
            'creativity': InterestCategory.ARTS,
            'drawing': InterestCategory.ARTS,
            'painting': InterestCategory.ARTS,
            'music': InterestCategory.ARTS,
            'singing': InterestCategory.ARTS,
            'design': InterestCategory.ARTS,
            'graphic design': InterestCategory.ARTS,
            'visual design': InterestCategory.ARTS,
            'photography': InterestCategory.ARTS,
            'writing': InterestCategory.ARTS,
            'creative writing': InterestCategory.ARTS,
            'literature': InterestCategory.ARTS,
            'drama': InterestCategory.ARTS,
            'theater': InterestCategory.ARTS,
            'theatre': InterestCategory.ARTS,
            'film': InterestCategory.ARTS,
            'video': InterestCategory.ARTS,
            'animation': InterestCategory.ARTS,
            'illustration': InterestCategory.ARTS,
            'digital art': InterestCategory.ARTS,
            'fine arts': InterestCategory.ARTS,
            'visual arts': InterestCategory.ARTS,
            'english': InterestCategory.ARTS,  # English often relates to creative writing
            
            # Healthcare
            'health': InterestCategory.HEALTHCARE,
            'medicine': InterestCategory.HEALTHCARE,
            'medical': InterestCategory.HEALTHCARE,
            'helping people': InterestCategory.HEALTHCARE,
            'care': InterestCategory.HEALTHCARE,
            'nursing': InterestCategory.HEALTHCARE,
            'doctor': InterestCategory.HEALTHCARE,
            'physician': InterestCategory.HEALTHCARE,
            'helping people': InterestCategory.HEALTHCARE,
            'patient care': InterestCategory.HEALTHCARE,
            'human health': InterestCategory.HEALTHCARE,
            'medical care': InterestCategory.HEALTHCARE,
            
            # Business & Finance
            'business': InterestCategory.BUSINESS,
            'finance': InterestCategory.BUSINESS,
            'money': InterestCategory.BUSINESS,
            'economics': InterestCategory.BUSINESS,
            'marketing': InterestCategory.BUSINESS,
            'sales': InterestCategory.BUSINESS,
            'management': InterestCategory.BUSINESS,
            'entrepreneurship': InterestCategory.BUSINESS,
            'startup': InterestCategory.BUSINESS,
            
            # Education
            'teaching': InterestCategory.EDUCATION,
            'education': InterestCategory.EDUCATION,
            'tutoring': InterestCategory.EDUCATION,
            'mentoring': InterestCategory.EDUCATION,
            
            # Sports & Recreation
            'sports': InterestCategory.SPORTS,
            'athletics': InterestCategory.SPORTS,
            'fitness': InterestCategory.SPORTS,
            'exercise': InterestCategory.SPORTS,
            'physical': InterestCategory.SPORTS,
            
            # Social Services
            'social work': InterestCategory.SOCIAL_SERVICES,
            'community': InterestCategory.SOCIAL_SERVICES,
            'volunteering': InterestCategory.SOCIAL_SERVICES,
            'counseling': InterestCategory.SOCIAL_SERVICES,
            
            # Law
            'law': InterestCategory.LAW,
            'legal': InterestCategory.LAW,
            'justice': InterestCategory.LAW,
            'debate': InterestCategory.LAW,
            
            # Environment
            'environment': InterestCategory.ENVIRONMENT,
            'nature': InterestCategory.ENVIRONMENT,
            'outdoors': InterestCategory.ENVIRONMENT,
            'sustainability': InterestCategory.ENVIRONMENT,
        }
        
        # Technology-specific keywords for enhanced matching
        self.tech_keywords = [
            'coding', 'programming', 'software', 'ai', 'artificial intelligence',
            'machine learning', 'nlp', 'natural language processing', 'data science',
            'web development', 'app development', 'python', 'javascript', 'react',
            'streamlit', 'llm', 'algorithms', 'computer science', 'technology'
        ]
        
        # Creative/Arts keywords for enhanced matching
        self.creative_keywords = [
            'art', 'arts', 'creative', 'creativity', 'design', 'drawing', 'painting',
            'music', 'writing', 'literature', 'photography', 'visual', 'graphic',
            'illustration', 'animation', 'film', 'video', 'theater', 'drama'
        ]
    
    def find_matching_careers(self, student_profile: StudentProfile) -> List[CareerPath]:
        """Find careers that match the student's profile with improved accuracy"""
        all_careers = self.career_db.get_all_careers()
        scored_careers = []
        
        # Get primary interest categories
        primary_categories = self._get_primary_categories(student_profile)
        
        for career in all_careers:
            # Calculate match score with enhanced logic
            match_score = self._calculate_match_score(student_profile, career)
            
            # Apply strict filtering based on primary interests
            if self._should_include_career(student_profile, career, match_score, primary_categories):
                # Generate personalized explanation using LLM
                explanation = self._generate_career_explanation(student_profile, career, match_score)
                
                # Create a copy with updated score and explanation
                matched_career = CareerPath(
                    title=career.title,
                    category=career.category,
                    description=career.description,
                    required_skills=career.required_skills,
                    education_requirements=career.education_requirements,
                    average_salary=career.average_salary,
                    job_outlook=career.job_outlook,
                    related_careers=career.related_careers,
                    match_score=match_score,
                    explanation=explanation
                )
                
                scored_careers.append(matched_career)
        
        # Sort by match score and return top matches
        sorted_careers = sorted(scored_careers, key=lambda x: x.match_score, reverse=True)
        
        return sorted_careers[:8]  # Return top 8 matches
    
    def _get_primary_categories(self, student_profile: StudentProfile) -> List[InterestCategory]:
        """Identify the primary interest categories for the student"""
        all_interests = (student_profile.interests + student_profile.hobbies + 
                        student_profile.preferred_subjects)
        
        category_scores = {}
        
        for interest in all_interests:
            interest_lower = interest.lower()
            
            # Check for direct keyword matches
            for keyword, category in self.interest_mappings.items():
                if keyword in interest_lower:
                    category_scores[category] = category_scores.get(category, 0) + 1
            
            # Boost scores for strong indicators
            if any(tech_word in interest_lower for tech_word in self.tech_keywords):
                category_scores[InterestCategory.TECHNOLOGY] = category_scores.get(InterestCategory.TECHNOLOGY, 0) + 2
                category_scores[InterestCategory.STEM] = category_scores.get(InterestCategory.STEM, 0) + 1
            
            if any(creative_word in interest_lower for creative_word in self.creative_keywords):
                category_scores[InterestCategory.ARTS] = category_scores.get(InterestCategory.ARTS, 0) + 2
        
        # Return categories with score > 0, sorted by score
        primary_categories = [cat for cat, score in sorted(category_scores.items(), key=lambda x: x[1], reverse=True) if score > 0]
        
        return primary_categories[:3]  # Top 3 categories
    
    def _should_include_career(self, student_profile: StudentProfile, career: CareerPath, 
                              match_score: float, primary_categories: List[InterestCategory]) -> bool:
        """Determine if a career should be included in recommendations"""
        
        # Minimum match score threshold
        if match_score < 0.25:
            return False
        
        # If we have clear primary categories, be strict about relevance
        if primary_categories:
            # Career must be in one of the primary categories OR have a high match score
            if career.category not in primary_categories and match_score < 0.6:
                return False
            
            # Special case: Don't recommend healthcare careers unless there's clear interest
            if (career.category == InterestCategory.HEALTHCARE and 
                InterestCategory.HEALTHCARE not in primary_categories and
                match_score < 0.7):
                return False
            
            # Special case: Don't recommend tech careers for purely creative students
            if (career.category in [InterestCategory.TECHNOLOGY, InterestCategory.STEM] and
                primary_categories == [InterestCategory.ARTS] and
                match_score < 0.5):
                return False
            
            # Special case: Don't recommend creative careers for purely tech students
            if (career.category == InterestCategory.ARTS and
                primary_categories == [InterestCategory.TECHNOLOGY] and
                match_score < 0.5):
                return False
        
        return True
    
    def _calculate_match_score(self, student_profile: StudentProfile, career: CareerPath) -> float:
        """Calculate how well a career matches a student's profile with enhanced accuracy"""
        score = 0.0
        total_weight = 0.0
        
        # Interest matching (weight: 0.4) - Increased weight for interests
        interest_score = self._calculate_interest_match(student_profile, career)
        score += interest_score * 0.4
        total_weight += 0.4
        
        # Academic subject matching (weight: 0.25)
        academic_score = self._calculate_academic_match(student_profile, career)
        score += academic_score * 0.25
        total_weight += 0.25
        
        # Skills alignment (weight: 0.2)
        skills_score = self._calculate_skills_match(student_profile, career)
        score += skills_score * 0.2
        total_weight += 0.2
        
        # Career goals alignment (weight: 0.15)
        goals_score = self._calculate_goals_match(student_profile, career)
        score += goals_score * 0.15
        total_weight += 0.15
        
        return min(score / total_weight if total_weight > 0 else 0.0, 1.0)
    
    def _calculate_interest_match(self, student_profile: StudentProfile, career: CareerPath) -> float:
        """Calculate interest matching score with enhanced keyword matching"""
        if not student_profile.interests and not student_profile.hobbies:
            return 0.0
        
        all_interests = student_profile.interests + student_profile.hobbies
        match_score = 0.0
        total_interests = len(all_interests)
        
        if total_interests == 0:
            return 0.0
        
        career_keywords = self._extract_career_keywords(career)
        
        for interest in all_interests:
            interest_lower = interest.lower()
            
            # Direct keyword matching with career
            if any(keyword in interest_lower for keyword in career_keywords):
                match_score += 1.0
                continue
            
            # Category-based matching
            interest_category = self._get_interest_category(interest)
            if interest_category == career.category:
                match_score += 0.8
                continue
            
            # Skill-based matching
            if any(skill.lower() in interest_lower or interest_lower in skill.lower() 
                   for skill in career.required_skills):
                match_score += 0.6
                continue
            
            # Partial text matching
            if any(word in interest_lower for word in career.title.lower().split()):
                match_score += 0.4
        
        return min(match_score / total_interests, 1.0)
    
    def _calculate_academic_match(self, student_profile: StudentProfile, career: CareerPath) -> float:
        """Calculate academic subject matching score"""
        if not student_profile.preferred_subjects:
            return 0.5  # Neutral score if no academic info
        
        match_score = 0.0
        total_subjects = len(student_profile.preferred_subjects)
        
        subject_career_mappings = {
            'computer science': ['Software Engineer', 'Data Scientist', 'AI/Machine Learning Engineer', 'Web Developer'],
            'mathematics': ['Data Scientist', 'Financial Analyst', 'Research Scientist', 'AI/Machine Learning Engineer'],
            'art': ['UX/UI Designer', 'Graphic Designer', 'Digital Artist', 'Content Creator'],
            'biology': ['Medical Doctor', 'Medical Researcher', 'Health Informatics Specialist'],
            'business': ['Product Manager', 'Financial Analyst', 'Business Analyst', 'Digital Marketing Specialist'],
            'english': ['Content Creator', 'Digital Marketing Specialist', 'Teacher'],
            'physics': ['Research Scientist', 'Data Scientist', 'Software Engineer'],
            'chemistry': ['Medical Researcher', 'Research Scientist', 'Medical Doctor']
        }
        
        for subject in student_profile.preferred_subjects:
            subject_lower = subject.lower()
            
            # Direct mapping
            if subject_lower in subject_career_mappings:
                if career.title in subject_career_mappings[subject_lower]:
                    match_score += 1.0
                    continue
            
            # Partial keyword matching
            if any(word in subject_lower for word in career.title.lower().split()):
                match_score += 0.6
                continue
            
            # Category-based matching
            if subject_lower in ['math', 'mathematics', 'science', 'physics', 'chemistry']:
                if career.category in [InterestCategory.STEM, InterestCategory.TECHNOLOGY]:
                    match_score += 0.5
        
        return min(match_score / total_subjects, 1.0)
    
    def _calculate_skills_match(self, student_profile: StudentProfile, career: CareerPath) -> float:
        """Calculate skills alignment score"""
        all_activities = (student_profile.extracurricular_activities + 
                         student_profile.interests + student_profile.hobbies)
        
        if not all_activities:
            return 0.5  # Neutral score
        
        match_score = 0.0
        skill_matches = 0
        
        for activity in all_activities:
            activity_lower = activity.lower()
            for skill in career.required_skills:
                skill_lower = skill.lower()
                if (skill_lower in activity_lower or activity_lower in skill_lower or
                    any(word in activity_lower for word in skill_lower.split())):
                    match_score += 1.0
                    skill_matches += 1
                    break
        
        # Bonus for multiple skill matches
        if skill_matches >= 3:
            match_score *= 1.2
        elif skill_matches >= 2:
            match_score *= 1.1
        
        return min(match_score / len(career.required_skills), 1.0)
    
    def _calculate_goals_match(self, student_profile: StudentProfile, career: CareerPath) -> float:
        """Calculate career goals alignment score"""
        if not student_profile.career_goals:
            return 0.5  # Neutral score
        
        goals_text = student_profile.career_goals.lower()
        career_text = (career.title + " " + career.description).lower()
        
        # Keyword matching
        common_words = set(goals_text.split()) & set(career_text.split())
        if len(common_words) >= 3:
            return 0.9
        elif len(common_words) >= 2:
            return 0.7
        elif len(common_words) >= 1:
            return 0.5
        
        return 0.3
    
    def _extract_career_keywords(self, career: CareerPath) -> List[str]:
        """Extract relevant keywords from career information"""
        keywords = []
        
        # Add title words
        keywords.extend(career.title.lower().split())
        
        # Add category-specific keywords
        if career.category == InterestCategory.TECHNOLOGY:
            keywords.extend(self.tech_keywords)
        elif career.category == InterestCategory.ARTS:
            keywords.extend(self.creative_keywords)
        
        # Add skill keywords
        keywords.extend([skill.lower() for skill in career.required_skills])
        
        return list(set(keywords))  # Remove duplicates
    
    def _get_interest_category(self, interest: str) -> InterestCategory:
        """Get the category for a given interest"""
        interest_lower = interest.lower()
        
        for keyword, category in self.interest_mappings.items():
            if keyword in interest_lower:
                return category
        
        return None
    
    def _generate_career_explanation(self, student_profile: StudentProfile, career: CareerPath, match_score: float) -> str:
        """Generate personalized explanation for career match using LLM"""
        try:
            # Create context for LLM
            student_info = f"""
            Interests: {', '.join(student_profile.interests)}
            Hobbies: {', '.join(student_profile.hobbies)}
            Preferred subjects: {', '.join(student_profile.preferred_subjects)}
            Career goals: {student_profile.career_goals or 'Not specified'}
            """
            
            career_info = f"""
            Title: {career.title}
            Description: {career.description}
            Required skills: {', '.join(career.required_skills)}
            """
            
            prompt = f"""
            Based on this student's profile and career information, explain in 1-2 sentences why this career is a {match_score:.0%} match.
            
            Student profile: {student_info}
            Career: {career_info}
            
            Focus on specific connections between their interests/skills and the career requirements.
            Be encouraging and specific.
            """
            
            explanation = self.llm_client.generate_response_sync(prompt)
            return explanation if explanation else f"This career aligns well with your interests and has a {match_score:.0%} compatibility score."
            
        except Exception as e:
            print(f"Error generating career explanation: {e}")
            return f"This career shows strong alignment with your profile ({match_score:.0%} match)."
