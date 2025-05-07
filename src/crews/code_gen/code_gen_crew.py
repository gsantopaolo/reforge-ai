# src/refactoring_crew.py
#!/usr/bin/env python3

import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import Any

# Placeholder imports for custom tools
from tools.migration_scheduler_tool import MigrationSchedulerTool
from tools.openrewrite_tool import OpenRewriteTool
from tools.llm_coder_tool import LLMCoderTool
from tools.compiler_tool import CompilerTool
from tools.test_runner_tool import TestRunnerTool
from tools.llm_debugger_tool import LLMDebuggerTool
from tools.testgen_llm_tool import TestGenLLMTool
from tools.coverage_analyzer_tool import CoverageAnalyzerTool
from tools.static_analyzer_tool import StaticAnalyzerTool
from tools.security_scan_tool import SecurityScanTool
from tools.benchmark_tool import BenchmarkTool
from tools.diff_analyzer import DiffAnalyzerTool

# Choose provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
_default_models = {"openai": "gpt-4.1-mini", "anthropic": "anthropic/claude-3-sonnet-20240229-v1:0"}
model_name = os.getenv("MODEL_NAME", _default_models.get(LLM_PROVIDER))
api_key_env = f"{LLM_PROVIDER.upper()}_API_KEY"
llm_client = LLM(model=model_name, api_key=os.getenv(api_key_env))

@CrewBase
class CodeGenCrew:
    """
    RefactoringCrew: automates migration of Kitchensink Java code
    to Spring Boot 3.2 + Java 21 via specialized AI agents.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    agents: Any
    agents_config: Any
    tasks_config: Any
    tasks: Any

    def __init__(self, codebase_path: str, refactor_path: str, kb_path: str):
        self.codebase_path = codebase_path
        self.refactor_path = refactor_path
        self.kb_path = kb_path

    # ────────── Agents ──────────
    @agent
    def migration_scheduler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['migration_scheduler_agent'],
            tools=[MigrationSchedulerTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=True
        )

    @agent
    def migration_executor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['migration_executor_agent'],
            tools=[OpenRewriteTool(), LLMCoderTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def test_runner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['test_runner_agent'],
            tools=[CompilerTool(), TestRunnerTool(), TestGenLLMTool(), CoverageAnalyzerTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def debugger_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['debugger_agent'],
            tools=[LLMDebuggerTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def quality_assurance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_assurance_agent'],
            tools=[StaticAnalyzerTool(), SecurityScanTool(), BenchmarkTool(), DiffAnalyzerTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def documentation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_agent'],
            # tools=[DiagramGeneratorTool()],
            llm=llm_client,
            verbose=True,
            allow_delegation=False
        )

    # ────────── Tasks ──────────
    @task
    def select_module_to_migrate(self) -> Task:
        return Task(
            config=self.tasks_config['select_module_to_migrate'],
            output_file="2-refactoring/state/selected-module.json"
        )

    @task
    def generate_migration_diff(self) -> Task:
        return Task(
            config=self.tasks_config['generate_migration_diff'],
            output_file="2-refactoring/diffs/migration.patch"
        )

    @task
    def compile_and_run_tests(self) -> Task:
        return Task(
            config=self.tasks_config['compile_and_run_tests'],
            output_file="2-refactoring/state/test-report.json"
        )

    @task
    def analyze_and_debug_failures(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_and_debug_failures'],
            output_file="2-refactoring/diffs/debug.patch"
        )

    @task
    def generate_additional_tests(self) -> Task:
        return Task(
            config=self.tasks_config['generate_additional_tests'],
            output_file="2-refactoring/tests/new-tests.java"
        )

    @task
    def run_integration_smoke_tests(self) -> Task:
        return Task(
            config=self.tasks_config['run_integration_smoke_tests'],
            output_file="2-refactoring/state/smoke-test.json"
        )

    @task
    def security_and_performance_scan(self) -> Task:
        return Task(
            config=self.tasks_config['security_and_performance_scan'],
            output_file="2-refactoring/state/security-performance.json"
        )

    @task
    def code_review_and_approval(self) -> Task:
        return Task(
            config=self.tasks_config['code_review_and_approval'],
            output_file="2-refactoring/docs/code-review.md"
        )

    @task
    def finalize_migration_and_merge(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_migration_and_merge'],
            output_file="2-refactoring/state/final-merge.json"
        )

    @task
    def update_documentation_post_migration(self) -> Task:
        return Task(
            config=self.tasks_config['update_documentation_post_migration'],
            output_file="2-refactoring/docs/updated-docs.md"
        )

    # ────────── Build Crew ──────────
    @crew
    def crew(self) -> Crew:
        manager = self.migration_scheduler_agent()
        operational_agents = [a for a in self.agents if a is not manager]
        return Crew(
            agents=operational_agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True
        )
