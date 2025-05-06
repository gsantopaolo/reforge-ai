import os
import subprocess
from typing import Type

from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools.base_tool import BaseTool


class JDepsInput(BaseModel):
    """
    Input arguments for JDepsTool.
    """
    target_path: str = Field(
        ...,
        description="Filesystem path to compiled class files or JAR"
    )
    jdk_internals: bool = Field(
        True,
        description="Whether to include JDK internal API usage in the analysis"
    )
    recursive: bool = Field(
        True,
        description="Whether to recurse into subpackages (the -R flag)"
    )


class JDepsTool(BaseTool):
    """
    Wrapper for the `jdeps` CLI to analyze Java dependencies and internal APIs.
    """
    name: str = "jdeps"
    description: str = "Analyze Java dependencies and JDK internal API usage via the jdeps CLI"
    args_schema: Type[JDepsInput] = JDepsInput

    # Declare the executable path as a private attribute
    _jdeps_cmd: str = PrivateAttr()

    def __init__(self, java_home: str = None):
        super().__init__()  # initialize BaseTool/BaseModel internals
        if java_home:
            self._jdeps_cmd = os.path.join(java_home, "bin", "jdeps")
        else:
            self._jdeps_cmd = "jdeps"

    def _run(self, target_path: str, jdk_internals: bool, recursive: bool) -> dict:
        """
        Execute jdeps with the specified flags and return parsed results.
        """
        cmd = [self._jdeps_cmd]
        if jdk_internals:
            cmd.append("--jdk-internals")
        if recursive:
            cmd.append("-R")
        cmd.extend(["-s", target_path])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"jdeps failed (exit {e.returncode}): {e.stderr.strip()}")

        output = result.stdout
        issues = [
            line.strip()
            for line in output.splitlines()
            if "JDK internal API" in line or line.startswith("jdeps:")
        ]

        return {
            "jdeps_output": output,
            "identified_issues": issues
        }
