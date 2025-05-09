# src/gen_code.py
# !/usr/bin/env python3
import sys
import os
import shutil
import json
from pathlib import Path
from typing import Dict
import logging  # Import logging module

# Assuming langtrace is configured elsewhere or not strictly needed for this core logic
# from langtrace_python_sdk import langtrace
# langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))

from crews.code_gen.code_gen_crew import CodeGenCrew
from tools.plan_tool import PlanTool  # For direct use by the script to get next step info

# --- Setup Logger ---
# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set default logging level

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PROJECT_ROOT = SCRIPT_DIR.parent.parent

CODEBASE_NAME = os.getenv("CODEBASE_NAME", "kitchensink")

LEGACY_CODEBASE_PATH = Path(
    os.getenv("LEGACY_CODEBASE_PATH", BASE_PROJECT_ROOT / "assessment_crew" / "temp_codebase" / CODEBASE_NAME))
WORKING_CODE_BASE_PATH = Path(os.getenv("WORKING_CODE_BASE_PATH", SCRIPT_DIR / "1-codegen-work" / CODEBASE_NAME))
GEN_DOCS_OUTPUT_PATH = Path(os.getenv("GEN_DOCS_OUTPUT_PATH", SCRIPT_DIR / "1-documentation" / "docs"))
KB_DOCS_PATH = Path(os.getenv("KB_DOCS_PATH", BASE_PROJECT_ROOT / "kb-docs"))
KB_CODE_PATH = Path(os.getenv("KB_CODE_PATH", BASE_PROJECT_ROOT / "kb-code"))

PLAN_FILE_NAME = os.getenv("PLAN_FILE_NAME", "7-PlanPhasedModuleExtraction.md")
PLAN_FILE_PATH = GEN_DOCS_OUTPUT_PATH / PLAN_FILE_NAME


# --- Helper Functions ---
def prepare_working_codebase(source_path: Path, target_path: Path):
    """Copies the source codebase to a fresh working directory for the current step."""
    if not source_path.is_dir():
        logger.error(f"❌ Source path for codebase copy does not exist or is not a directory: {source_path}")
        raise FileNotFoundError(f"Source path for codebase copy not found: {source_path}")

    if target_path.exists():
        logger.info(f"🧹 Cleaning up existing working directory: {target_path}")
        shutil.rmtree(target_path)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"📂 Copying codebase from {source_path} to working directory {target_path}")
    shutil.copytree(source_path, target_path)


