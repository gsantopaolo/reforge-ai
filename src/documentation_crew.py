#!/usr/bin/env python3
# src/documentation_crew.py

import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from numpy.distutils.lib2def import output_def
from onnxruntime.transformers.benchmark_helper import output_fusion_statistics
from openpyxl.styles.builtins import output

from tools.code_parser       import CodeParserTool
from tools.dependency_mapper import DependencyMapperTool
from crewai_tools            import SerperDevTool
from typing import Any

# Choose a provider via env LLM_PROVIDER (openai or anthropic)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

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

@CrewBase
class DocumentationCrew:
    """
    DocumentationCrew: auto-generates comprehensive docs
    for a legacy Java 10 banking system moving to Java 21.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    agents: Any
    agents_config: Any
    tasks_config: Any
    tasks: Any

    def __init__(self, codebase_path: str, doc_path: str):
        self.codebase_path = codebase_path
        self.doc_path      = doc_path

    # ────────── Agents ──────────

    @agent
    def project_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_manager_agent"],
            tools=[],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def codebase_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["codebase_analyst_agent"],
            tools=[ DependencyMapperTool(code_path=self.codebase_path) ],
            llm=None,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def documentation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["documentation_agent"],
            tools=[
                CodeParserTool(code_path=self.codebase_path),
                SerperDevTool()
            ],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def domain_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["domain_expert_agent"],
            tools=[],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def reviewer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["reviewer_agent"],
            tools=[],            # purely critique
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    # ────────── Tasks ──────────
    # (the task method names and keys MUST exactly match tasks.yaml)

    @task
    def initialize_project_kb(self) -> Task:
        return Task(config=self.tasks_config["initialize_project_kb"],
                    output_file="1-documentation/docs/ProjectKnowledgeBase.md"
        )

    @task
    def inventory_codebase(self) -> Task:
        return Task(config=self.tasks_config["inventory_codebase"],
                    output_file="1-documentation/docs/CodebaseInventory.md")

    @task
    def analyze_legacy_code(self) -> Task:
        return Task(config=self.tasks_config["analyze_legacy_code"],
                    output_file="1-documentation/docs/LegacyCodeAnalysis.md")

    @task
    def generate_module_docs(self) -> Task:
        return Task(config=self.tasks_config["generate_module_docs"],
                    output_file="1-documentation/docs/ModuleDocumentation.md")

    @task
    def plan_migration_roadmap(self) -> Task:
        return Task(config=self.tasks_config["plan_migration_roadmap"],
                    output_file="1-documentation/docs/MigrationRoadmap.md")


    @task
    def final_handover_and_summary(self) -> Task:
        return Task(config=self.tasks_config["final_handover_and_summary"],
                    output_file="1-documentation/docs/FinalHandoverAndSummary.md")

    # ────────── Build Crew ──────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
