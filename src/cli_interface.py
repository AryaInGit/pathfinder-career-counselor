import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from src.conversation_manager import ConversationManager
from src.models import StudentProfile
from src.career_database import CareerDatabase
from src.career_matcher import CareerMatcher
from src.llm_client import LLMClient

class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.conversation_manager = ConversationManager()
        self.career_db = CareerDatabase()
        self.llm_client = LLMClient()
        self.career_matcher = CareerMatcher(self.career_db, self.llm_client)
        
    def run(self):
        """Run the CLI interface with mode selection"""
        self._display_welcome()
        
        # Mode selection
        mode = self._select_mode()
        
        if mode == "quick":
            self._run_quick_mode()
        else:
            self._run_conversational_mode()
    
    def _display_welcome(self):
        """Display welcome screen"""
        welcome_text = Text()
        welcome_text.append("🎓 Student Career Pathway Recommender\n", style="bold blue")
        welcome_text.append("Discover your ideal career path through AI-powered recommendations\n", style="dim")
        welcome_text.append("⚡ Powered by Groq for ultra-fast responses", style="bold green")
        
        welcome_panel = Panel(
            Align.center(welcome_text),
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)
        self.console.print()
    
    def _select_mode(self):
        """Let user select between quick and conversational mode"""
        self.console.print("[bold cyan]Choose Your Experience:[/bold cyan]")
        self.console.print()
        
        # Create mode options table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="bold")
        table.add_column("Description")
        
        table.add_row(
            "1. 🚀 Quick Mode", 
            "[green]Get instant career recommendations from sample scenarios[/green]"
        )
        table.add_row(
            "2. 💬 Conversational Mode", 
            "[blue]Full career counseling experience with personalized guidance[/blue]"
        )
        
        self.console.print(table)
        self.console.print()
        
        while True:
            choice = Prompt.ask(
                "[bold]Select mode",
                choices=["1", "2", "quick", "conversational", "q", "c"],
                default="1"
            )
            
            if choice in ["1", "quick", "q"]:
                return "quick"
            elif choice in ["2", "conversational", "c"]:
                return "conversational"
    
    def _run_quick_mode(self):
        """Run quick recommendation mode"""
        self.console.print(Panel(
            "[bold green]🚀 Quick Recommendation Mode[/bold green]\n"
            "[dim]Select a scenario that matches your interests for instant career recommendations[/dim]",
            border_style="green"
        ))
        
        while True:
            scenario = self._select_scenario()
            
            if scenario == "quit":
                break
            
            # Generate quick recommendations
            self._generate_quick_recommendations(scenario)
            
            # Ask if they want to try another scenario or switch modes
            if not self._continue_quick_mode():
                break
    
    def _select_scenario(self):
        """Display sample scenarios for quick mode"""
        scenarios = {
            "1": {
                "title": "🖥️ Technology Enthusiast",
                "description": "I love coding, AI, and building software solutions",
                "profile": {
                    "interests": ["programming", "artificial intelligence", "software development", "problem-solving"],
                    "hobbies": ["coding projects", "tech blogs", "hackathons"],
                    "preferred_subjects": ["computer science", "mathematics", "physics"],
                    "career_goals": "Build innovative technology solutions that solve real-world problems"
                }
            },
            "2": {
                "title": "🎨 Creative Designer",
                "description": "I enjoy art, design, and visual creativity",
                "profile": {
                    "interests": ["graphic design", "user experience", "visual arts", "creativity"],
                    "hobbies": ["drawing", "photography", "digital art"],
                    "preferred_subjects": ["art", "design", "english"],
                    "career_goals": "Create beautiful and functional designs that inspire people"
                }
            },
            "3": {
                "title": "🔬 Science Explorer",
                "description": "I'm fascinated by research, data, and scientific discovery",
                "profile": {
                    "interests": ["data science", "research", "analytics", "scientific discovery"],
                    "hobbies": ["reading research papers", "data visualization", "experiments"],
                    "preferred_subjects": ["mathematics", "statistics", "biology", "chemistry"],
                    "career_goals": "Use data and research to make important discoveries"
                }
            },
            "4": {
                "title": "💼 Business Leader",
                "description": "I'm interested in entrepreneurship, strategy, and leadership",
                "profile": {
                    "interests": ["business strategy", "entrepreneurship", "leadership", "innovation"],
                    "hobbies": ["reading business books", "networking", "startup events"],
                    "preferred_subjects": ["economics", "business studies", "mathematics"],
                    "career_goals": "Lead teams and build successful businesses"
                }
            },
            "5": {
                "title": "🏥 Healthcare Helper",
                "description": "I want to help people and work in healthcare",
                "profile": {
                    "interests": ["helping people", "medicine", "health", "patient care"],
                    "hobbies": ["volunteering", "health research", "fitness"],
                    "preferred_subjects": ["biology", "chemistry", "psychology"],
                    "career_goals": "Make a positive impact on people's health and wellbeing"
                }
            },
            "6": {
                "title": "🎓 Education Advocate",
                "description": "I love teaching, mentoring, and sharing knowledge",
                "profile": {
                    "interests": ["teaching", "education", "mentoring", "knowledge sharing"],
                    "hobbies": ["tutoring", "reading", "educational content creation"],
                    "preferred_subjects": ["english", "history", "mathematics"],
                    "career_goals": "Inspire and educate the next generation"
                }
            }
        }
        
        self.console.print("\n[bold cyan]📋 Sample Scenarios:[/bold cyan]")
        
        # Display scenarios in a nice table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Option", style="bold", width=3)
        table.add_column("Scenario", style="bold", width=25)
        table.add_column("Description", width=50)
        
        for key, scenario in scenarios.items():
            table.add_row(
                f"{key}.",
                scenario["title"],
                f"[dim]{scenario['description']}[/dim]"
            )
        
        table.add_row("7.", "[red]🚪 Back to Main Menu[/red]", "[dim]Return to mode selection[/dim]")
        table.add_row("q.", "[red]❌ Quit[/red]", "[dim]Exit the application[/dim]")
        
        self.console.print(table)
        self.console.print()
        
        while True:
            choice = Prompt.ask(
                "[bold]Select a scenario",
                choices=["1", "2", "3", "4", "5", "6", "7", "q", "quit", "back"],
                default="1"
            )
            
            if choice in ["q", "quit"]:
                return "quit"
            elif choice in ["7", "back"]:
                # Restart the application
                self.run()
                return "quit"
            elif choice in scenarios:
                return scenarios[choice]
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")
    
    def _generate_quick_recommendations(self, scenario):
        """Generate quick career recommendations for selected scenario"""
        self.console.print(f"\n[bold blue]🎯 Analyzing: {scenario['title']}[/bold blue]")
        
        # Create student profile from scenario
        profile = StudentProfile(
            name="Student",
            interests=scenario["profile"]["interests"],
            hobbies=scenario["profile"]["hobbies"],
            preferred_subjects=scenario["profile"]["preferred_subjects"],
            career_goals=scenario["profile"]["career_goals"]
        )
        
        with self.console.status("[bold green]⚡ Generating recommendations with Groq..."):
            try:
                # Get career recommendations
                recommendations = self.career_matcher.find_matching_careers(profile)
                
                if not recommendations:
                    self.console.print("[red]No recommendations found. Please try a different scenario.[/red]")
                    return
                
                # Display top 3 recommendations
                self._display_quick_recommendations(recommendations[:3], scenario["title"])
                
            except Exception as e:
                self.console.print(f"[red]Error generating recommendations: {str(e)}[/red]")
    
    def _display_quick_recommendations(self, recommendations, scenario_title):
        """Display career recommendations in a beautiful format"""
        self.console.print(f"\n[bold green]✨ Top Career Matches for {scenario_title}:[/bold green]")
        
        for i, career in enumerate(recommendations, 1):
            # Create career card
            career_info = Text()
            career_info.append(f"{i}. {career.title}\n", style="bold blue")
            career_info.append(f"Match Score: {career.match_score:.0%}\n", style="bold green")
            career_info.append(f"{career.description}\n\n", style="dim")
            
            career_info.append("💰 Salary: ", style="bold")
            career_info.append(f"{career.average_salary}\n", style="green")
            
            career_info.append("📈 Job Outlook: ", style="bold")
            career_info.append(f"{career.job_outlook}\n", style="green")
            
            career_info.append("🎓 Education: ", style="bold")
            career_info.append(f"{career.education_requirements}\n", style="cyan")
            
            if career.explanation:
                career_info.append("\n💡 Why this matches: ", style="bold yellow")
                career_info.append(f"{career.explanation}", style="yellow")
            
            # Display in a panel
            panel = Panel(
                career_info,
                border_style="blue",
                padding=(1, 2)
            )
            
            self.console.print(panel)
        
        # Show skills and related careers for the top match
        if recommendations:
            top_career = recommendations[0]
            self._display_career_details(top_career)
    
    def _display_career_details(self, career):
        """Display detailed information about a career"""
        # Skills table
        skills_table = Table(title=f"🛠️ Required Skills for {career.title}", show_header=False)
        skills_table.add_column("Skills", style="cyan")
        
        # Add skills in rows of 2
        skills = career.required_skills
        for i in range(0, len(skills), 2):
            if i + 1 < len(skills):
                skills_table.add_row(f"• {skills[i]}", f"• {skills[i+1]}")
            else:
                skills_table.add_row(f"• {skills[i]}", "")
        
        self.console.print(skills_table)
        
        # Related careers
        if career.related_careers:
            related_text = Text()
            related_text.append("🔗 Related Careers: ", style="bold magenta")
            related_text.append(", ".join(career.related_careers), style="magenta")
            
            self.console.print(Panel(related_text, border_style="magenta"))
    
    def _continue_quick_mode(self):
        """Ask if user wants to continue with quick mode"""
        self.console.print()
        
        table = Table(show_header=False, box=None)
        table.add_column("Option", style="bold")
        table.add_column("Description")
        
        table.add_row("1. 🔄 Try Another Scenario", "Explore different career paths")
        table.add_row("2. 💬 Switch to Conversational Mode", "Get personalized career counseling")
        table.add_row("3. ❌ Exit", "End the session")
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "[bold]What would you like to do next?",
            choices=["1", "2", "3", "scenario", "conversational", "exit"],
            default="1"
        )
        
        if choice in ["1", "scenario"]:
            return True
        elif choice in ["2", "conversational"]:
            self._run_conversational_mode()
            return False
        else:
            return False
    
    def _run_conversational_mode(self):
        """Run conversational career counseling mode"""
        self.console.print(Panel(
            "[bold blue]💬 AI Career Counseling Mode[/bold blue]\n"
            "[dim]Have a personalized conversation with PathFinder to discover your ideal career path[/dim]",
            border_style="blue"
        ))
        
        # Start conversation
        try:
            greeting = self.conversation_manager.start_conversation()
            self._display_message("PathFinder", greeting)
            
            while True:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.console.print("[yellow]Thanks for using PathFinder! Good luck with your career journey! 🎓[/yellow]")
                    break
                
                # Process input and get response
                with self.console.status("[bold green]PathFinder is thinking..."):
                    response = self.conversation_manager.process_user_input(user_input)
                
                self._display_message("PathFinder", response)
                
                # Check if we have recommendations to display
                if self.conversation_manager.state.career_recommendations:
                    self._display_conversational_recommendations()
                    
                    # Ask if they want to continue the conversation
                    if not Confirm.ask("\n[bold]Would you like to continue the conversation?[/bold]"):
                        break
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Session ended. Thanks for using PathFinder![/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]An error occurred: {str(e)}[/red]")
    
    def _display_message(self, speaker, message):
        """Display a message with proper formatting"""
        if speaker == "PathFinder":
            style = "blue"
            icon = "🤖"
        else:
            style = "cyan"
            icon = "👤"
        
        formatted_message = Text()
        formatted_message.append(f"{icon} {speaker}: ", style=f"bold {style}")
        formatted_message.append(message)
        
        panel = Panel(
            formatted_message,
            border_style=style,
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def _display_conversational_recommendations(self):
        """Display career recommendations from conversational mode"""
        recommendations = self.conversation_manager.state.career_recommendations
        
        if not recommendations:
            return
        
        self.console.print("\n[bold green]🎯 Your Personalized Career Recommendations:[/bold green]")
        
        # Display top 5 recommendations
        for i, career in enumerate(recommendations[:5], 1):
            self.console.print(f"\n[bold blue]{i}. {career.title}[/bold blue] - [bold green]{career.match_score:.0%} Match[/bold green]")
            
            # Create details table
            details_table = Table(show_header=False, box=None, padding=(0, 1))
            details_table.add_column("Field", style="bold", width=20)
            details_table.add_column("Details", width=60)
            
            details_table.add_row("💼 Description", career.description)
            details_table.add_row("💰 Salary Range", career.average_salary)
            details_table.add_row("📈 Job Outlook", career.job_outlook)
            details_table.add_row("🎓 Education", career.education_requirements)
            
            if career.explanation:
                details_table.add_row("💡 Why it matches", career.explanation)
            
            details_table.add_row("🛠️ Key Skills", ", ".join(career.required_skills[:4]) + ("..." if len(career.required_skills) > 4 else ""))
            
            if career.related_careers:
                details_table.add_row("🔗 Related Careers", ", ".join(career.related_careers[:3]) + ("..." if len(career.related_careers) > 3 else ""))
            
            self.console.print(details_table)
        
        self.console.print()


if __name__ == "__main__":
    cli = CLIInterface()
    cli.run()
