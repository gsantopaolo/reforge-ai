# tools/plan_tool.py
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path

class ReadPlanInput(BaseModel):
    """Input for reading the plan file. No parameters needed."""
    pass

class WritePlanInput(BaseModel):
    """Input for writing to the plan file."""
    full_plan_content: str = Field(..., description="The complete new content for the plan file. The LLM must provide the entire updated plan.")

class PlanToolActionInput(BaseModel):
    action: str = Field(..., description="The action to perform: 'read_plan' or 'write_plan'.")
    content_to_write: Optional[str] = Field(None, description="The full content to write to the plan file (only for 'write_plan' action).")

class PlanTool(BaseTool):
    name: str = "PlanFileAccessTool"
    description: str = (
        "Provides access to the modernization plan Markdown file. "
        "It can read the entire content of the plan or overwrite the entire plan with new content. "
        "The interpretation of the plan's content (e.g., finding next steps, updating status) "
        "is handled by the LLM agent using this tool."
    )
    args_schema: Type[BaseModel] = PlanToolActionInput
    plan_file_path: Path

    def __init__(self, plan_file: str, **kwargs):
        super().__init__(**kwargs)
        self.plan_file_path = Path(plan_file)
        # No action-specific checks in __init__; those belong in the action methods.

    def _read_plan_content(self) -> str:
        if not self.plan_file_path.is_file():
            # If the intent is to read, but the file doesn't exist, this is an error.
            return f"Error: Plan file not found at {self.plan_file_path}. Cannot read."
        try:
            with open(self.plan_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading plan file: {e}"

    def _write_plan_content(self, new_content: str) -> str:
        try:
            # Ensure parent directory exists, useful if writing a new plan file.
            self.plan_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.plan_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return "Plan file updated successfully with new content."
        except Exception as e:
            return f"Error writing to plan file: {e}"

    # ---- Methods for direct use by script (not via _run) ----
    def read_plan(self) -> str:
        """Script-callable version to read the entire plan."""
        return self._read_plan_content()

    def write_plan(self, new_content: str) -> str:
        """Script-callable version to overwrite the entire plan."""
        return self._write_plan_content(new_content)
    # ---- End Script-callable methods ----

    def _run(self, action: str, content_to_write: Optional[str] = None) -> str:
        if action == "read_plan":
            return self._read_plan_content()
        elif action == "write_plan":
            if content_to_write is None:
                return "Error: 'content_to_write' is required for 'write_plan' action."
            return self._write_plan_content(content_to_write)
        else:
            return f"Error: Unknown action '{action}'. Valid actions are 'read_plan' or 'write_plan'."