from typing import List, Optional, Dict, Any
import json
from src.models import ConversationState, StudentProfile, CareerPath
from src.llm_client import LLMClient
from src.prompt_templates import PromptTemplates
from src.career_database import CareerDatabase
from src.career_matcher import CareerMatcher

class ConversationManager:
    def __init__(self):
        self.state = ConversationState()
        self.llm_client = LLMClient()
        self.prompt_templates = PromptTemplates()
        self.career_db = CareerDatabase()
        self.career_matcher = CareerMatcher(self.career_db, self.llm_client)
        self.questions_asked = 0  # Track number of questions asked
        
    def start_conversation(self) -> str:
        """Start the career counseling conversation"""
        self.state.current_step = "greeting"
        greeting_prompt = self.prompt_templates.get_greeting_prompt()
        
        response = self.llm_client.generate_response_sync(
            "Generate a warm, welcoming greeting to start a career counseling session with a student. Introduce yourself as PathFinder.",
            greeting_prompt
        )
        
        self._add_to_history("assistant", response)
        return response
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return appropriate response"""
        self._add_to_history("user", user_input)
        
        # Extract information from the conversation
        self._update_student_profile(user_input)
        
        # Determine next step based on current state and available information
        if self.state.current_step == "greeting":
            return self._handle_initial_response(user_input)
        elif self.state.current_step == "information_gathering":
            return self._handle_information_gathering(user_input)
        elif self.state.current_step == "clarification":
            return self._handle_clarification(user_input)
        elif self.state.current_step == "career_matching":
            return self._handle_career_matching()
        else:
            return self._handle_general_response(user_input)
    
    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.state.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": None  # In a real app, you'd add actual timestamps
        })
    
    def _update_student_profile(self, user_input: str):
        """Extract and update student profile information from user input"""
        # Get recent conversation context (last 4 messages)
        recent_messages = self.state.conversation_history[-4:] if len(self.state.conversation_history) >= 4 else self.state.conversation_history
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
        
        # Define schema for information extraction
        schema = {
            "name": "string or null",
            "interests": ["array of strings"],
            "hobbies": ["array of strings"],
            "preferred_subjects": ["array of strings"],
            "academic_scores": {"subject": "performance_level"},
            "career_goals": "string or null",
            "learning_style": "string or null",
            "extracurricular_activities": ["array of strings"],
            "work_environment_preference": "string or null"
        }
        
        # Extract structured information
        extracted_info = self.llm_client.extract_structured_data(conversation_text, schema)
        
        # Update student profile with extracted information
        if extracted_info:
            if extracted_info.get("name") and not self.state.student_profile.name:
                self.state.student_profile.name = extracted_info["name"]
            if extracted_info.get("interests"):
                new_interests = [interest for interest in extracted_info["interests"] 
                               if interest not in self.state.student_profile.interests]
                self.state.student_profile.interests.extend(new_interests)
            if extracted_info.get("hobbies"):
                new_hobbies = [hobby for hobby in extracted_info["hobbies"] 
                             if hobby not in self.state.student_profile.hobbies]
                self.state.student_profile.hobbies.extend(new_hobbies)
            if extracted_info.get("preferred_subjects"):
                new_subjects = [subject for subject in extracted_info["preferred_subjects"] 
                              if subject not in self.state.student_profile.preferred_subjects]
                self.state.student_profile.preferred_subjects.extend(new_subjects)
            if extracted_info.get("academic_scores"):
                self.state.student_profile.academic_scores.update(extracted_info["academic_scores"])
            if extracted_info.get("career_goals") and not self.state.student_profile.career_goals:
                self.state.student_profile.career_goals = extracted_info["career_goals"]
            if extracted_info.get("learning_style") and not self.state.student_profile.learning_style:
                self.state.student_profile.learning_style = extracted_info["learning_style"]
            if extracted_info.get("extracurricular_activities"):
                new_activities = [activity for activity in extracted_info["extracurricular_activities"] 
                                if activity not in self.state.student_profile.extracurricular_activities]
                self.state.student_profile.extracurricular_activities.extend(new_activities)
            if extracted_info.get("work_environment_preference") and not self.state.student_profile.work_environment_preference:
                self.state.student_profile.work_environment_preference = extracted_info["work_environment_preference"]
    
    def _get_conversation_text(self) -> str:
        """Get the full conversation as text"""
        conversation_parts = []
        for msg in self.state.conversation_history:
            role = "Student" if msg["role"] == "user" else "PathFinder"
            conversation_parts.append(f"{role}: {msg['content']}")
        return "\n".join(conversation_parts)
    
    def _handle_initial_response(self, user_input: str) -> str:
        """Handle the student's initial response"""
        self.state.current_step = "information_gathering"
        self.questions_asked = 0
        
        # Check if we have substantial information to proceed
        if self._has_substantial_information():
            # Generate a thoughtful response acknowledging their input and ask one targeted follow-up
            return self._generate_contextual_response(user_input)
        else:
            return self._ask_follow_up_questions()
    
    def _handle_information_gathering(self, user_input: str) -> str:
        """Handle ongoing information gathering"""
        self.questions_asked += 1
        
        # If we have enough information or asked too many questions, move to matching
        if self._has_sufficient_information() or self.questions_asked >= 3:
            self.state.current_step = "career_matching"
            return self._handle_career_matching()
        else:
            return self._generate_contextual_response(user_input)
    
    def _handle_clarification(self, user_input: str) -> str:
        """Handle clarification questions"""
        # Update profile with clarification
        self._update_student_profile(user_input)
        
        if self._has_sufficient_information():
            self.state.current_step = "career_matching"  
            return self._handle_career_matching()
        else:
            return self._generate_contextual_response(user_input)
    
    def _handle_career_matching(self) -> str:
        """Generate career recommendations"""
        if not self.state.career_recommendations:
            # Generate recommendations
            self.state.career_recommendations = self.career_matcher.find_matching_careers(
                self.state.student_profile
            )
        
        # Generate response with top recommendations
        return self._format_career_recommendations()
    
    def _handle_general_response(self, user_input: str) -> str:
        """Handle general conversation"""
        # Check if they're asking about specific careers or need more details
        if any(keyword in user_input.lower() for keyword in ['tell me more', 'details', 'how to', 'what about']):
            return self._provide_detailed_response(user_input)
        
        # Generate contextual response
        return self._generate_contextual_response(user_input)
    
    def _generate_contextual_response(self, user_input: str) -> str:
        """Generate a contextual response based on the conversation"""
        profile_summary = self._get_profile_summary()
        
        # Create a prompt that acknowledges their input and continues the conversation naturally
        prompt = f"""
        As PathFinder, a friendly AI career counselor, respond to the student's message: "{user_input}"
        
        Current student profile: {profile_summary}
        
        Guidelines:
        1. Acknowledge what they shared with enthusiasm
        2. Show genuine interest in their projects/experiences
        3. If they've shared substantial information about their interests, ask ONE specific follow-up question about their goals or preferences
        4. If you have enough information (name, interests, some background), suggest moving to career recommendations
        5. Keep the tone conversational and encouraging
        6. Don't ask multiple questions at once
        7. Don't repeat information they've already provided
        
        Respond naturally as PathFinder would in a real conversation.
        """
        
        try:
            response = self.llm_client.generate_response_sync(prompt)
            return response
        except Exception as e:
            print(f"Error generating contextual response: {e}")
            return "That's really interesting! I can see you have clear interests and passions. Would you like me to analyze your profile and suggest some career paths that might be perfect for you?"
    
    def _provide_detailed_response(self, user_input: str) -> str:
        """Provide detailed response to specific questions"""
        prompt = f"""
        As PathFinder, the student asked: "{user_input}"
        
        Student profile: {self._get_profile_summary()}
        Available recommendations: {[career.title for career in self.state.career_recommendations] if self.state.career_recommendations else 'None yet'}
        
        Provide a helpful, detailed response addressing their question.
        """
        
        return self.llm_client.generate_response_sync(prompt)
    
    def _has_substantial_information(self) -> bool:
        """Check if we have substantial information about the student"""
        profile = self.state.student_profile
        
        # Check for meaningful information
        has_name = bool(profile.name)
        has_interests = len(profile.interests) > 0 or len(profile.hobbies) > 0
        has_some_detail = (len(profile.preferred_subjects) > 0 or 
                          profile.career_goals or 
                          len(profile.extracurricular_activities) > 0)
        
        return has_name and has_interests and has_some_detail
    
    def _has_sufficient_information(self) -> bool:
        """Check if we have enough information to make career recommendations"""
        profile = self.state.student_profile
        
        # Basic requirements for career matching
        has_interests = len(profile.interests) > 0 or len(profile.hobbies) > 0
        has_academics = len(profile.preferred_subjects) > 0 or len(profile.academic_scores) > 0
        has_some_direction = profile.career_goals or len(profile.extracurricular_activities) > 0
        
        return has_interests and (has_academics or has_some_direction)
    
    def _ask_follow_up_questions(self) -> str:
        """Generate appropriate follow-up questions"""
        missing_areas = self._identify_missing_information()
        
        if not missing_areas:
            # Use general clarifying questions
            return self.llm_client.generate_response_sync(
                "",
                self.prompt_templates.get_clarifying_questions_prompt(self.state.student_profile)
            )
        
        # Generate targeted questions for missing areas
        prompt = f"""
        As PathFinder, generate 1-2 friendly follow-up questions to learn more about the student's:
        {', '.join(missing_areas)}
        
        Current profile: {self._get_profile_summary()}
        
        Make the questions conversational and engaging.
        """
        
        return self.llm_client.generate_response_sync(prompt)
    
    def _identify_missing_information(self) -> List[str]:
        """Identify what information is still missing"""
        missing = []
        profile = self.state.student_profile
        
        if not profile.name:
            missing.append("name")
        if not profile.interests and not profile.hobbies:
            missing.append("interests or hobbies")
        if not profile.preferred_subjects:
            missing.append("favorite subjects")
        if not profile.career_goals:
            missing.append("career goals or aspirations")
        
        return missing
    
    def _get_profile_summary(self) -> str:
        """Get a summary of the current student profile"""
        profile = self.state.student_profile
        summary_parts = []
        
        if profile.name:
            summary_parts.append(f"Name: {profile.name}")
        if profile.interests:
            summary_parts.append(f"Interests: {', '.join(profile.interests)}")
        if profile.hobbies:
            summary_parts.append(f"Hobbies: {', '.join(profile.hobbies)}")
        if profile.preferred_subjects:
            summary_parts.append(f"Favorite subjects: {', '.join(profile.preferred_subjects)}")
        if profile.career_goals:
            summary_parts.append(f"Career goals: {profile.career_goals}")
        if profile.extracurricular_activities:
            summary_parts.append(f"Activities: {', '.join(profile.extracurricular_activities)}")
        
        return "; ".join(summary_parts) if summary_parts else "Limited information available"
    
    def _format_career_recommendations(self) -> str:
        """Format career recommendations into a response"""
        if not self.state.career_recommendations:
            return "I'd love to help you find great career matches, but I need a bit more information about your interests and goals first. Could you tell me more about what you enjoy doing?"
        
        top_careers = self.state.career_recommendations[:3]
        student_name = self.state.student_profile.name or "there"
        
        prompt = f"""
        As PathFinder, present these top 3 career recommendations to {student_name}:
        
        {self._format_careers_for_prompt(top_careers)}
        
        Guidelines:
        1. Be enthusiastic and encouraging
        2. Mention why each career matches their profile
        3. Include key details like salary and job outlook
        4. Ask if they'd like to know more about any specific career
        5. Keep it conversational and personalized
        
        Present this as a friendly career counselor would.
        """
        
        try:
            response = self.llm_client.generate_response_sync(prompt)
            return response
        except Exception as e:
            print(f"Error formatting recommendations: {e}")
            # Fallback to simple formatting
            return self._format_recommendations_simple(top_careers)
    
    def _format_careers_for_prompt(self, careers: List[CareerPath]) -> str:
        """Format careers for LLM prompt"""
        formatted = []
        for i, career in enumerate(careers, 1):
            formatted.append(f"""
            {i}. {career.title} ({career.match_score:.0%} match)
            - Description: {career.description}
            - Salary: {career.average_salary}
            - Job Outlook: {career.job_outlook}
            - Why it matches: {career.explanation}
            """)
        return "\n".join(formatted)
    
    def _format_recommendations_simple(self, careers: List[CareerPath]) -> str:
        """Simple fallback formatting for recommendations"""
        response = f"Great news! I've found some excellent career matches for you:\n\n"
        
        for i, career in enumerate(careers, 1):
            response += f"{i}. **{career.title}** ({career.match_score:.0%} match)\n"
            response += f"   {career.description}\n"
            response += f"   💰 Salary: {career.average_salary}\n"
            response += f"   📈 Outlook: {career.job_outlook}\n\n"
        
        response += "Would you like to learn more about any of these careers?"
        return response
