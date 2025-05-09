# tools/file_system_read_write_tool.py
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import os
import shutil


class FileSystemReadWriteActionInput(BaseModel):
    """Input schema for the FileSystemReadWriteTool's _run method."""
    action: str = Field(...,
                        description="The action to perform: 'read_file', 'write_file', 'delete_file', 'create_directory'.")
    file_path: str = Field(...,
                           description="The relative path to the file or directory, interpreted from the tool's base_write_path.")
    content: Optional[str] = Field(None, description="The content to write to the file (only for 'write_file' action).")
    overwrite: Optional[bool] = Field(False,
                                      description="Whether to overwrite the file if it already exists (for 'write_file' action). Defaults to False.")


class FileSystemReadWriteTool(BaseTool):
    name: str = "FileSystemReadWrite"
    description: str = (
        "Performs file system operations: read, write, delete files, and create directories. "
        "All operations are restricted to a pre-configured base working directory for security. "
        "Provide paths relative to this base directory."
    )
    args_schema: Type[BaseModel] = FileSystemReadWriteActionInput

    base_write_path: Path  # All operations are confined here.

    def __init__(self, base_write_path: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.base_write_path = Path(base_write_path).resolve()
        # Ensure the base path exists, or create it
        self.base_write_path.mkdir(parents=True, exist_ok=True)
        if not self.base_write_path.is_dir():
            raise ValueError(
                f"Base write path '{self.base_write_path}' is not a valid directory or could not be created.")

    def _resolve_path_within_base(self, relative_path_str: str) -> Path:
        """
        Resolves the provided relative path against the base_write_path.
        Ensures the resulting path is within the base_write_path for security.
        """
        if not relative_path_str:  # Handle empty path string if it occurs
            raise ValueError("Error: file_path cannot be empty.")

        # Normalize path to prevent '..' from creating issues if not handled by resolve() correctly in all OS.
        # os.path.normpath can help, but Path.resolve() usually handles this.
        # However, an explicit check after resolving is safer.

        # Treat the input path as relative to the base_write_path
        # Path.joinpath() is safer than string concatenation for paths
        prospective_path = (self.base_write_path / relative_path_str).resolve()

        # Security check: Ensure the resolved path is truly within the base_write_path
        # and doesn't escape via symlinks or complex '..' sequences.
        if self.base_write_path not in prospective_path.parents and prospective_path != self.base_write_path:
            # Check if prospective_path is a direct child or the base_path itself.
            # If it's not, and base_path is not one of its parents, it's an escape attempt.
            is_safe = False
            try:
                prospective_path.relative_to(self.base_write_path)
                is_safe = True
            except ValueError:  # Not a subpath
                is_safe = False

            if not is_safe:
                raise ValueError(
                    f"Access Denied: Path '{relative_path_str}' (resolved to '{prospective_path}') "
                    f"attempts to escape the tool's base directory '{self.base_write_path}'."
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
        except ValueError as ve:  # From _resolve_path_within_base
            return f"Error: {ve}"
        except Exception as e:
            return f"Error reading file '{relative_file_path}': {e}"

    def _write_file(self, relative_file_path: str, content: str, overwrite: bool) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_file_path)

            if resolved_path.is_dir():
                return f"Error: Path '{resolved_path}' (relative path: '{relative_file_path}') is a directory, cannot write file."

            if resolved_path.exists() and not overwrite:
                return f"Error: File '{resolved_path}' already exists and overwrite is set to False."

            # Ensure parent directory of the file exists
            resolved_path.parent.mkdir(parents=True, exist_ok=True)

            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File '{resolved_path}' (relative path: '{relative_file_path}') written successfully."
        except ValueError as ve:  # From _resolve_path_within_base
            return f"Error: {ve}"
        except Exception as e:
            return f"Error writing file '{relative_file_path}': {e}"

    def _delete_file(self, relative_file_path: str) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_file_path)
            if not resolved_path.exists():
                return f"Error: File or directory not found at '{resolved_path}' (relative path: '{relative_file_path}') for deletion."

            if resolved_path.is_dir():
                # For safety, let's not allow recursive directory deletion by default with this simple tool.
                # If you need it, add a specific action or flag, and be very careful.
                # shutil.rmtree(resolved_path)
                return f"Error: Path '{resolved_path}' is a directory. This tool currently only deletes files. For directory deletion, use a dedicated directory management tool or action."
            elif resolved_path.is_file():
                resolved_path.unlink()  # Deletes the file
                return f"File '{resolved_path}' (relative path: '{relative_file_path}') deleted successfully."
            else:  # Symlink or other
                return f"Error: Path '{resolved_path}' is not a regular file or directory. Deletion aborted."
        except ValueError as ve:  # From _resolve_path_within_base
            return f"Error: {ve}"
        except Exception as e:
            return f"Error deleting file '{relative_file_path}': {e}"

    def _create_directory(self, relative_dir_path: str) -> str:
        try:
            resolved_path = self._resolve_path_within_base(relative_dir_path)
            if resolved_path.exists() and resolved_path.is_dir():
                return f"Directory '{resolved_path}' (relative path: '{relative_dir_path}') already exists."
            if resolved_path.exists() and not resolved_path.is_dir():
                return f"Error: Path '{resolved_path}' (relative path: '{relative_dir_path}') exists and is not a directory."

            resolved_path.mkdir(parents=True, exist_ok=True)  # exist_ok=True is fine if we want to ensure it exists
            return f"Directory '{resolved_path}' (relative path: '{relative_dir_path}') created successfully."
        except ValueError as ve:  # From _resolve_path_within_base
            return f"Error: {ve}"
        except Exception as e:
            return f"Error creating directory '{relative_dir_path}': {e}"

    def _run(self, action: str, file_path: str, content: Optional[str] = None,
             overwrite: Optional[bool] = False) -> str:
        if action == "read_file":
            return self._read_file(file_path)
        elif action == "write_file":
            if content is None:
                return "Error: 'content' is required for 'write_file' action."
            return self._write_file(file_path, content, overwrite if overwrite is not None else False)
        elif action == "delete_file":
            return self._delete_file(file_path)
        elif action == "create_directory":
            return self._create_directory(file_path)
        else:
            return f"Error: Unknown action '{action}'. Valid actions are 'read_file', 'write_file', 'delete_file', 'create_directory'."