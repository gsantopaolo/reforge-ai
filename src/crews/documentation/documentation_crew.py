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
from tools.jdeps_tool        import JDepsTool
from crewai_tools            import SerperDevTool, DirectoryReadTool, FileReadTool
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

    def __init__(self, codebase_path: str, doc_path: str, kb_path: str):
        self.codebase_path = codebase_path
        self.doc_path      = doc_path
        self.kb_path       = kb_path

        # cache for tools
        always_cache       = lambda args, result: True

        # code dir and file tool
        self._code_dir_tool     = DirectoryReadTool(directory=self.codebase_path)
        self._code_dir_tool.cache_function = always_cache
        self._code_file_tool    = FileReadTool()
        self._code_file_tool.cache_function = always_cache

        # kb dir and file tool
        self._kb_dir_tool = DirectoryReadTool(directory=self.kb_path)
        # self._kb_dir_tool.cache_function = always_cache
        self._kb_file_tool = FileReadTool()
        # self._kb_file_tool.cache_function = always_cache



    # ────────── Agents ──────────

    @agent
    def project_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_manager_agent"],
            # tools=[SerperDevTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=True
        )

    @agent
    def codebase_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["codebase_analyst_agent"],
            tools=[ DependencyMapperTool(code_path=self.codebase_path),
                    self._code_dir_tool,
                    self._code_file_tool,
                    SerperDevTool(),
                    JDepsTool(base_path=self.codebase_path),
                    CodeParserTool(code_path=self.codebase_path),],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def documentation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["documentation_agent"],
            tools=[
                CodeParserTool(code_path=self.codebase_path),
                JDepsTool(base_path=self.codebase_path),
                self._code_dir_tool,
                self._code_file_tool,
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
            tools=[
                SerperDevTool(),
                self._code_dir_tool,
                self._code_file_tool
            ],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def migration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["migration_agent"],
            tools=[
                SerperDevTool(),
                self._kb_dir_tool,
                self._kb_file_tool,
            ],
            llm=llm_client,
            verbose=True,
            allow_delegation=True
        )

    # ────────── Tasks ──────────
    # (the task method names and keys MUST exactly match tasks.yaml)
    @task
    def extract_file_metadata(self) -> Task:
        return Task(config=self.tasks_config["extract_file_metadata"],
                    output_file="1-documentation/docs/1-Metadata.md")

    @task
    def generate_system_architecture(self) -> Task:
        return Task(config=self.tasks_config["generate_system_architecture"],
                    output_file="1-documentation/docs/2-SystemArchitecture.md")

    @task
    def generate_module_docs(self) -> Task:
        return Task(config=self.tasks_config["generate_module_docs"],
                    output_file="1-documentation/docs/3-ModuleDocumentation.md")

    @task
    def component_technology_inventory(self) -> Task:
        return Task(config=self.tasks_config["component_technology_inventory"],
                    output_file="1-documentation/docs/4-ComponentsInventory.md")

    @task
    def research_migration_best_practices(self) -> Task:
        return Task(config=self.tasks_config["research_migration_best_practices"],
                    output_file="1-documentation/docs/5-MigrationBestPractices.md")

    @task
    def impact_analysis_on_java21(self) -> Task:
        return Task(config=self.tasks_config["impact_analysis_on_java21"],
                    output_file="1-documentation/docs/6-ImpactAnalysis.md")

    @task
    def plan_phased_module_extraction(self) -> Task:
        return Task(config=self.tasks_config["plan_phased_module_extraction"],
                    output_file="1-documentation/docs/7-PlanPhasedModuleExtraction.md")

    @task
    def plan_migration_roadmap(self) -> Task:
        return Task(config=self.tasks_config["plan_migration_roadmap"],
                    output_file="1-documentation/docs/8-PlanMigrationRoadmap.md")

    @task
    def final_handover_and_summary(self) -> Task:
        return Task(config=self.tasks_config["final_handover_and_summary"],
                    output_file="1-documentation/docs/0-ExecutiveSummary.md")

    # ────────── Build Crew ──────────

    @crew
    def crew(self) -> Crew:
        manager = self.project_manager_agent()
        operational_agents = [a for a in self.agents if a is not manager]
        return Crew(
            agents=operational_agents,
            tasks=self.tasks,
            # process=Process.sequential,
            process=Process.hierarchical, #switched to hierarchical to enable the reviewer_agent
            manager_agent=manager,
            manager_llm=llm_client,
            planning=True,
            verbose=True
        )