def main():
    logger.info("🚀 Starting Code Generation Process...")
    llm_provider_name = os.getenv("LLM_PROVIDER", "N/A").upper()
    logger.info(f"🧠 GenAI provider in use: {llm_provider_name}")
    logger.info(f"🤖 Using Model: {os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')}")  # Or your general model_name

    logger.info(f"📜 PLAN_FILE_PATH: {PLAN_FILE_PATH}")
    logger.info(f"🏛️ LEGACY_CODEBASE_PATH (initial source): {LEGACY_CODEBASE_PATH}")
    logger.info(f"🛠️ WORKING_CODE_BASE_PATH (for modifications): {WORKING_CODE_BASE_PATH}")
    logger.info(f"📚 GEN_DOCS_OUTPUT_PATH (for SoftwareArchitect): {GEN_DOCS_OUTPUT_PATH}")
    logger.info(f"🧠 KB_DOCS_PATH (for SoftwareArchitect): {KB_DOCS_PATH}")
    logger.info(f"💻 KB_CODE_PATH (for SoftwareArchitect): {KB_CODE_PATH}")

    # Ensure essential paths exist
    if not LEGACY_CODEBASE_PATH.is_dir():
        logger.critical(f"❌ Critical Error: Legacy codebase path not found: {LEGACY_CODEBASE_PATH}")
        sys.exit(1)
    if not GEN_DOCS_OUTPUT_PATH.is_dir():
        logger.warning(
            f"⚠️ Warning: Gen Docs output path not found: {GEN_DOCS_OUTPUT_PATH}. SoftwareArchitect may lack context.")
    if not KB_DOCS_PATH.is_dir():
        logger.warning(f"⚠️ Warning: KB Docs path not found: {KB_DOCS_PATH}. SoftwareArchitect may lack context.")
    if not KB_CODE_PATH.is_dir():
        logger.warning(f"⚠️ Warning: KB Code path not found: {KB_CODE_PATH}. This is a critical knowledge source.")
    if not PLAN_FILE_PATH.is_file():
        logger.critical(f"❌ Critical Error: Plan file not found: {PLAN_FILE_PATH}")
        sys.exit(1)

    WORKING_CODE_BASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    plan_tool = PlanTool(plan_file=str(PLAN_FILE_PATH))

    codegen_crew_instance = CodeGenCrew(
        plan_file_path=str(PLAN_FILE_PATH),
        codebase_path=str(LEGACY_CODEBASE_PATH),
        gen_docs_output_path=str(GEN_DOCS_OUTPUT_PATH),
        kb_docs_path=str(KB_DOCS_PATH),
        kb_code_path=str(KB_CODE_PATH),
        working_code_path=str(WORKING_CODE_BASE_PATH)
    )

    current_source_for_step_preparation = LEGACY_CODEBASE_PATH

    while True:
        current_step_details = plan_tool.get_next_step_to_do()
        if not current_step_details:
            logger.info("🎉 No more 'todo' steps found in the plan. Modernization complete (or plan finished)!")
            break

        step_id = current_step_details['id']
        step_name = current_step_details['name']
        step_description = current_step_details.get('description', '')
        step_notes = current_step_details.get('notes', '')

        logger.info(f"🔷 Processing Step: {step_name} (ID: {step_id})")
        if step_description:
            logger.info(f"   Description: {step_description[:150].replace(chr(10), ' ')}...")
        if step_notes:
            logger.info(f"   Previous feedback/notes for this step: {step_notes}")

        prepare_working_codebase(current_source_for_step_preparation, WORKING_CODE_BASE_PATH)

        kickoff_inputs = {
            "current_plan_step_identifier": step_id,
            "retry_feedback_notes": step_notes if step_notes and "retry with feedback" in step_notes.lower() else ""
        }

        active_crew = codegen_crew_instance.build_crew_for_step()

        logger.info(f"  🚀 Kicking off AI crew for step: {step_name}...")
        crew_result = active_crew.kickoff(inputs=kickoff_inputs)

        user_decision_string = "Error: User decision not retrieved from crew result."
        if crew_result and crew_result.tasks_output:
            for task_output_obj in reversed(crew_result.tasks_output):
                if task_output_obj.task.config.get('human_input', False):
                    user_decision_string = str(task_output_obj.exported_output).strip()
                    break
            if user_decision_string == "Error: User decision not retrieved from crew result." and crew_result.raw:
                user_decision_string = str(crew_result.raw).strip()

        logger.info(f"  🗣️ User decision processed by AI Crew (TeamLead): '{user_decision_string}'")

        if user_decision_string:
            decision_lower = user_decision_string.lower()
            if decision_lower == "approve":
                logger.info(f"  ✅ Step '{step_name}' approved. Plan updated by TeamLead.")
                current_source_for_step_preparation = Path(WORKING_CODE_BASE_PATH)
                logger.info(f"  Updated source for next step preparation: {current_source_for_step_preparation}")
                # Optional: Backup approved state
                # approved_step_dir = WORKING_CODE_BASE_PATH.parent / f"{step_id}_approved"
                # if approved_step_dir.exists(): shutil.rmtree(approved_step_dir)
                # shutil.copytree(WORKING_CODE_BASE_PATH, approved_step_dir)
                # logger.info(f"  Approved state for step {step_id} backed up to {approved_step_dir}")

            elif decision_lower == "reject":
                logger.warning(f"  ❌ Step '{step_name}' rejected. Plan updated by TeamLead. Stopping process.")
                break
            elif decision_lower.startswith("retry_with_feedback:"):
                logger.info(f"  🔄 Step '{step_name}' to be retried. Plan updated by TeamLead with feedback.")
            else:
                logger.error(
                    f"  ⚠️ Unknown decision string: '{user_decision_string}'. Assuming rejection and stopping.")
                break
        else:
            logger.error("  ⚠️ No decision string received from the crew's human validation task. Stopping.")
            break

    logger.info("✅ Code Generation Process Finished.")


if __name__ == "__main__":
    main()