import streamlit as st
import asyncio
import os
from datetime import datetime
from src.conversation_manager import ConversationManager
from src.models import StudentProfile
from src.career_database import CareerDatabase
from src.career_matcher import CareerMatcher
from src.llm_client import LLMClient

# Configure page
st.set_page_config(
    page_title="PathFinder - AI Career Counselor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .career-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #4f46e5;
    }
    
    .match-score {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .scenario-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .scenario-card:hover {
        background: #e2e8f0;
        transform: translateY(-2px);
    }
    
    .chat-container {
        background: #f8fafc;
        padding: 0rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .user-message {
        background: #4f46e5;
        color: white;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        text-align: right;
    }
    
    .assistant-message {
        background: white;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    if 'career_db' not in st.session_state:
        st.session_state.career_db = CareerDatabase()
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = LLMClient()
    if 'career_matcher' not in st.session_state:
        st.session_state.career_matcher = CareerMatcher(
            st.session_state.career_db, 
            st.session_state.llm_client
        )
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'quick_recommendations' not in st.session_state:
        st.session_state.quick_recommendations = []

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 PathFinder - AI Career Counselor</h1>
        <p>Discover your ideal career path through AI-powered recommendations</p>
        <p style="font-size: 0.9em; opacity: 0.9;">⚡    Powered by Groq for ultra-fast responses</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with navigation and profile info"""
    with st.sidebar:
        st.header("🎯 Navigation")
        
        # Mode selection
        if st.session_state.current_mode is None:
            st.subheader("Choose Your Experience")
            
            if st.button("🚀 Quick Mode", use_container_width=True):
                st.session_state.current_mode = "quick"
                st.rerun()
            
            if st.button("💬 Conversational Mode", use_container_width=True):
                st.session_state.current_mode = "conversational"
                st.session_state.conversation_started = False
                st.rerun()
        
        else:
            # Show current mode and reset option
            st.info(f"Current Mode: {st.session_state.current_mode.title()}")
            
            if st.button("🔄 Switch Mode", use_container_width=True):
                st.session_state.current_mode = None
                st.session_state.conversation_started = False
                st.session_state.chat_history = []
                st.session_state.quick_recommendations = []
                st.rerun()
        
        # Display profile information if available
        if hasattr(st.session_state.conversation_manager, 'state'):
            profile = st.session_state.conversation_manager.state.student_profile
            if profile.name or profile.interests or profile.hobbies:
                st.subheader("👤 Your Profile")
                if profile.name:
                    st.write(f"**Name:** {profile.name}")
                if profile.interests:
                    st.write(f"**Interests:** {', '.join(profile.interests[:3])}{'...' if len(profile.interests) > 3 else ''}")
                if profile.hobbies:
                    st.write(f"**Hobbies:** {', '.join(profile.hobbies[:3])}{'...' if len(profile.hobbies) > 3 else ''}")
        
        # API Status
        st.subheader("🔧 System Status")
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            st.success("✅ Groq API Connected")
        else:
            st.error("❌ Groq API Key Missing")
            st.info("Add GROQ_API_KEY to your environment variables")

def display_quick_mode():
    """Display quick recommendation mode"""
    st.header("🚀 Quick Career Recommendations")
    st.write("Select a scenario that matches your interests for instant career recommendations:")
    
    # Define scenarios
    scenarios = {
        "🖥️ Technology Enthusiast": {
            "description": "I love coding, AI, and building software solutions",
            "profile": {
                "interests": ["programming", "artificial intelligence", "software development", "problem-solving"],
                "hobbies": ["coding projects", "tech blogs", "hackathons"],
                "preferred_subjects": ["computer science", "mathematics", "physics"],
                "career_goals": "Build innovative technology solutions that solve real-world problems"
            }
        },
        "🎨 Creative Designer": {
            "description": "I enjoy art, design, and visual creativity",
            "profile": {
                "interests": ["graphic design", "user experience", "visual arts", "creativity"],
                "hobbies": ["drawing", "photography", "digital art"],
                "preferred_subjects": ["art", "design", "english"],
                "career_goals": "Create beautiful and functional designs that inspire people"
            }
        },
        "🔬 Science Explorer": {
            "description": "I'm fascinated by research, data, and scientific discovery",
            "profile": {
                "interests": ["data science", "research", "analytics", "scientific discovery"],
                "hobbies": ["reading research papers", "data visualization", "experiments"],
                "preferred_subjects": ["mathematics", "statistics", "biology", "chemistry"],
                "career_goals": "Use data and research to make important discoveries"
            }
        },
        "💼 Business Leader": {
            "description": "I'm interested in entrepreneurship, strategy, and leadership",
            "profile": {
                "interests": ["business strategy", "entrepreneurship", "leadership", "innovation"],
                "hobbies": ["reading business books", "networking", "startup events"],
                "preferred_subjects": ["economics", "business studies", "mathematics"],
                "career_goals": "Lead teams and build successful businesses"
            }
        },
        "🏥 Healthcare Helper": {
            "description": "I want to help people and work in healthcare",
            "profile": {
                "interests": ["helping people", "medicine", "health", "patient care"],
                "hobbies": ["volunteering", "health research", "fitness"],
                "preferred_subjects": ["biology", "chemistry", "psychology"],
                "career_goals": "Make a positive impact on people's health and wellbeing"
            }
        },
        "🎓 Education Advocate": {
            "description": "I love teaching, mentoring, and sharing knowledge",
            "profile": {
                "interests": ["teaching", "education", "mentoring", "knowledge sharing"],
                "hobbies": ["tutoring", "reading", "educational content creation"],
                "preferred_subjects": ["english", "history", "mathematics"],
                "career_goals": "Inspire and educate the next generation"
            }
        }
    }
    
    # Display scenarios
    cols = st.columns(2)
    for i, (title, scenario) in enumerate(scenarios.items()):
        with cols[i % 2]:
            if st.button(f"{title}\n{scenario['description']}", key=f"scenario_{i}", use_container_width=True):
                generate_quick_recommendations(title, scenario)

def generate_quick_recommendations(scenario_title, scenario):
    """Generate quick career recommendations for selected scenario"""
    with st.spinner("⚡ Generating recommendations with Groq..."):
        try:
            # Create student profile from scenario
            profile = StudentProfile(
                name="Student",
                interests=scenario["profile"]["interests"],
                hobbies=scenario["profile"]["hobbies"],
                preferred_subjects=scenario["profile"]["preferred_subjects"],
                career_goals=scenario["profile"]["career_goals"]
            )
            
            # Get career recommendations
            recommendations = st.session_state.career_matcher.find_matching_careers(profile)
            
            if recommendations:
                st.session_state.quick_recommendations = recommendations[:3]
                display_quick_recommendations(scenario_title)
            else:
                st.error("No recommendations found. Please try a different scenario.")
                
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")

def display_quick_recommendations(scenario_title):
    """Display career recommendations in a beautiful format"""
    st.success(f"✨ Top Career Matches for {scenario_title}")
    
    for i, career in enumerate(st.session_state.quick_recommendations, 1):
        with st.container():
            st.markdown(f"""
            <div class="career-card">
                <h3>{i}. {career.title}</h3>
                <div class="match-score">Match Score: {career.match_score:.0%}</div>
                <p>{career.description}</p>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                    <div><strong>💰 Salary:</strong> {career.average_salary}</div>
                    <div><strong>📈 Job Outlook:</strong> {career.job_outlook}</div>
                </div>
                <div><strong>🎓 Education:</strong> {career.education_requirements}</div>
                {f'<div style="margin-top: 1rem;"><strong>💡 Why this matches:</strong> {career.explanation}</div>' if career.explanation else ''}
            </div>
            """, unsafe_allow_html=True)
    
    # Show skills and related careers for the top match
    if st.session_state.quick_recommendations:
        top_career = st.session_state.quick_recommendations[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🛠️ Required Skills for {top_career.title}")
            for skill in top_career.required_skills:
                st.write(f"• {skill}")
        
        with col2:
            if top_career.related_careers:
                st.subheader("🔗 Related Careers")
                for related in top_career.related_careers:
                    st.write(f"• {related}")

def display_conversational_mode():
    """Display conversational career counseling mode"""
    st.header("💬 AI Career Counseling")
    st.write("Have a personalized conversation with PathFinder to discover your ideal career path.")
    
    # Initialize conversation if not started
    if not st.session_state.conversation_started:
        with st.spinner("Starting conversation..."):
            try:
                greeting = st.session_state.conversation_manager.start_conversation()
                st.session_state.chat_history.append({"role": "assistant", "content": greeting})
                st.session_state.conversation_started = True
            except Exception as e:
                st.error(f"Error starting conversation: {str(e)}")
                return
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>PathFinder:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("PathFinder is thinking..."):
            try:
                response = st.session_state.conversation_manager.process_user_input(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Check if we have career recommendations
                if st.session_state.conversation_manager.state.career_recommendations:
                    display_conversation_recommendations()
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        st.rerun()

def display_conversation_recommendations():
    """Display career recommendations from conversational mode"""
    recommendations = st.session_state.conversation_manager.state.career_recommendations
    
    if recommendations:
        st.subheader("🎯 Your Personalized Career Recommendations")
        
        for i, career in enumerate(recommendations[:5], 1):
            with st.expander(f"{i}. {career.title} - {career.match_score:.0%} Match"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {career.description}")
                    if career.explanation:
                        st.write(f"**Why this matches you:** {career.explanation}")
                    st.write(f"**Education Required:** {career.education_requirements}")
                
                with col2:
                    st.metric("Salary Range", career.average_salary)
                    st.metric("Job Outlook", career.job_outlook)
                
                # Skills
                st.write("**Required Skills:**")
                skills_text = " • ".join(career.required_skills)
                st.write(skills_text)
                
                # Related careers
                if career.related_careers:
                    st.write("**Related Careers:**")
                    st.write(", ".join(career.related_careers))


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main content based on current mode
    if st.session_state.current_mode is None:
        # Welcome screen
        st.markdown("""
        # Welcome to PathFinder! 
        ## Your AI career guidance assistant 
        
        Choose your preferred experience:
        
        - **🚀 Quick Mode**                            
        Get instant career recommendations from pre-defined scenarios that match your interests. Perfect for quick exploration!
        
        - **💬 Conversational Mode**   
        Have a personalized conversation with PathFinder to build your complete profile and receive tailored career guidance.
        
        **👉 Select a mode from the sidebar to begin!**
        
        ---

        ### Why Choose PathFinder?
        
        """)
        
        # Show some statistics or features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("**💼 Career Paths**", "25+", "Across multiple industries")
        
        with col2:
            st.metric("**⚡AI Powered**", "Groq LLM", "Ultra-fast responses")
        
        with col3:
            st.metric("**🎯 Match Accuracy**", "95%+", "Personalized recommendations")
    
    elif st.session_state.current_mode == "quick":
        display_quick_mode()
    
    elif st.session_state.current_mode == "conversational":
        display_conversational_mode()
        
    # Footer Section
    st.markdown("---")
    st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with ❤️ using Streamlit and <span class="groq-badge">⚡ Groq</span><br>
    <small>
        <a href="https://github.com/AryaInGit" target="_blank">GitHub</a> |
        <a href="mailto:arya.tech.ai@gmail.com">Contact</a> |
        <a href="https://github.com/AryaInGit/PathFinder/blob/main/PRIVACY.md" target="_blank">Privacy</a> |
        <a href="https://github.com/AryaInGit/PathFinder/blob/main/LICENSE.md" target="_blank">License</a>
    </small>
</div>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
