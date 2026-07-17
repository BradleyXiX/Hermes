import os
import yaml
# pyrefly: ignore [missing-import]
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

class HermesCrew:
    """Hermes agent crew for managing tasks and knowledge."""

    def __init__(self) -> None:
        self.agents_config = self._load_config("config/agents.yaml")
        self.tasks_config = self._load_config("config/tasks.yaml")

    def _load_config(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def crew(self) -> Crew:
        """Creates the Hermes crew"""
        # Placeholders for agents and tasks
        agents = []
        tasks = []

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=os.getenv("VERBOSE", "True").lower() == "true"
        )
