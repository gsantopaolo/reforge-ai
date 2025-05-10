# src/crews/code_gen/code_gen_crew.py
# !/usr/bin/env python3

import os
import logging
from crewai         import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools   import SerperDevTool, DirectoryReadTool, FileReadTool, FileWriterTool, MDXSearchTool, WebsiteSearchTool
from typing         import Any, Dict, Optional
from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit




# Import our defined tools
# from tools.plan_tool import PlanTool
# from tools.file_system_read_tool import FileSystemReadTool
# from tools.code_search_tool import CodeSearchTool
# from tools.open_rewrite_tool import OpenRewriteTool
# from tools.file_system_read_write_tool import FileSystemReadWriteTool
# from tools.legacy_compiler_tool import LegacyCompilerTool
# from tools.spring_boot_compiler_tool import SpringBootCompilerTool
from tools.compiler_tool import CompilerTool

crew_logger = logging.getLogger(__name__)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
_default_models = {"openai": "gpt-4-turbo-preview", "anthropic": "claude-3-sonnet-20240229",
                   "gemini": "gemini-1.5-pro-latest"}
model_name_from_env = os.getenv("MODEL_NAME")
default_model_for_provider = _default_models.get(LLM_PROVIDER)
final_model_name: Optional[str] = None
if model_name_from_env:
    final_model_name = model_name_from_env
elif default_model_for_provider:
    final_model_name = default_model_for_provider
else:
    crew_logger.warning(f"No default model for provider '{LLM_PROVIDER}' & MODEL_NAME not set. Using OpenAI fallback.")
    if LLM_PROVIDER == "openai":
        final_model_name = "gpt-4-turbo-preview"
    else:
        crew_logger.error(f"Cannot determine model for provider '{LLM_PROVIDER}'."); final_model_name = None

llm_client_instance = None

if final_model_name:
    model_string_for_crewai = final_model_name
    if LLM_PROVIDER == "anthropic" and not final_model_name.startswith("anthropic/"):
        model_string_for_crewai = f"anthropic/{final_model_name}"
    elif LLM_PROVIDER == "gemini" and not final_model_name.startswith("gemini/"):
        model_string_for_crewai = f"gemini/{final_model_name}"
    api_key_env_var_name = f"{LLM_PROVIDER.upper()}_API_KEY";
    api_key = os.getenv(api_key_env_var_name)
    llm_params = {"model": model_string_for_crewai}
    if api_key and LLM_PROVIDER not in ["gemini"]: llm_params['api_key'] = api_key
    try:
        llm_client_instance = LLM(**llm_params)
        crew_logger.info(f"LLM Client initialized: Provider='{LLM_PROVIDER}', Model='{model_string_for_crewai}'.")
    except Exception as e:
        crew_logger.critical(f"CRITICAL: Failed to initialize LLM client: {e}.")
        llm_client_instance = None
else:
    crew_logger.critical("CRITICAL: Could not determine model name for LLM initialization.")


