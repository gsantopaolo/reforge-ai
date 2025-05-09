# tools/open_rewrite_tool.py
from typing import Type, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import subprocess
import os


class OpenRewriteToolInput(BaseModel):
    """Input for applying OpenRewrite recipes to a Java codebase."""
    project_path: str = Field(...,
                              description="The absolute path to the root of the Java project (e.g., where pom.xml or build.gradle is located).")
    recipes: List[str] = Field(...,
                               description="A list of OpenRewrite recipe identifiers to apply (e.g., 'org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2').")
    # Optional: For Maven/Gradle specific execution
    build_tool: Optional[str] = Field("maven",
                                      description="The build tool of the project ('maven' or 'gradle'). Defaults to 'maven'.")
    # Optional: To generate a diff instead of applying changes directly
    # generate_diff_only: bool = Field(False, description="If true, generates a diff file instead of applying changes directly. (Requires recipe/CLI support)")


class OpenRewriteTool(BaseTool):
    name: str = "JavaCodeRefactorOpenRewrite"
    description: str = (
        "Applies specified OpenRewrite recipes to a Java codebase to automate refactoring. "
        "Can target Maven or Gradle projects. Ensure OpenRewrite is configured in the target project's build file or a CLI is available."
    )
    args_schema: Type[BaseModel] = OpenRewriteToolInput

    # You might want to configure paths to Maven/Gradle executables if not in PATH
    # mvn_executable: str = "mvn"
    # gradle_executable: str = "./gradlew" # Or "gradle"

    def _run_maven_rewrite(self, project_path_str: str, recipes: List[str]) -> Dict[str, Any]:
        """Executes OpenRewrite using the Maven plugin."""
        project_path = Path(project_path_str)
        pom_file = project_path / "pom.xml"
        if not pom_file.exists():
            return {"status": "error", "message": f"pom.xml not found in {project_path}. Cannot run Maven OpenRewrite."}

        # Ensure the rewrite plugin is configured in the pom.xml with <activeRecipes>
        # or that the recipes can be activated via command line.
        # Example: mvn org.openrewrite.maven:rewrite-maven-plugin:run -Drewrite.activeRecipes=com.yourorg.YourRecipe

        # Constructing a general command. Specific plugin versions and configurations might differ.
        # This assumes the plugin is already configured in the pom.xml to pick up recipes,
        # or you can pass them via -Drewrite.activeRecipes
        active_recipes_str = ",".join(recipes)
        command = [
            "mvn",
            "-f", str(pom_file),
            "org.openrewrite.maven:rewrite-maven-plugin:run",
            f"-Drewrite.activeRecipes={active_recipes_str}"
            # Add -Drewrite.plainTextMasks if you need to see diffs for non-Java files
        ]

        result_message = f"Attempting to apply recipes: {active_recipes_str} using Maven.\n"
        try:
            # It's crucial to run this in the project's directory
            process = subprocess.run(command, cwd=str(project_path), capture_output=True, text=True, check=False)

            if process.returncode == 0:
                result_message += "OpenRewrite Maven plugin executed successfully.\n"
                result_message += "Output:\n" + process.stdout
                # To get a diff, you'd ideally configure OpenRewrite to output a patch file
                # or run `git diff` after execution if changes are made directly.
                # For now, we assume changes are applied directly.
                return {"status": "success", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
            else:
                result_message += f"OpenRewrite Maven plugin execution failed (return code: {process.returncode}).\n"
                result_message += "Stdout:\n" + process.stdout + "\n"
                result_message += "Stderr:\n" + process.stderr
                return {"status": "error", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
        except FileNotFoundError:
            return {"status": "error", "message": "Maven (mvn) command not found. Ensure it's in your PATH."}
        except Exception as e:
            return {"status": "error", "message": f"An exception occurred while running Maven OpenRewrite: {e}"}

    def _run_gradle_rewrite(self, project_path_str: str, recipes: List[str]) -> Dict[str, Any]:
        """Executes OpenRewrite using the Gradle plugin."""
        project_path = Path(project_path_str)
        gradle_script_name = "gradlew.bat" if os.name == 'nt' else "gradlew"
        gradle_executable = project_path / gradle_script_name

        if not gradle_executable.exists():
            # Fallback to system gradle if gradlew is not present
            gradle_executable_cmd = "gradle"
        else:
            gradle_executable_cmd = str(gradle_executable)

        # Ensure the rewrite plugin (id("org.openrewrite.rewrite")) is applied in build.gradle
        # and recipes can be activated.
        # Example: ./gradlew rewriteRun -Prewrite.activeRecipes=com.yourorg.YourRecipe
        active_recipes_str = ",".join(recipes)
        command = [
            gradle_executable_cmd,
            "-p", str(project_path),  # Specify project directory
            "rewriteRun",
            f"-Prewrite.activeRecipes={active_recipes_str}"
        ]

        result_message = f"Attempting to apply recipes: {active_recipes_str} using Gradle.\n"
        try:
            process = subprocess.run(command, cwd=str(project_path), capture_output=True, text=True, check=False)

            if process.returncode == 0:
                result_message += "OpenRewrite Gradle plugin executed successfully.\n"
                result_message += "Output:\n" + process.stdout
                return {"status": "success", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
            else:
                result_message += f"OpenRewrite Gradle plugin execution failed (return code: {process.returncode}).\n"
                result_message += "Stdout:\n" + process.stdout + "\n"
                result_message += "Stderr:\n" + process.stderr
                return {"status": "error", "message": result_message, "stdout": process.stdout,
                        "stderr": process.stderr}
        except FileNotFoundError:
            return {"status": "error",
                    "message": f"Gradle command ('{gradle_executable_cmd}') not found. Ensure it's in your PATH or gradlew exists."}
        except Exception as e:
            return {"status": "error", "message": f"An exception occurred while running Gradle OpenRewrite: {e}"}

    def _run(self, project_path: str, recipes: List[str], build_tool: Optional[str] = "maven") -> str:
        """
        Applies OpenRewrite recipes to the specified Java project.
        """
        resolved_project_path = Path(project_path).resolve()
        if not resolved_project_path.is_dir():
            return f"Error: Project path '{resolved_project_path}' not found or not a directory."

        if not recipes:
            return "Error: No OpenRewrite recipes provided to apply."

        result_dict: Dict[str, Any]
        if build_tool.lower() == "maven":
            result_dict = self._run_maven_rewrite(str(resolved_project_path), recipes)
        elif build_tool.lower() == "gradle":
            result_dict = self._run_gradle_rewrite(str(resolved_project_path), recipes)
        else:
            return f"Error: Unsupported build tool '{build_tool}'. Supported: 'maven', 'gradle'."

        # For the agent, we return a summarized string.
        # The dictionary could be useful if the calling Python script wanted structured output.
        summary_str = f"OpenRewrite Execution Summary for project: {resolved_project_path}\n"
        summary_str += f"Build Tool: {build_tool}\n"
        summary_str += f"Recipes: {', '.join(recipes)}\n"
        summary_str += f"Status: {result_dict['status']}\n"
        summary_str += f"Message: {result_dict['message']}\n"
        if result_dict.get("stdout"):
            summary_str += f"--- STDOUT ---\n{result_dict['stdout'][:1000]}...\n"  # Truncate for brevity
        if result_dict.get("stderr"):
            summary_str += f"--- STDERR ---\n{result_dict['stderr'][:1000]}...\n"

        if result_dict['status'] == 'success':
            summary_str += "\nINFO: Code changes were likely applied directly to the project. A 'git diff' can show changes if the project is a git repository."

        return summary_str