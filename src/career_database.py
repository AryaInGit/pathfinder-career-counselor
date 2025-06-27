from typing import Dict, List
from src.models import CareerPath, InterestCategory

class CareerDatabase:
    def __init__(self):
        self.careers = self._initialize_careers()
    
    def _initialize_careers(self) -> Dict[str, CareerPath]:
        careers = {}
        
        # STEM & Technology Careers - Enhanced with more relevant options
        careers["software_engineer"] = CareerPath(
            title="Software Engineer",
            category=InterestCategory.TECHNOLOGY,
            description="Design, develop, and maintain software applications and systems using various programming languages and frameworks",
            required_skills=["Programming", "Problem-solving", "Logical thinking", "Software Development", "Debugging"],
            education_requirements="Bachelor's degree in Computer Science, Software Engineering, or related field",
            average_salary="$85,000 - $150,000",
            job_outlook="Excellent (22% growth)",
            related_careers=["Data Scientist", "Web Developer", "Systems Analyst", "DevOps Engineer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["data_scientist"] = CareerPath(
            title="Data Scientist",
            category=InterestCategory.STEM,
            description="Analyze complex data using statistical methods, machine learning, and AI to help organizations make data-driven decisions",
            required_skills=["Statistics", "Programming", "Machine Learning", "Data visualization", "Python", "Critical thinking"],
            education_requirements="Bachelor's/Master's in Data Science, Statistics, Computer Science, or related field",
            average_salary="$95,000 - $165,000",
            job_outlook="Excellent (35% growth)",
            related_careers=["Machine Learning Engineer", "Business Analyst", "Statistician", "AI Research Scientist"],
            match_score=0.0,
            explanation=""
        )
        
        careers["ai_engineer"] = CareerPath(
            title="AI/Machine Learning Engineer",
            category=InterestCategory.TECHNOLOGY,
            description="Develop and implement artificial intelligence and machine learning solutions to solve complex problems",
            required_skills=["Machine Learning", "Deep Learning", "Python", "TensorFlow", "PyTorch", "NLP", "Computer Vision"],
            education_requirements="Bachelor's/Master's in Computer Science, AI, or related field",
            average_salary="$110,000 - $180,000",
            job_outlook="Excellent (40% growth)",
            related_careers=["Data Scientist", "Research Scientist", "Software Engineer", "NLP Engineer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["web_developer"] = CareerPath(
            title="Web Developer",
            category=InterestCategory.TECHNOLOGY,
            description="Create and maintain websites and web applications using various programming languages and frameworks",
            required_skills=["HTML/CSS", "JavaScript", "React", "Node.js", "Problem-solving", "UI/UX Design"],
            education_requirements="Bachelor's degree in Computer Science or equivalent experience/bootcamp",
            average_salary="$60,000 - $120,000",
            job_outlook="Good (13% growth)",
            related_careers=["Full-Stack Developer", "Frontend Developer", "UI/UX Designer", "Software Engineer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["cybersecurity_analyst"] = CareerPath(
            title="Cybersecurity Analyst",
            category=InterestCategory.TECHNOLOGY,
            description="Protect organizations from cyber threats by monitoring security systems and investigating security breaches",
            required_skills=["Network Security", "Risk Assessment", "Incident Response", "Ethical Hacking", "Problem-solving"],
            education_requirements="Bachelor's degree in Cybersecurity, Computer Science, or related field",
            average_salary="$80,000 - $140,000",
            job_outlook="Excellent (33% growth)",
            related_careers=["Information Security Manager", "Penetration Tester", "Security Consultant", "Network Administrator"],
            match_score=0.0,
            explanation=""
        )
        
        # Arts & Creative
        careers["ux_designer"] = CareerPath(
            title="UX/UI Designer",
            category=InterestCategory.ARTS,
            description="Design user interfaces and experiences for digital products, combining creativity with user research",
            required_skills=["User Research", "Prototyping", "Visual Design", "Figma", "Adobe Creative Suite", "Problem-solving"],
            education_requirements="Bachelor's degree in Design, HCI, or related field",
            average_salary="$70,000 - $130,000",
            job_outlook="Good (13% growth)",
            related_careers=["Product Designer", "Graphic Designer", "Web Designer", "Design Researcher"],
            match_score=0.0,
            explanation=""
        )
        
        careers["graphic_designer"] = CareerPath(
            title="Graphic Designer",
            category=InterestCategory.ARTS,
            description="Create visual concepts to communicate ideas through art and design for various media",
            required_skills=["Creativity", "Visual design", "Adobe Creative Suite", "Typography", "Communication"],
            education_requirements="Bachelor's degree in Graphic Design or related field",
            average_salary="$45,000 - $75,000",
            job_outlook="Good (3% growth)",
            related_careers=["UX/UI Designer", "Art Director", "Web Designer", "Brand Designer"],
            match_score=0.0,
            explanation=""
        )
        
        # Business & Finance - Tech-oriented
        careers["product_manager"] = CareerPath(
            title="Product Manager",
            category=InterestCategory.BUSINESS,
            description="Guide the development and strategy of products, working with engineering, design, and business teams",
            required_skills=["Strategic thinking", "Communication", "Data analysis", "Project management", "Technical understanding"],
            education_requirements="Bachelor's degree in Business, Engineering, or related field",
            average_salary="$90,000 - $160,000",
            job_outlook="Excellent (19% growth)",
            related_careers=["Technical Product Manager", "Business Analyst", "Project Manager", "Strategy Consultant"],
            match_score=0.0,
            explanation=""
        )
        
        careers["financial_analyst"] = CareerPath(
            title="Financial Analyst",
            category=InterestCategory.BUSINESS,
            description="Analyze financial data and trends to guide investment decisions and business strategy",
            required_skills=["Mathematics", "Analytical thinking", "Excel proficiency", "Financial modeling", "Communication"],
            education_requirements="Bachelor's degree in Finance, Economics, or related field",
            average_salary="$65,000 - $120,000",
            job_outlook="Good (6% growth)",
            related_careers=["Investment Banker", "Financial Advisor", "Budget Analyst", "Quantitative Analyst"],
            match_score=0.0,
            explanation=""
        )
        
        # Healthcare - Tech-related
        careers["health_informatics"] = CareerPath(
            title="Health Informatics Specialist",
            category=InterestCategory.HEALTHCARE,
            description="Use technology and data analysis to improve healthcare delivery and patient outcomes",
            required_skills=["Healthcare knowledge", "Data analysis", "Programming", "Database management", "Problem-solving"],
            education_requirements="Bachelor's/Master's in Health Informatics, Computer Science, or Healthcare + IT training",
            average_salary="$75,000 - $125,000",
            job_outlook="Excellent (8% growth)",
            related_careers=["Clinical Data Manager", "Healthcare Data Analyst", "Medical Software Developer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["doctor"] = CareerPath(
            title="Medical Doctor",
            category=InterestCategory.HEALTHCARE,
            description="Diagnose and treat illnesses while directly helping patients improve their health",
            required_skills=["Science knowledge", "Empathy", "Problem-solving", "Communication", "Critical thinking"],
            education_requirements="Medical degree (MD) + residency training (8+ years)",
            average_salary="$200,000 - $400,000",
            job_outlook="Excellent (4% growth)",
            related_careers=["Nurse Practitioner", "Physician Assistant", "Medical Researcher"],
            match_score=0.0,
            explanation=""
        )
        
        careers["physician_assistant"] = CareerPath(
            title="Physician Assistant",
            category=InterestCategory.HEALTHCARE,
            description="Provide healthcare services under physician supervision with direct patient interaction",
            required_skills=["Medical knowledge", "Diagnosis", "Patient care", "Communication"],
            education_requirements="Master's degree from accredited PA program",
            average_salary="$110,000 - $130,000",
            job_outlook="Excellent (31% growth)",
            related_careers=["Nurse Practitioner", "Medical Doctor", "Registered Nurse"],
            match_score=0.0,
            explanation=""
        )

        careers["medical_researcher"] = CareerPath(
            title="Medical Researcher",
            category=InterestCategory.HEALTHCARE,
            description="Conduct research to improve human health and advance medical knowledge",
            required_skills=["Research methodology", "Data analysis", "Scientific writing", "Biology"],
            education_requirements="PhD in Biomedical Sciences or related field",
            average_salary="$80,000 - $120,000",
            job_outlook="Good (8% growth)",
            related_careers=["Epidemiologist", "Biochemist", "Clinical Research Coordinator"],
            match_score=0.0,
            explanation=""
            )
        
        # Education - Tech-focused
        careers["computer_science_teacher"] = CareerPath(
            title="Computer Science Teacher",
            category=InterestCategory.EDUCATION,
            description="Teach programming, computer science concepts, and technology skills to students",
            required_skills=["Programming", "Communication", "Patience", "Curriculum development", "Teaching"],
            education_requirements="Bachelor's degree in Computer Science + teaching certification",
            average_salary="$50,000 - $80,000",
            job_outlook="Good (8% growth)",
            related_careers=["Corporate Trainer", "Curriculum Developer", "Educational Technology Specialist"],
            match_score=0.0,
            explanation=""
        )
        
        careers["teacher"] = CareerPath(
            title="Teacher",
            category=InterestCategory.EDUCATION,
            description="Educate and inspire students in various subjects and grade levels",
            required_skills=["Communication", "Patience", "Subject expertise", "Classroom management", "Empathy"],
            education_requirements="Bachelor's degree + teaching certification",
            average_salary="$45,000 - $70,000",
            job_outlook="Average (4% growth)",
            related_careers=["School Counselor", "Principal", "Curriculum Developer", "Educational Consultant"],
            match_score=0.0,
            explanation=""
        )
        
        # Research & Academia
        careers["research_scientist"] = CareerPath(
            title="Research Scientist",
            category=InterestCategory.STEM,
            description="Conduct research in specialized fields to advance knowledge and develop new technologies",
            required_skills=["Research methodology", "Critical thinking", "Data analysis", "Scientific writing", "Problem-solving"],
            education_requirements="PhD in relevant field",
            average_salary="$80,000 - $150,000",
            job_outlook="Good (7% growth)",
            related_careers=["University Professor", "R&D Engineer", "Data Scientist", "Lab Manager"],
            match_score=0.0,
            explanation=""
        )
        
        # Additional Technology Careers
        careers["devops_engineer"] = CareerPath(
            title="DevOps Engineer",
            category=InterestCategory.TECHNOLOGY,
            description="Bridge the gap between development and operations, focusing on automation and infrastructure",
            required_skills=["Cloud platforms", "CI/CD", "Containerization", "Scripting", "System administration"],
            education_requirements="Bachelor's in Computer Science or equivalent experience",
            average_salary="$90,000 - $150,000",
            job_outlook="Excellent (25% growth)",
            related_careers=["Software Engineer", "Systems Administrator", "Cloud Architect", "Site Reliability Engineer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["mobile_developer"] = CareerPath(
            title="Mobile App Developer",
            category=InterestCategory.TECHNOLOGY,
            description="Create mobile applications for iOS and Android platforms",
            required_skills=["Swift/Kotlin", "Mobile UI/UX", "API integration", "App store optimization", "Problem-solving"],
            education_requirements="Bachelor's in Computer Science or equivalent experience",
            average_salary="$70,000 - $130,000",
            job_outlook="Good (22% growth)",
            related_careers=["Web Developer", "Software Engineer", "UI/UX Designer", "Game Developer"],
            match_score=0.0,
            explanation=""
        )
        
        careers["game_developer"] = CareerPath(
            title="Game Developer",
            category=InterestCategory.TECHNOLOGY,
            description="Design and develop video games for various platforms using game engines and programming",
            required_skills=["Game engines", "Programming", "3D modeling", "Game design", "Mathematics"],
            education_requirements="Bachelor's in Computer Science, Game Development, or related field",
            average_salary="$65,000 - $120,000",
            job_outlook="Good (11% growth)",
            related_careers=["Software Engineer", "3D Artist", "Game Designer", "Animation Programmer"],
            match_score=0.0,
            explanation=""
        )
        
        # Creative Arts
        careers["digital_artist"] = CareerPath(
            title="Digital Artist",
            category=InterestCategory.ARTS,
            description="Create digital artwork for games, films, advertising, and other media",
            required_skills=["Digital art software", "Creativity", "Color theory", "Drawing", "3D modeling"],
            education_requirements="Bachelor's in Fine Arts, Digital Arts, or equivalent portfolio",
            average_salary="$50,000 - $90,000",
            job_outlook="Good (4% growth)",
            related_careers=["Graphic Designer", "Game Artist", "Animator", "Concept Artist"],
            match_score=0.0,
            explanation=""
        )
        
        careers["content_creator"] = CareerPath(
            title="Content Creator/Influencer",
            category=InterestCategory.ARTS,
            description="Create engaging content across digital platforms to build audiences and brand partnerships",
            required_skills=["Content creation", "Social media", "Video editing", "Marketing", "Communication"],
            education_requirements="Variable - often self-taught or communications/marketing degree",
            average_salary="$30,000 - $100,000+",
            job_outlook="Excellent (growing field)",
            related_careers=["Social Media Manager", "Digital Marketer", "Video Producer", "Brand Ambassador"],
            match_score=0.0,
            explanation=""
        )
        
        # Business & Finance
        careers["business_analyst"] = CareerPath(
            title="Business Analyst",
            category=InterestCategory.BUSINESS,
            description="Analyze business processes and requirements to improve organizational efficiency",
            required_skills=["Data analysis", "Process modeling", "Communication", "Problem-solving", "Documentation"],
            education_requirements="Bachelor's in Business, Economics, or related field",
            average_salary="$70,000 - $120,000",
            job_outlook="Good (14% growth)",
            related_careers=["Data Analyst", "Product Manager", "Management Consultant", "Project Manager"],
            match_score=0.0,
            explanation=""
        )
        
        careers["digital_marketer"] = CareerPath(
            title="Digital Marketing Specialist",
            category=InterestCategory.BUSINESS,
            description="Develop and execute online marketing campaigns across digital platforms",
            required_skills=["SEO/SEM", "Social media marketing", "Analytics", "Content marketing", "Email marketing"],
            education_requirements="Bachelor's in Marketing, Communications, or related field",
            average_salary="$55,000 - $95,000",
            job_outlook="Good (10% growth)",
            related_careers=["Content Creator", "Social Media Manager", "Brand Manager", "Growth Hacker"],
            match_score=0.0,
            explanation=""
        )
        
        return careers
    
    def get_all_careers(self) -> List[CareerPath]:
        """Get all available career paths"""
        return list(self.careers.values())
    
    def get_career_by_title(self, title: str) -> CareerPath:
        """Get a specific career by title"""
        for career in self.careers.values():
            if career.title.lower() == title.lower():
                return career
        return None
    
    def get_careers_by_category(self, category: InterestCategory) -> List[CareerPath]:
        """Get careers filtered by category"""
        return [career for career in self.careers.values() if career.category == category]
    
    def search_careers(self, query: str) -> List[CareerPath]:
        """Search careers by title, description, or skills"""
        query = query.lower()
        matching_careers = []
        
        for career in self.careers.values():
            if (query in career.title.lower() or 
                query in career.description.lower() or 
                any(query in skill.lower() for skill in career.required_skills)):
                matching_careers.append(career)
        
        return matching_careers
