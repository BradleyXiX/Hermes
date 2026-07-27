import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# 1. Load Secrets
load_dotenv()

# 2. Configure the free-tier Gemini LLM
# We use gemini-2.0-flash for high-speed, cost-effective inference
gemini_llm = LLM(model="gemini/gemini-flash-lite-latest")

# 3. Define the Triage Agent
triage_agent = Agent(
    role='Principal Inbox Triage Specialist',
    goal='Analyze incoming emails and strictly categorize them into URGENT or FYI.',
    backstory='''You are an elite, highly efficient AI executive assistant. 
    Your primary directive is to protect your principal's time. You quickly 
    identify actionable items, deadlines, and critical communications, ruthlessly 
    separating them from newsletters, generic announcements, and system alerts.''',
    llm=gemini_llm,
    verbose=True
)

# 4. Define the Categorization Task
triage_task = Task(
    description='''Analyze the following raw email data: 
    
    {email_data}
    
    Categorize each email into one of two buckets based on these strict rules:
    
    1. URGENT: The email requires a response, contains an upcoming USIU academic deadline, involves grades, or is a direct message from a VIP contact (e.g., Marie, your girlfriend, or specific professors). 
    2. FYI: The email is a newsletter, a general university-wide announcement, a promotional offer, or a system alert that requires no action.
    
    Format the final output specifically for a Telegram message. Use standard emojis (like 🚨 for Urgent and ℹ️ for FYI). Bold the Sender's name and provide a 1-2 sentence summary of the email's core point. Do not include raw headers or clutter.''',
    expected_output='A cleanly formatted Telegram message grouping emails strictly under 🚨 URGENT and ℹ️ FYI headers.',
    agent=triage_agent
)

def execute_triage(email_text):
    """Bridge function to trigger the agent from the Telegram bot."""
    
    # Assemble the crew
    hermes_crew = Crew(
        agents=[triage_agent],
        tasks=[triage_task],
        max_rpm=5
    )
    
    # Inject the dynamic Telegram payload into the agent
    result = hermes_crew.kickoff(inputs={'email_data': email_text})
    
    # Return the raw string output back to Telegram
    return str(result)