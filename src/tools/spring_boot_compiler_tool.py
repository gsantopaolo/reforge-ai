# tools/spring_boot_compiler_tool.py
from typing import Type, Optional, Dict, Any, List # Added List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import subprocess
import os

# Re-using the same input schema as LegacyCompilerTool for consistency
class CompilerToolInput(BaseModel):
    """Input for compiling a Java project."""
    project_path: str = Field(..., description="The absolute path to the root of the Java project (e.g., where pom.xml or build.gradle is located).")
    # Optional: clean_before_compile: bool = Field(True, description="Whether to run a 'clean' build phase before compiling.")
    # Optional: extra_args: Optional[List[str]] = Field(None, description="Extra arguments to pass to the build command.")


class SpringBootCompilerTool(BaseTool):
    name: str = "SpringBootProjectCompiler"
    description: str = (
        "Compiles a Spring Boot / Java 21 project using Maven or Gradle. "
        "Ensure the project has a valid pom.xml or build.gradle. "
        "The appropriate JDK (e.g., JDK 21) should be active in the environment (e.g., via JAVA_HOME)."
    )
    args_schema: Type[BaseModel] = CompilerToolInput

    # Default path if not provided in _run, configured at instantiation
    default_spring_code_path: Path

    def __init__(self, spring_code_path: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.default_spring_code_path = Path(spring_code_path).resolve()
        if not self.default_spring_code_path.is_dir():
            # This is a configuration error for the tool itself
            raise ValueError(f"Default Spring Boot code path '{self.default_spring_code_path}' for SpringBootCompilerTool is not a valid directory.")

    def _compile_project(self, project_path_str: str) -> Dict[str, Any]:
        """Shared compilation logic, same as in LegacyCompilerTool."""
        project_path = Path(project_path_str).resolve()
        if not project_path.is_dir():
            return {"status": "error", "message": f"Project path '{project_path}' not found or not a directory."}

        pom_file = project_path / "pom.xml"
        gradle_file = project_path / "build.gradle"
        gradle_kts_file = project_path / "build.gradle.kts"

        build_tool_used = ""
        command: List[str] = [] # Explicitly List[str]

        if pom_file.exists():
            build_tool_used = "Maven"
            # For Spring Boot, 'package' is often used to get the executable JAR,
            # but 'compile' is sufficient to check if code builds.
            # Using 'clean package' to be more comprehensive for Spring Boot.
            command = ["mvn", "-f", str(pom_file), "clean", "package", "-DskipTests"] # Skip tests during this compile phase
        elif gradle_file.exists() or gradle_kts_file.exists():
            build_tool_used = "Gradle"
            gradle_script_name = "gradlew.bat" if os.name == 'nt' else "gradlew"
            gradle_executable = project_path / gradle_script_name

            gradle_cmd_prefix = str(gradle_executable) if gradle_executable.exists() else "gradle"
            # For Spring Boot, 'bootJar' or 'build' (which includes bootJar) are common.
            # 'build' is generally fine and includes compilation.
            command = [gradle_cmd_prefix, "-p", str(project_path), "clean", "build", "-x", "test"] # -x test is Gradle way to skip tests
        else:
            return {"status": "error", "message": f"No pom.xml or build.gradle[.kts] found in {project_path}."}

        result_message = f"Attempting to compile Spring Boot project at '{project_path}' using {build_tool_used}.\n"
        result_message += f"Command: {' '.join(command)}\n"

        try:
            # Setting JAVA_HOME might be necessary if multiple JDKs are installed and the correct one isn't default.
            # This is an advanced setup and depends on your environment management.
            # For now, assume the environment is pre-configured with the correct JDK for Spring Boot/Java 21.
            process = subprocess.run(command, cwd=str(project_path), capture_output=True, text=True, check=False, timeout=300) # 5 min timeout

            if process.returncode == 0:
                result_message += f"{build_tool_used} compilation/package successful.\n"
                return {"status": "success", "message": result_message, "stdout": process.stdout, "stderr": process.stderr}
            else:
                result_message += f"{build_tool_used} compilation/package failed (return code: {process.returncode}).n"
                return {"status": "error", "message": result_message, "stdout": process.stdout, "stderr": process.stderr}
        except subprocess.TimeoutExpired:
            result_message += f"{build_tool_used} compilation/package timed out after 300 seconds.\n"
            return {"status": "error", "message": result_message, "stdout": "Timeout", "stderr": "Timeout"}
        except FileNotFoundError:
            cmd_name = command[0]
            return {"status": "error", "message": f"{build_tool_used} command ('{cmd_name}') not found. Ensure it's in your PATH or executable."}
        except Exception as e:
            return {"status": "error", "message": f"An exception occurred during {build_tool_used} compilation/package: {e}"}

    def _run(self, project_path: Optional[str] = None) -> str:
        """
        Compiles the Spring Boot Java project.
        If project_path is not provided, uses the default_spring_code_path configured at instantiation.
        """
        # If project_path is explicitly given in tool input, use it. Otherwise, use default.
        path_to_compile = Path(project_path).resolve() if project_path else self.default_spring_code_path

        result_dict = self._compile_project(str(path_to_compile))

        # Format a string output for the agent
        output_str = f"Spring Boot Compilation Summary for: {path_to_compile}\n"
        output_str += f"Status: {result_dict['status']}\n"
        output_str += f"Message From Tool: {result_dict['message']}\n" # Contains command and tool's own messages
        if result_dict.get("stdout"):
            output_str += f"--- STDOUT ---\n{result_dict['stdout'][:2000]}\n" # Truncate
        if result_dict.get("stderr"):
            output_str += f"--- STDERR ---\n{result_dict['stderr'][:2000]}\n" # Truncate

        return output_str.strip()