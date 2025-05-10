# tools/plan_tool.py
import yaml  # For YAML parsing
from typing import Type, Dict, Optional, List, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
from typing import Literal


# Import the Plan and PlanStep models (assuming they are in a separate file or above)
# If in the same file, they are already available.
# from .plan_models import Plan, PlanStep
# For simplicity, let's put them here for now:

class PlanStep(BaseModel):
    id: str = Field(..., description="Unique identifier for the plan step.")
    name: str = Field(..., description="A short, descriptive name for the step.")
    description: str = Field(..., description="A detailed description of what this step entails.")
    status: Literal["todo", "done", "skipped", "failed", "rejected", "in_progress"] = Field(
        default="todo",
        description="The current status of the step."
    )
    notes: Optional[str] = Field(None,
                                 description="Any notes, feedback, or reasons related to the current status or next actions.")


class Plan(BaseModel):
    steps: List[PlanStep] = Field(default_factory=list, description="The list of modernization steps.")


# Input Schemas for Tool Actions (remain similar)
class PlanToolGetNextStepInput(BaseModel):
    pass


class PlanToolGetStepDetailsInput(BaseModel):
    step_id: str = Field(..., description="The unique identifier of the plan step.")


class PlanToolUpdateStepStatusInput(BaseModel):
    step_id: str = Field(..., description="The unique identifier of the plan step.")
    new_status: Literal["todo", "done", "skipped", "failed", "rejected", "in_progress"] = Field(
        ...,
        description="The new status for the step."
    )
    notes: Optional[str] = Field(None, description="Optional notes to add or update for the step.")


class PlanToolActionInput(BaseModel):
    action: str = Field(..., description="Action: 'get_next_step', 'get_step_details', 'update_step_status'.")
    action_input: Optional[Dict[str, Any]] = Field(None, description="Inputs specific to the chosen action.")


class PlanTool(BaseTool):
    name: str = "PlanTool"
    description: str = (
        "Manages the modernization plan YAML file. "
        "It can retrieve the next step to be done, get details of a specific step, "
        "and update the status and notes for a step."
    )
    args_schema: Type[BaseModel] = PlanToolActionInput

    _plan_file_path_internal: Path

    def __init__(self, plan_file: str, **kwargs: Any):
        super().__init__(**kwargs)
        self._plan_file_path_internal = Path(plan_file).resolve()
        if not self._plan_file_path_internal.is_file():
            # Allow creation if it doesn't exist, will be created on first write.
            # Or raise error if it must exist:
            # raise FileNotFoundError(f"PlanTool configured with non-existent plan file: {self._plan_file_path_internal}")
            print(f"Warning: Plan file {self._plan_file_path_internal} not found. Will be created if written to.")

    def _load_plan(self) -> Plan:
        """Loads the plan from the YAML file."""
        if not self._plan_file_path_internal.is_file():
            return Plan(steps=[])  # Return an empty plan if file doesn't exist
        try:
            with open(self._plan_file_path_internal, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if data and "steps" in data:  # Ensure basic structure
                return Plan(**data)
            return Plan(steps=[])  # Return empty plan if file is empty or malformed
        except yaml.YAMLError as e:
            print(f"Error parsing YAML plan file ({self._plan_file_path_internal}): {e}")
            # Depending on desired robustness, either return empty plan or raise error
            return Plan(steps=[])
        except Exception as e:
            print(f"Unexpected error loading plan file ({self._plan_file_path_internal}): {e}")
            return Plan(steps=[])

    def _save_plan(self, plan: Plan) -> str:
        """Saves the plan to the YAML file."""
        try:
            # Ensure parent directory exists
            self._plan_file_path_internal.parent.mkdir(parents=True, exist_ok=True)
            with open(self._plan_file_path_internal, 'w', encoding='utf-8') as f:
                # Pydantic's model_dump is useful here for clean serialization
                yaml.dump(plan.model_dump(exclude_none=True), f, sort_keys=False, allow_unicode=True)
            return "Plan file updated successfully."
        except Exception as e:
            return f"Error writing plan file ({self._plan_file_path_internal}): {e}"

    def _get_next_step_to_do_logic(self) -> Optional[Dict[str, Any]]:
        plan = self._load_plan()
        for step in plan.steps:
            if step.status == "todo":
                return step.model_dump()  # Return as dict
        return None

    def _get_step_details_logic(self, step_id: str) -> Optional[Dict[str, Any]]:
        plan = self._load_plan()
        for step in plan.steps:
            if step.id == step_id:
                return step.model_dump()
        return None

    def _update_step_status_logic(self, step_id: str, new_status: str, notes: Optional[str] = None) -> str:
        plan = self._load_plan()
        step_found = False
        for step in plan.steps:
            if step.id == step_id:
                step.status = new_status
                if notes is not None:  # Allow clearing notes by passing empty string or explicitly setting new notes
                    step.notes = notes
                elif notes is None and new_status != step.status:  # If status changed and no notes provided, don't overwrite existing notes
                    pass  # Keep existing notes
                step_found = True
                break

        if not step_found:
            return f"Error: Step with ID '{step_id}' not found in the plan."

        return self._save_plan(plan)

    # ---- Methods for direct use by script (not via _run) ----
    def get_next_step_to_do(self) -> Optional[Dict[str, Any]]:
        return self._get_next_step_to_do_logic()

    def mark_step_as_done(self, step_id: str, notes: Optional[str] = "Completed by AI process.") -> str:
        return self._update_step_status_logic(step_id, "done", notes)

    def mark_step_as_todo(self, step_id: str, notes: str = "") -> str:
        return self._update_step_status_logic(step_id, "todo", notes)

    # ---- End Script-callable methods ----

    def _run(self, action: str, action_input: Optional[Dict[str, Any]] = None) -> Any:
        action_input = action_input or {}
        if action == "get_next_step":
            result = self._get_next_step_to_do_logic()
            return result if result else "No 'todo' steps found."
        elif action == "get_step_details":
            if "step_id" not in action_input: return "Error: 'step_id' is required."
            result = self._get_step_details_logic(action_input["step_id"])
            return result if result else f"Step with ID '{action_input['step_id']}' not found."
        elif action == "update_step_status":
            if "step_id" not in action_input or "new_status" not in action_input:
                return "Error: 'step_id' and 'new_status' are required."
            return self._update_step_status_logic(
                action_input["step_id"],
                action_input["new_status"],
                action_input.get("notes")  # notes are optional
            )
        else:
            return f"Error: Unknown action '{action}'. Valid: 'get_next_step', 'get_step_details', 'update_step_status'."