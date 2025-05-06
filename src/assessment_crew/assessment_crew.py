import os
from typing import Any
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew

from tools.jdeps_tool import JDepsTool
from tools.sonar_tool import SonarTool
from tools.db_parser_tool import DBParserTool

#
# Choose a provider via env LLM_PROVIDER (openai or anthropic)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

a =0
# Default model names per provider (override via MODEL_NAME if needed)
_default_models = {
    "openai": "gpt-4.1-mini",
    "anthropic": "anthropic/claude-3-sonnet-20240229-v1:0"
}
model_name = os.getenv("MODEL_NAME", _default_models.get(LLM_PROVIDER))

# Build the LLM client
api_key_env = f"{LLM_PROVIDER.upper()}_API_KEY"
llm_client = LLM(
    model=model_name,
    api_key=os.getenv(api_key_env)
)

# Instantiate shared tool objects
jdeps_tool = JDepsTool(java_home=os.getenv("JAVA_HOME"))
sonar_tool = SonarTool()
db_tool    = DBParserTool(java_helper_jar=os.getenv("JSQL_HELPER_JAR"))


@CrewBase
class AssessmentCrew:
    """Crew for Java Codebase Assessment (compatibility, analysis, DB, etc.)"""
    # tell PyCharm these exist
    agents_config: Any
    tasks_config: Any

    @agent
    def compatibility_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["compatibility_agent"],
            llm=llm_client,
            tools=[jdeps_tool],
            verbose=True
        )

    @agent
    def static_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["static_analysis_agent"],
            llm=llm_client,
            tools=[sonar_tool],
            verbose=True
        )

    @agent
    def db_detection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["db_detection_agent"],
            llm=llm_client,
            tools=[db_tool],
            verbose=True
        )

    @agent
    def ast_parsing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ast_parsing_agent"],
            llm=llm_client,
            tools=[],
            verbose=True
        )

    @agent
    def documentation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["documentation_agent"],
            llm=llm_client,
            tools=[],
            verbose=True
        )

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_agent"],
            llm=llm_client,
            tools=[],
            verbose=True
        )

    @agent
    def metrics_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["metrics_agent"],
            llm=llm_client,
            tools=[sonar_tool],
            verbose=True
        )

    @agent
    def prioritization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["prioritization_agent"],
            llm=llm_client,
            tools=[],
            verbose=True
        )

    @task
    def compatibility_task(self) -> Task:
        return Task(config=self.tasks_config["compatibility_task"])


    @task
    def static_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["static_analysis_task"])

    @task
    def db_usage_task(self) -> Task:
        return Task(config=self.tasks_config["db_usage_task"])

    @task
    def ast_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["ast_analysis_task"])

    @task
    def documentation_task(self) -> Task:
        return Task(
            config=self.tasks_config["documentation_task"],
            output_file="1-assessment/docs/AssessmentReport.md"
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary_task"],
            output_file="1-assessment/docs/ExecutiveSummary.md"
        )

    @task
    def metrics_task(self) -> Task:
        return Task(config=self.tasks_config["metrics_task"])

    @task
    def prioritization_task(self) -> Task:
        return Task(config=self.tasks_config["prioritization_task"])

    @crew
    def crew(self) -> Crew:
        """
        Assemble the crew with all agents and tasks in sequential order.
        Always starts with an empty state—runtime context must be passed into kickoff().
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            state={}  # No parameters here: state injection happens in kickoff()
        )