@CrewBase
class CodeGenCrew:
    # These tell CrewBase where to load the config from.
    # Paths are relative to this file (src/crews/code_gen/code_gen_crew.py)
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    agents: Any
    agents_config: Any
    tasks_config: Any
    tasks: Any

    # These attributes will be populated by CrewBase after it loads the YAML files.
    # The @agent and @task decorators will then use these loaded configs.
    # No need for agents_config: Any, tasks_config: Any at class level if CrewBase handles it.
    # agents: Any (CrewBase adds this if agents are defined)
    # tasks: Any (CrewBase adds this if tasks are defined)

    def __init__(self,
                 plan_file_path: str,
                 codebase_path: str,
                 gen_docs_output_path: str,
                 kb_docs_path: str,
                 kb_code_path: str,
                 working_code_path: str):
        if llm_client_instance is None:
            raise RuntimeError("LLM client not initialized in CodeGenCrew module.")
        self.llm = llm_client_instance

        # Store paths for tool instantiation
        self.plan_file_path = plan_file_path
        self.codebase_path = codebase_path
        self.gen_docs_output_path = gen_docs_output_path
        self.kb_docs_path = kb_docs_path
        self.kb_code_path = kb_code_path
        self.working_code_path = working_code_path

        toolkit = FileManagementToolkit(
            root_dir="./workspace",  # all ops confined here
            selected_tools=["copy_file", "delete_file"]  # only include copy & delete (optional)

        )
        lc_tools = toolkit.get_tools()

        self.lc_tools = lc_tools

        # # cache for tools
        # always_cache = lambda args, result: True
        #
        # # code dir and file tool
        # self._code_dir_tool = DirectoryReadTool("/Users/gp/Developer/java-samples/reforge-ai/src/1-documentation/")
        # self._code_dir_tool.cache_function = always_cache
        # self._code_file_tool = FileReadTool()
        # self._code_file_tool.cache_function = always_cache

        # web search tool
        # self._serper_tool = SerperDevTool()

    @agent
    def team_lead(self) -> Agent:
        # self.agents_config is populated by CrewBase from agents_config = 'config/agents.yaml'
        agent_config = self.agents_config['team_lead']
        return Agent(
            config=agent_config,
            llm=self.llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', True))

    @agent
    def software_architect(self) -> Agent:
        agent_config = self.agents_config['software_architect']
        return Agent(
            config=agent_config,
            tools=[
                # PlanTool(plan_file=self.plan_file_path),

                DirectoryReadTool("/Users/gp/Developer/java-samples/reforge-ai/temp/"),
                FileReadTool(),
                FileWriterTool(),
                MDXSearchTool(),
                SerperDevTool(),
                WebsiteSearchTool(),
                self.lc_tools,
                # self._code_dir_tool,
                # self._code_file_tool,
                # self._serper_tool
            ],
            llm=self.llm,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', True))

    @agent
    def principal_software_engineer(self) -> Agent:
        agent_config = self.agents_config['principal_software_engineer']
        return Agent(config=agent_config,
                     tools=[
                         # FileSystemReadTool(),
                         DirectoryReadTool("/Users/gp/Developer/java-samples/reforge-ai/temp/"),
                         FileReadTool(),
                         FileWriterTool(),
                         SerperDevTool(),
                         MDXSearchTool(),
                         WebsiteSearchTool(),
                         self.lc_tools,
                         # OpenRewriteTool(),
                         # FileSystemReadWriteTool(base_write_path=self.working_code_path),
                         # self._code_dir_tool,
                         # self._code_file_tool,
                         # self._serper_tool
                     ],
                     llm=self.llm,
                     verbose=agent_config.get('verbose', True),
                     allow_delegation=agent_config.get('allow_delegation', True))

    @agent
    def build_and_test_agent(self) -> Agent:
        agent_config = self.agents_config['build_and_test_agent']
        return Agent(config=agent_config,
                     tools=[
                         CompilerTool(self.codebase_path),
                     ],
                     # llm=self.llm,
                     verbose=agent_config.get('verbose', True),
                     allow_delegation=agent_config.get('allow_delegation', False))

    @task
    def create_modernization_step_brief_task(self) -> Task:
        # self.tasks_config is populated by CrewBase from tasks_config = 'config/tasks.yaml'
        return Task(config=self.tasks_config['create_modernization_step_brief'], agent=self.software_architect())

    @task
    def implement_code_changes_task(self) -> Task:
        return Task(config=self.tasks_config['implement_code_changes'], agent=self.principal_software_engineer(),
                    context=[self.create_modernization_step_brief_task()])

    @crew
    def app_modernization_crew(self) -> Crew:
        manager = self.team_lead()
        worker_agents = [
            self.software_architect(),
            self.principal_software_engineer(),
            self.build_and_test_agent()
        ]
        # self.tasks is a property populated by @CrewBase from @task methods
        return Crew(
            agents=worker_agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True
        )