# tools/legacy_compiler_tool.py
from typing import Type, Optional, Dict, Any, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import subprocess
import os
import logging

logger = logging.getLogger(__name__)


class CompilerToolInput(BaseModel):
    project_path: Optional[str] = Field(None,  # Changed to Optional to allow default path usage
                                        description="The absolute path to the root of the Java project. If None, uses default path.")


class LegacyCompilerTool(BaseTool):
    name: str = "LegacyJavaProjectCompiler"
    description: str = (
        "Compiles a legacy Java project (e.g., JBoss EE) using Maven or Gradle. "
        "Ensure the project has a valid pom.xml or build.gradle. "
        "The appropriate JDK for the legacy project should be active in the environment (e.g., via JAVA_HOME)."
    )
    args_schema: Type[BaseModel] = CompilerToolInput

    _default_legacy_code_path_internal: Path  # Internal instance attribute

    def __init__(self, legacy_code_path: str, **kwargs: Any):
        super().__init__(**kwargs)  # Call BaseTool's Pydantic init first

        self._default_legacy_code_path_internal = Path(legacy_code_path).resolve()
        if not self._default_legacy_code_path_internal.is_dir():
            logger.error(
                f"LegacyCompilerTool: Default legacy code path '{self._default_legacy_code_path_internal}' is not a valid directory.")
            raise ValueError(
                f"Default legacy code path '{self._default_legacy_code_path_internal}' for LegacyCompilerTool is not a valid directory.")

    def _compile_project(self, project_path_str: str) -> Dict[str, Any]:
        project_path = Path(project_path_str).resolve()
        if not project_path.is_dir():
            return {"status": "error", "message": f"Project path '{project_path}' not found or not a directory."}

        pom_file = project_path / "pom.xml"
        gradle_file = project_path / "build.gradle"
        gradle_kts_file = project_path / "build.gradle.kts"

        build_tool_used = ""
        command: List[str] = []

        if pom_file.exists():
            build_tool_used = "Maven"
            command = ["mvn", "-f", str(pom_file), "clean", "compile"]
        elif gradle_file.exists() or gradle_kts_file.exists():
            build_tool_used = "Gradle"
            gradle_script_name = "gradlew.bat" if os.name == 'nt' else "gradlew"
            gradle_executable = project_path / gradle_script_name
            gradle_cmd_prefix = str(gradle_executable) if gradle_executable.exists() else "gradle"
            command = [gradle_cmd_prefix, "-p", str(project_path), "clean", "build", "--exclude-task", "test"]
        else:
            return {"status": "error", "message": f"No pom.xml or build.gradle[.kts] found in {project_path}."}

        result_message = f"Attempting to compile legacy project at '{project_path}' using {build_tool_used}.\n"
        result_message += f"Command: {' '.join(command)}\n"

        try:
            process = subprocess.run(command, cwd=str(project_path), capture_output=True, text=True, check=False,
                                     timeout=300)
            if process.returncode == 0:
                result_message += f"{build_tool_used} compilation successful.\n"
                return {"status": "success", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
            else:
                result_message += f"{build_tool_used} compilation failed (return code: {process.returncode}).\n"
                return {"status": "error", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
        except subprocess.TimeoutExpired:
            result_message += f"{build_tool_used} compilation timed out after 300 seconds.\n"
            return {"status": "error", "message": result_message, "stdout": "Timeout", "stderr": "Timeout"}
        except FileNotFoundError:
            cmd_name = command[0]
            return {"status": "error",
                    "message": f"{build_tool_used} command ('{cmd_name}') not found. Ensure it's in your PATH or executable."}
        except Exception as e:
            return {"status": "error", "message": f"An exception occurred during {build_tool_used} compilation: {e}"}

    def _run(self, project_path: Optional[str] = None) -> str:
        path_to_compile = Path(project_path).resolve() if project_path else self._default_legacy_code_path_internal

        result_dict = self._compile_project(str(path_to_compile))

        output_str = f"Legacy Compilation Summary for: {path_to_compile}\n"
        output_str += f"Status: {result_dict['status']}\n"
        output_str += f"Message From Tool: {result_dict['message']}\n"
        if result_dict.get("stdout"):
            output_str += f"--- STDOUT ---\n{result_dict['stdout'][:2000]}\n"
        if result_dict.get("stderr"):
            output_str += f"--- STDERR ---\n{result_dict['stderr'][:2000]}\n"

        return output_str.strip()