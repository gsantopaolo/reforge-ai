# tools/file_system_read_write_tool.py
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import os  # Not strictly needed in this version if shutil is used for all
import shutil
import logging  # Added for consistency

logger = logging.getLogger(__name__)  # Logger for this tool


class FileSystemReadWriteActionInput(BaseModel):
    action: str = Field(...,
                        description="The action to perform: 'read_file', 'write_file', 'delete_file', 'create_directory'.")
    file_path: str = Field(...,
                           description="The relative path to the file or directory, interpreted from the tool's base_write_path.")
    content: Optional[str] = Field(None, description="The content to write to the file (only for 'write_file' action).")
    overwrite: Optional[bool] = Field(False,
                                      description="Whether to overwrite the file if it already exists (for 'write_file' action). Defaults to False.")


class FileSystemReadWriteTool(BaseTool):
    name: str = "FileSystemReadWriteTool"  # ENSURE THIS MATCHES YOUR agents.yaml
    description: str = (
        "Performs file system operations: read, write, delete files, and create directories. "
        "All operations are restricted to a pre-configured base working directory for security. "
        "Provide paths relative to this base directory."
    )
    args_schema: Type[BaseModel] = FileSystemReadWriteActionInput

    # REMOVE: base_write_path: Path
    _base_write_path_internal: Path  # Internal instance attribute

    def __init__(self, base_write_path: str, **kwargs: Any):
        super().__init__(**kwargs)  # Call BaseTool's Pydantic init first

        # Then set custom instance attributes
        self._base_write_path_internal = Path(base_write_path).resolve()
        try:
            self._base_write_path_internal.mkdir(parents=True, exist_ok=True)
            if not self._base_write_path_internal.is_dir():
                # This should ideally not happen if mkdir worked or it already existed as a dir
                raise ValueError(
                    f"Base write path '{self._base_write_path_internal}' could not be confirmed as a directory.")
        except Exception as e:
            logger.error(
                f"Error ensuring base_write_path exists for FileSystemReadWriteTool: {self._base_write_path_internal}. Error: {e}")
            raise ValueError(f"Could not initialize FileSystemReadWriteTool due to base path issue: {e}")

    def _resolve_path_within_base(self, relative_path_str: str) -> Path:
        if not relative_path_str:
            raise ValueError("Error: file_path cannot be empty for FileSystemReadWriteTool.")

        # Path.joinpath or / operator is safe for constructing paths
        prospective_path = (self._base_write_path_internal / relative_path_str).resolve()

        # Security check: ensure it's within the base path
        try:
            prospective_path.relative_to(self._base_write_path_internal)
        except ValueError:  # This means prospective_path is not a sub-path
            logger.error(f"Access Denied: Path '{relative_path_str}' (resolved to '{prospective_path}') "
                         f"attempts to escape the tool's base directory '{self._base_write_path_internal}'.")
            raise ValueError(
                f"Access Denied: Path operation outside of designated base directory."
            )
        return prospective_path

    def _read_file(self, relative_file_path: str) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_file_path)
            if not resolved_path.is_file():
                return f"Error: File not found at '{resolved_path}' (relative path: '{relative_file_path}')."
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except ValueError as ve:
            return f"Error resolving path for read: {ve}"
        except Exception as e:
            return f"Error reading file '{relative_file_path}': {e}"

    def _write_file(self, relative_file_path: str, content: str, overwrite: bool) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_file_path)
            if resolved_path.is_dir():
                return f"Error: Path '{resolved_path}' (relative: '{relative_file_path}') is a directory, cannot write file."
            if resolved_path.exists() and not overwrite:
                return f"Error: File '{resolved_path}' (relative: '{relative_file_path}') already exists and overwrite is False."

            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File '{resolved_path}' (relative: '{relative_file_path}') written successfully."
        except ValueError as ve:
            return f"Error resolving path for write: {ve}"
        except Exception as e:
            return f"Error writing file '{relative_file_path}': {e}"

    def _delete_file(self, relative_file_path: str) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_file_path)
            if not resolved_path.exists():
                return f"Error: File or directory not found at '{resolved_path}' (relative: '{relative_file_path}') for deletion."
            if resolved_path.is_dir():
                return f"Error: Path '{resolved_path}' is a directory. This tool deletes files only."
            elif resolved_path.is_file():
                resolved_path.unlink()
                return f"File '{resolved_path}' (relative: '{relative_file_path}') deleted successfully."
            else:
                return f"Error: Path '{resolved_path}' (relative: '{relative_file_path}') is not a regular file. Deletion aborted."
        except ValueError as ve:
            return f"Error resolving path for delete: {ve}"
        except Exception as e:
            return f"Error deleting file '{relative_file_path}': {e}"

    def _create_directory(self, relative_dir_path: str) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_dir_path)
            if resolved_path.exists() and resolved_path.is_dir():
                return f"Directory '{resolved_path}' (relative: '{relative_dir_path}') already exists."
            if resolved_path.exists() and not resolved_path.is_dir():
                return f"Error: Path '{resolved_path}' (relative: '{relative_dir_path}') exists and is not a directory."

            resolved_path.mkdir(parents=True, exist_ok=True)
            return f"Directory '{resolved_path}' (relative: '{relative_dir_path}') created successfully."
        except ValueError as ve:
            return f"Error resolving path for create_directory: {ve}"
        except Exception as e:
            return f"Error creating directory '{relative_dir_path}': {e}"

    def _run(self, action: str, file_path: str, content: Optional[str] = None,
             overwrite: Optional[bool] = False) -> str:
        # Ensure overwrite gets a default if None, as Pydantic might pass None if not specified by agent
        effective_overwrite = overwrite if overwrite is not None else False

        if action == "read_file":
            return self._read_file(file_path)
        elif action == "write_file":
            if content is None:
                return "Error: 'content' is required for 'write_file' action."
            return self._write_file(file_path, content, effective_overwrite)
        elif action == "delete_file":
            return self._delete_file(file_path)
        elif action == "create_directory":
            return self._create_directory(file_path)
        else:
            return f"Error: Unknown action '{action}'. Valid actions: 'read_file', 'write_file', 'delete_file', 'create_directory'."