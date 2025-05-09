# src/crews/code_gen/code_gen_crew.py
#!/usr/bin/env python3

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI # Or your preferred LLM provider
from typing import Any, Dict

# Import our defined tools
from tools.plan_tool import PlanTool
from tools.file_system_read_tool import FileSystemReadTool
from tools.code_search_tool import CodeSearchTool
from tools.open_rewrite_tool import OpenRewriteTool
from tools.file_system_read_write_tool import FileSystemReadWriteTool
from tools.legacy_compiler_tool import LegacyCompilerTool
from tools.spring_boot_compiler_tool import SpringBootCompilerTool

llm = ChatOpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

@CrewBase
class CodeGenCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    agents: Any
    tasks: Any

    def __init__(self,
                 plan_file_path: str,
                 codebase_path: str,
                 gen_docs_output_path: str,
                 kb_docs_path: str,
                 kb_code_path: str,
                 working_code_path: str):
        self.plan_file_path = plan_file_path
        self.codebase_path = codebase_path
        self.gen_docs_output_path = gen_docs_output_path
        self.kb_docs_path = kb_docs_path
        self.kb_code_path = kb_code_path
        self.working_code_path = working_code_path

    @agent
    def team_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['team_lead'],
            tools=[PlanTool(plan_file=self.plan_file_path)], # TeamLead now needs PlanTool for the validation task
            llm=llm,
            verbose=True
        )

    @agent
    def software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['software_architect'],
            tools=[
                PlanTool(plan_file=self.plan_file_path),
                FileSystemReadTool(),
                CodeSearchTool(
                    gen_docs_path=self.gen_docs_output_path,
                    kb_docs_path=self.kb_docs_path,
                    kb_code_path=self.kb_code_path
                )
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def principal_software_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['principal_software_engineer'],
            tools=[
                OpenRewriteTool(),
                FileSystemReadWriteTool(base_write_path=self.working_code_path)
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def build_and_test_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['build_and_test_agent'],
            tools=[
                LegacyCompilerTool(legacy_code_path=self.codebase_path),
                SpringBootCompilerTool(spring_code_path=self.working_code_path)
            ],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def create_modernization_step_brief_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_modernization_step_brief'],
            agent=self.software_architect(),
            # Input: {current_plan_step_identifier} will be in kickoff_inputs
            # Output: step_brief_output (string)
        )

    @task
    def implement_code_changes_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_code_changes'],
            agent=self.principal_software_engineer(),
            context=[self.create_modernization_step_brief_task()], # Depends on the brief
            # Input: {step_brief_output} from context
            # Output: code_changes_output (dict: {'diff': str, 'path': str})
        )

    @task
    def compile_modernized_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['compile_modernized_code'],
            agent=self.build_and_test_agent(),
            context=[self.implement_code_changes_task()], # Depends on code changes path
            # Input: {code_changes_output} (specifically the path) from context
            # Output: build_results_output (dict)
        )

    @task
    def request_human_validation_task(self) -> Task:
        # This task's description in tasks.yaml uses placeholders like
        # {step_brief_output}, {code_changes_output}, {build_results_output},
        # and {current_plan_step_identifier}. These must be filled from context
        # or kickoff_inputs when the task is executed.
        return Task(
            config=self.tasks_config['request_human_validation'],
            agent=self.team_lead(), # TeamLead executes this task
            human_input=True, # CrewAI will pause for input
            context=[ # Depends on outputs of all previous tasks
                self.create_modernization_step_brief_task(),
                self.implement_code_changes_task(),
                self.compile_modernized_code_task()
            ]
            # Output: user_decision_string (string)
        )

    @crew
    def build_crew_for_step(self) -> Crew:
        return Crew(
            agents=[ # TeamLead is now also a worker agent for its specific task
                self.team_lead(),
                self.software_architect(),
                self.principal_software_engineer(),
                self.build_and_test_agent()
            ],
            tasks=[
                self.create_modernization_step_brief_task(),
                self.implement_code_changes_task(),
                self.compile_modernized_code_task(),
                self.request_human_validation_task() # Human validation is the last step
            ],
            process=Process.hierarchical,
            manager_llm=self.team_lead().llm, # TeamLead's LLM still manages overall flow
            verbose=True
        )