# tools/maven_compiler_tool_hardcoded_path.py
import os
import subprocess
from pathlib import Path
from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import logging

logger = logging.getLogger(__name__)

# Define the hardcoded path here
# Ensure this is the correct root directory of the Maven project you want to compile
# This should be the path to the directory containing the pom.xml
HARDCODED_PROJECT_PATH = "/Users/gp/Developer/java-samples/reforge-ai/temp/1-codegen-work/kitchensink"


# OR, if you want to compile the original legacy one directly sometimes for comparison:
# HARDCODED_PROJECT_PATH = "/Users/gp/Developer/java-samples/reforge-ai/assessment_crew/temp_codebase/kitchensink"

class HardcodedMavenCompilerToolInput(BaseModel):
    """Input for the HardcodedMavenCompilerTool."""
    goals: Optional[List[str]] = Field(default_factory=lambda: ["clean", "compile"],
                                       description="List of Maven goals to execute (e.g., ['clean', 'compile'], ['package']).")
    # Optional: extra_args: Optional[List[str]] = Field(None, description="Extra arguments to pass to the mvn command.")


class CompilerTool(BaseTool):
    name: str = "CompilerTool"  # Give it a distinct name
    description: str = (
        f"Compiles a specific Java project located at '{HARDCODED_PROJECT_PATH}' using Apache Maven. "
        "You can specify Maven goals; defaults to 'clean compile'."
    )
    args_schema: Type[BaseModel] = HardcodedMavenCompilerToolInput

    _mvn_cmd: str  # To store the mvn command path

    def __init__(self, mvn_executable: Optional[str] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._mvn_cmd = mvn_executable if mvn_executable else "mvn"

        # Validate the hardcoded path at initialization
        self._project_path_internal = Path(HARDCODED_PROJECT_PATH).resolve()
        if not self._project_path_internal.is_dir():
            logger.error(
                f"{self.name}: Hardcoded project path '{self._project_path_internal}' not found or not a directory.")
            raise ValueError(f"Hardcoded project path '{self._project_path_internal}' is invalid for {self.name}.")

        pom_file = self._project_path_internal / "pom.xml"
        if not pom_file.is_file():
            logger.error(f"{self.name}: pom.xml not found in hardcoded project path '{self._project_path_internal}'.")
            raise ValueError(f"pom.xml not found in hardcoded project path for {self.name}.")

    def _run(self, goals: Optional[List[str]] = None) -> str:  # project_path is no longer an argument
        effective_goals = goals if goals else ["clean", "compile"]  # Default goals

        command: List[str] = [self._mvn_cmd, "-f", str(self._project_path_internal / "pom.xml")] + effective_goals

        logger.info(f"Executing Maven command: {' '.join(command)} in directory: {self._project_path_internal}")

        result_message = f"Attempting to run Maven goals '{' '.join(effective_goals)}' on project at '{self._project_path_internal}'.\n"
        result_message += f"Full Command: {' '.join(command)}\n"

        try:
            process = subprocess.run(
                command,
                cwd=str(self._project_path_internal),
                capture_output=True,
                text=True,
                check=False,
                timeout=600
            )

            stdout_summary = process.stdout[-2000:]
            stderr_summary = process.stderr[-2000:]
            status = "success" if process.returncode == 0 else "error"

            if process.returncode == 0:
                result_message += "Maven execution successful.\n"
            else:
                result_message += f"Maven execution failed (return code: {process.returncode}).\n"

            result_message += f"\n--- STDOUT (Last 2000 chars) ---\n{stdout_summary}\n"
            if process.stderr:
                result_message += f"\n--- STDERR (Last 2000 chars) ---\n{stderr_summary}\n"

            if "[ERROR]" in process.stdout or "[ERROR]" in process.stderr:
                if "COMPILATION ERROR" in process.stdout or "COMPILATION ERROR" in process.stderr:
                    status = "compilation_error"
                    result_message += "\n[TOOL_NOTE] COMPILATION ERRORS DETECTED in Maven output.\n"

            final_summary = (
                f"Maven Execution Summary for: {self._project_path_internal}\n"
                f"Goals: {effective_goals}\n"
                f"Status: {status}\n"
                f"Tool Message: {result_message.splitlines()[0]}\n"
                f"STDOUT Snippet: {stdout_summary}\n"
                f"STDERR Snippet: {stderr_summary if process.stderr else 'None'}\n"
            )
            if status != "success":
                final_summary += "\nACTION_REQUIRED: Review STDOUT/STDERR for specific Maven errors."

            return final_summary.strip()

        except subprocess.TimeoutExpired:
            logger.error(f"Maven execution timed out for project: {self._project_path_internal}")
            return f"Error: Maven execution timed out after 600 seconds for project: {self._project_path_internal}."
        except FileNotFoundError:
            logger.error(f"Maven command ('{self._mvn_cmd}') not found. Ensure it's in your PATH.")
            return f"Error: Maven command ('{self._mvn_cmd}') not found. Ensure it's in your PATH."
        except Exception as e:
            logger.error(f"An exception occurred while running Maven: {e} for project {self._project_path_internal}")
            return f"Error: An unexpected exception occurred: {e}"