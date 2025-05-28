#!/usr/bin/env python3
# src/documentation_crew.py

import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from numpy.distutils.lib2def import output_def
from onnxruntime.transformers.benchmark_helper import output_fusion_statistics
from openpyxl.styles.builtins import output

from tools.code_parser       import CodeParserTool
from tools.dependency_mapper import DependencyMapperTool
from tools.maven_build_tool  import MavenBuildTool
from crewai_tools            import SerperDevTool, DirectoryReadTool, FileReadTool, FileWriterTool
from typing import Any

from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from langchain_community.tools import ShellTool

from tools.langchain_fs_tool import LangChainFSWrapper
from tools.langchain_shell_tool import LangChainShellWrapper

# Choose a provider via env LLM_PROVIDER (openai or anthropic)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# Default model names per provider (override via MODEL_NAME if needed)
# must change .ENV AS WELL!!!
_default_models = {
    # "openai": "gpt-4.1-mini",
    "openai": "gpt-4.1-2025-04-14",
    # "openai": "o3-2025-04-16",
    "anthropic": "anthropic/claude-3-7-sonnet-20250219",
    # "anthropic": "claude-3-5-sonnet-latest",
    "gemini": "gemini/gemini-2.5-pro-exp-03-25"
}
model_name = os.getenv("MODEL_NAME", _default_models.get(LLM_PROVIDER))

# Build the LLM client
api_key_env = f"{LLM_PROVIDER.upper()}_API_KEY"
llm_client = LLM(
    model=model_name,
    api_key=os.getenv(api_key_env)
)

@CrewBase
class GenModernCrew:
    """
    DocumentationCrew: auto-generates comprehensive docs
    for a legacy Java 10 banking system moving to Java 21.
    """
    agents_config = 'config/docs_agents.yaml'
    tasks_config = 'config/docs_tasks.yaml'
    agents: Any
    agents_config: Any
    tasks_config: Any
    tasks: Any

    def __init__(self, codebase_path: str, kb_path: str):
        self.codebase_path = codebase_path
        self.kb_path       = kb_path

        # cache for tools
        always_cache       = lambda args, result: True


        # kb dir and file tool
        self._kb_dir_tool = DirectoryReadTool(directory=self.kb_path)
        # self._kb_dir_tool.cache_function = always_cache
        self._kb_file_tool = FileReadTool()
        # self._kb_file_tool.cache_function = always_cache

        self.llm = llm_client

        # setup file-management toolkit
        toolkit = FileManagementToolkit(
            # todo: hardcoded path
            root_dir=str("/Users/gp/Developer/java-samples/reforge-ai/src/1-codegen-work/"),
            selected_tools=["copy_file", "file_delete"]
        )
        lc_tools = toolkit.get_tools()
        self.fs_tools = [
            LangChainFSWrapper(name=t.name, description=t.description, lc_tool=t)
            for t in lc_tools
        ]

    # ────────── Agents ──────────
    @agent
    def team_lead(self) -> Agent:
        cfg = self.agents_config['team_lead']
        return Agent(
            config=cfg,
            llm=self.llm,
            verbose=cfg.get('verbose', True),
            allow_delegation=cfg.get('allow_delegation', True),
            max_iter=cfg.get('max_iter', 25)
        )

    @agent
    def software_architect(self) -> Agent:
        cfg = self.agents_config['software_architect']
        tools = [
            # DirectoryReadTool(str(self.temp_base)),
            self._kb_dir_tool,
            self._kb_file_tool,
            # FileWriterTool(),
            # MDXSearchTool(),
            # SerperDevTool(),
            # WebsiteSearchTool(),
            # *self.fs_tools
        ]
        return Agent(
            config=cfg,
            tools=tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=cfg.get('max_iter', 25)
        )

    # ────────── Tasks ──────────
    @task
    def create_modernization_step_brief_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_modernization_step_brief'],
            agent=self.software_architect()
        )



    # ────────── Crew ──────────
    @crew
    def crew(self) -> Crew:
        manager = self.team_lead()
        operational_agents = [a for a in self.agents if a is not manager]
        return Crew(
            agents=operational_agents,
            tasks=self.tasks,
            # process=Process.sequential,
            process=Process.hierarchical, #switched to hierarchical to enable the reviewer_agent
            manager_agent=manager,
            manager_llm=llm_client,
            planning=True,
            verbose=True,
            memory = True,
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(db_path="./modernization_memory.db")
        ),
        )


