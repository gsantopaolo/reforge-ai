# tools/file_system_read_tool.py
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import os


class FileSystemReadToolInput(BaseModel):
    """Input for reading a file from the file system."""
    file_path: str = Field(..., description="The absolute or relative path to the file to be read.")
    # Optional: Add encoding if you need to handle various file encodings
    # encoding: Optional[str] = Field("utf-8", description="The encoding of the file to be read.")


class FileSystemReadTool(BaseTool):
    name: str = "FileSystemReadFile"
    description: str = (
        "Reads the entire content of a specified file from the file system. "
        "Provide the full path to the file."
    )
    args_schema: Type[BaseModel] = FileSystemReadToolInput

    # Optional: base_path to restrict reading to a certain directory for security
    # base_path: Optional[Path] = None

    # def __init__(self, base_path: Optional[str] = None, **kwargs):
    #     super().__init__(**kwargs)
    #     if base_path:
    #         self.base_path = Path(base_path).resolve()
    #     else:
    #         self.base_path = None

    def _resolve_path(self, file_path_str: str) -> Path:
        """
        Resolves the provided file path.
        If a base_path is configured for the tool, the file_path is treated
        as relative to that base_path and an error is raised if it tries to
        escape the base_path. Otherwise, it's resolved normally.
        """
        # if self.base_path:
        #     abs_file_path = (self.base_path / file_path_str).resolve()
        #     # Security check: Ensure the resolved path is within the base_path
        #     if self.base_path not in abs_file_path.parents and abs_file_path != self.base_path :
        #         raise ValueError(
        #             f"Access denied: Path '{file_path_str}' attempts to escape the tool's base directory '{self.base_path}'."
        #         )
        #     return abs_file_path
        # else:
        # Always resolve to an absolute path for consistency and to avoid ambiguity
        return Path(file_path_str).resolve()

    def _run(self, file_path: str) -> str:
        """
        Reads the content of the specified file.
        The 'file_path' argument is automatically populated by CrewAI from the args_schema.
        """
        try:
            resolved_path = self._resolve_path(file_path)

            if not resolved_path.is_file():
                return f"Error: File not found at '{resolved_path}'."

            # Security check: ensure we are not reading from unexpected places if a base_path was intended
            # This basic check prevents '..' from going too far up IF base_path logic was enabled.
            # With current _resolve_path, it just checks if the final path is a file.
            # A more robust sandboxing might be needed for untrusted inputs.

            with open(resolved_path, 'r', encoding='utf-8') as f:  # Assuming utf-8, make configurable if needed
                content = f.read()
            return content
        except ValueError as ve:  # From _resolve_path if base_path logic is enabled and violated
            return f"Error: {ve}"
        except Exception as e:
            return f"Error reading file '{file_path}': {e}"

    # You can add direct script-callable methods if needed, like in PlanTool,
    # but for this tool, agents will primarily use _run.
    # def read_file_content(self, file_path_str: str) -> str:
    #     return self._run(file_path=file_path_str)