import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# 1. Load Secrets
load_dotenv()

# 2. Configure the free-tier Gemini LLM
# We use gemini-2.0-flash for high-speed, cost-effective inference
gemini_llm = LLM(model="gemini/gemini-2.0-flash")

# 3. Define the Single-Responsibility Agent
inbox_router = Agent(
    role="Senior Inbox Triage Specialist",
    goal="Analyze incoming emails and accurately categorize their urgency as High, Medium, or Low.",
    backstory="You are a highly efficient assistant managing a software engineer's busy inbox. You understand technical jargon and prioritize urgent system alerts or direct recruiter outreach.",
    llm=gemini_llm,
    verbose=True
)

# 4. Define the specific Task for the Agent
triage_task = Task(
    description="Analyze this email: '{email_content}'. Categorize its urgency (High, Medium, Low) and provide a one-sentence justification.",
    expected_output="A single word indicating urgency (High, Medium, Low), followed by a one-sentence justification.",
    agent=inbox_router
)

# 5. Assemble the Crew (Even if it's just one agent for now)
hermes_crew = Crew(
    agents=[inbox_router],
    tasks=[triage_task]
)

# --- Test Execution Block ---
if __name__ == "__main__":
    # Mock data to test our logic before hitting live APIs
    mock_email = "URGENT: AWS Lambda deployment failed in production. Error 502 Bad Gateway."
    
    print("Initializing Hermes Triage Test...")
    result = hermes_crew.kickoff(inputs={'email_content': mock_email})
    print("\n=== Agent Output ===")
    print(result)