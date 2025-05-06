import os
import subprocess
from typing import Type

from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools.base_tool import BaseTool
# Optionally: from python_sonarqube_api import SonarQubeClient

class SonarInput(BaseModel):
    """
    Input arguments for the SonarQube analysis tool.
    """
    code_path: str = Field(..., description="Root directory of the source code to analyze")
    project_key: str = Field(..., description="Unique SonarQube project key")
    host_url: str = Field("http://localhost:9000", description="SonarQube server URL")
    token: str | None = Field(None, description="SonarQube authentication token")

class SonarTool(BaseTool):
    """
    CrewAI tool to perform SonarQube code analysis:
     - Runs the SonarScanner CLI
     - Fetches result metrics via SonarQube Web API
    """
    name: str = "sonar-scanner"
    description: str = "Analyze code with SonarQube Scanner and fetch metrics via API"
    args_schema: Type[SonarInput] = SonarInput

    # Private attributes for internal use only
    _scanner_cmd: str = PrivateAttr()
    _project_key: str = PrivateAttr()
    _host_url: str = PrivateAttr()
    _token: str | None = PrivateAttr()

    def __init__(self, sonar_scanner_path: str | None = None):
        super().__init__()  # initialize BaseModel internals
        # Locate the scanner binary, defaulting to `sonar-scanner` on PATH
        self._scanner_cmd = sonar_scanner_path or "sonar-scanner"

    def _run(
        self,
        code_path: str,
        project_key: str,
        host_url: str,
        token: str | None
    ) -> dict:
        """
        1) Run the SonarScanner CLI on `code_path`.
        2) Query the SonarQube Web API for project metrics.
        """
        # 1. CLI invocation
        cmd = [
            self._scanner_cmd,
            f"-Dsonar.projectKey={project_key}",
            f"-Dsonar.sources={code_path}",
            f"-Dsonar.host.url={host_url}"
        ]
        if token:
            cmd.append(f"-Dsonar.login={token}")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"SonarScanner failed (exit {e.returncode}): {e.stderr.strip()}")

        cli_output = result.stdout

        # 2. Fetch metrics via Web API (optional)
        # If you have `python-sonarqube-api`, you could do:
        #
        # client = SonarQubeClient(host=host_url, token=token)
        # metrics = client.measures.get_project_measures(
        #     projectKey=project_key,
        #     metricKeys=["bugs", "vulnerabilities", "code_smells"]
        # )
        #
        # For brevity, here we’ll return only the CLI summary.

        return {
            "cli_output": cli_output,
            # "api_metrics": metrics,  # uncomment if using python-sonarqube-api :contentReference[oaicite:7]{index=7}
        }
