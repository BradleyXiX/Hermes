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
    
    Categorize and summarize the emails based on these strict rules to prevent alert fatigue:
    
    1. 🚨 URGENT: Requires immediate action, contains an upcoming USIU academic deadline, involves grades, or is a direct message from a VIP contact (e.g., Marie, your girlfriend, or professors). 
       - For these, provide a hyper-concise 1-sentence summary.
       - Bold the sender's name.
       
    2. ℹ️ FYI: Newsletters, general announcements, promotional offers, or system alerts. 
       - DO NOT list these individually. 
       - Compress all FYI emails into a single aggregate sentence at the very end of the message (e.g., "You also have 14 FYI emails consisting mostly of security advisories and promotional offers.").
    
    Format the output specifically for a Telegram message. Prioritize extreme brevity. Do not include raw headers, introductory text, or unnecessary pleasantries.''',
    
    expected_output='A hyper-concise Telegram message focusing almost entirely on 🚨 URGENT items, with only a single aggregate sentence for FYI items at the bottom.',
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