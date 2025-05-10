# src/gen_code.py
# !/usr/bin/env python3
import sys, os, shutil, subprocess, json
from langtrace_python_sdk import langtrace

langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))

import sys
import os
import shutil
import json
from pathlib import Path
import logging
import argparse

from crews.code_gen.code_gen_crew import CodeGenCrew
from tools.plan_tool import PlanTool

# --- Setup Logger ---
logger = logging.getLogger("reforge_ai.gen_code")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_CODEBASE_NAME = "kitchensink"
PLAN_FILE_CONSTANT_NAME = "7-PlanPhasedModuleExtraction.yaml"


# --- Main Function ---
def main():
    parser = argparse.ArgumentParser(description="ReforgeAI Code Generation: Processes a single modernization step.")
    parser.add_argument(
        "codebase_name",
        nargs="?",
        default=os.getenv("CODEBASE_NAME", DEFAULT_CODEBASE_NAME),
        help=f"The name of the codebase to process. Defaults to '{DEFAULT_CODEBASE_NAME}' or the CODEBASE_NAME environment variable."
    )
    args = parser.parse_args()
    codebase_name_to_use = args.codebase_name

    # --- Path Configuration ---
    legacy_codebase_path = Path(os.getenv("LEGACY_CODEBASE_PATH",
                                          BASE_PROJECT_ROOT / "temp" / "1-codgen-work" / codebase_name_to_use))
    working_code_base_path = Path(
        os.getenv("WORKING_CODE_BASE_PATH", SCRIPT_DIR / "1-codegen-work" / codebase_name_to_use))
    gen_docs_output_path = Path(os.getenv("GEN_DOCS_OUTPUT_PATH", SCRIPT_DIR / "1-documentation" / "docs"))
    kb_docs_path = Path(os.getenv("KB_DOCS_PATH", BASE_PROJECT_ROOT / "temp/1-documentation/kb-docs"))
    kb_code_path = Path(os.getenv("KB_CODE_PATH", BASE_PROJECT_ROOT / "temp/1-documentation/kb-code"))
    plan_file_name = os.getenv("PLAN_FILE_NAME", PLAN_FILE_CONSTANT_NAME)
    plan_file_path = gen_docs_output_path / plan_file_name
    state_output_dir = SCRIPT_DIR / "2-refactoring" / "state"
    state_output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("🚀 Starting Code Generation Process (Single Step Execution)...")
    # ... (logging of paths and LLM info as before) ...
    logger.info(f"Target Codebase: {codebase_name_to_use}")
    llm_provider_log = os.getenv("LLM_PROVIDER", "openai").upper()
    _default_models_for_log = {"openai": "gpt-4-turbo-preview", "anthropic": "claude-3-sonnet-20240229",
                               "gemini": "gemini-1.5-pro-latest"}
    model_name_log = os.getenv("MODEL_NAME", _default_models_for_log.get(llm_provider_log.lower(),
                                                                         f"unknown default for {llm_provider_log.lower()}"))
    logger.info(f"🧠 GenAI Provider (from ENV): {llm_provider_log}")
    logger.info(f"🤖 Using Model (from ENV/default): {model_name_log}")
    logger.info(f"📜 Plan File Path: {plan_file_path}")
    logger.info(f"🏛️ Source Codebase for this run (from): {legacy_codebase_path}")
    logger.info(f"🛠️ Working Directory for modifications (to): {working_code_base_path}")
    logger.info(f"📚 Generated Documentation Path (context): {gen_docs_output_path}")
    logger.info(f"🧠 Knowledge Base (Docs) Path (context): {kb_docs_path}")
    logger.info(f"💻 Knowledge Base (Code) Path (context): {kb_code_path}")

    # Path validations (as before)
    critical_paths = {"Source Codebase": legacy_codebase_path, "Plan File": plan_file_path}
    for name, path_val in critical_paths.items():
        if not (path_val.is_dir() if "codebase" in name.lower() else path_val.is_file()):
            logger.critical(f"❌ Critical Error: {name} for '{codebase_name_to_use}' not found at: {path_val}")
            sys.exit(1)
    warning_paths = {"Generated Documentation": gen_docs_output_path, "KB Docs": kb_docs_path, "KB Code": kb_code_path}
    for name, path_val in warning_paths.items():
        if not path_val.is_dir(): logger.warning(
            f"⚠️ Warning: {name} path not found: {path_val}. Agents may lack full context.")

    working_code_base_path.parent.mkdir(parents=True, exist_ok=True)
    plan_tool_instance = PlanTool(plan_file=str(plan_file_path))
    initial_next_step_check = plan_tool_instance.get_next_step_to_do()

    if not initial_next_step_check:
        logger.info("🎉 No 'todo' steps found in the plan. Process has likely completed all planned steps.")
        sys.exit(0)

    step_id_for_crew = initial_next_step_check['id']
    step_name_for_crew = initial_next_step_check['name']
    step_description_for_log = initial_next_step_check.get('description', '')
    step_notes_for_crew = initial_next_step_check.get('notes', '')

    logger.info(
        f"🔷 Processing Step: {step_name_for_crew} (ID: {step_id_for_crew}) for codebase '{codebase_name_to_use}'")
    if step_description_for_log: logger.info(
        f"   Description: {step_description_for_log[:150].replace(chr(10), ' ')}...")
    if step_notes_for_crew: logger.info(f"   Notes from previous attempt/feedback: {step_notes_for_crew}")

    try:
        codegen_crew_instance = CodeGenCrew(
            plan_file_path=str(plan_file_path),
            codebase_path=str(legacy_codebase_path),
            gen_docs_output_path=str(gen_docs_output_path),
            kb_docs_path=str(kb_docs_path),
            kb_code_path=str(kb_code_path),
            working_code_path=str(working_code_base_path)
        )
    except RuntimeError as e:
        logger.critical(f"❌ Failed to initialize CodeGenCrew: {e}.")
        sys.exit(1)

    prepare_working_codebase(legacy_codebase_path, working_code_base_path)

    kickoff_inputs = {
        "current_plan_step_identifier": step_id_for_crew,
        "retry_feedback_notes": step_notes_for_crew if step_notes_for_crew and "retry with feedback" in step_notes_for_crew.lower() else "",

        # Default/initial values for placeholders expected by task descriptions
        "create_modernization_step_brief_task": "Modernization brief is being prepared by the Software Architect.",

        "implement_code_changes_task": {
            "diff": "Code changes are being implemented by the Principal Software Engineer.",
            "changed_files_path": str(working_code_base_path)
        },
        "compile_modernized_code_task": {
            "modernized_status": "Compilation pending.",
            "modernized_logs": "No compilation logs yet.",
            "legacy_status": "N/A",
            "legacy_logs": "N/A"
        },
        "legacy_code_path_for_this_step": str(legacy_codebase_path),
        "working_code_path_for_this_step": str(working_code_base_path),
    }

    active_crew = codegen_crew_instance.build_crew_for_step()
    logger.info(f"  🚀 Kicking off AI crew for step: '{step_name_for_crew}' on codebase '{codebase_name_to_use}'...")
    crew_final_state = active_crew.kickoff(inputs=kickoff_inputs)

    logger.info(f"  🏁 Crew execution finished for step '{step_name_for_crew}'.")

    # ... (rest of state saving and final logging as before, no changes needed there) ...
    final_crew_output_summary = "No direct raw output from crew."
    if crew_final_state:
        if hasattr(crew_final_state, 'raw') and crew_final_state.raw:
            final_crew_output_summary = str(crew_final_state.raw).strip()
            logger.info(f"  📝 Final raw output from crew (likely human's decision): {final_crew_output_summary}")
        state_file_name = f"codegen_step_{step_id_for_crew}_{codebase_name_to_use}_state.json"
        state_file_path = state_output_dir / state_file_name
        try:
            dumpable_state = {}
            if hasattr(crew_final_state, 'model_dump'):
                dumpable_state = crew_final_state.model_dump()
            elif isinstance(crew_final_state, dict):
                dumpable_state = crew_final_state
            elif hasattr(crew_final_state, '__dict__'):
                dumpable_state = crew_final_state.__dict__
            else:
                dumpable_state = {"final_output": str(crew_final_state)}
            with open(state_file_path, "w", encoding='utf-8') as f:
                json.dump(dumpable_state, f, indent=2, default=str)
            logger.info(f"  💾 Crew execution state saved to: {state_file_path}")
        except Exception as e:
            logger.error(f"  ⚠️ Could not save crew execution state: {e}")
            logger.debug(f"  Raw crew_final_state that failed to serialize was: {crew_final_state}")
    logger.info("✅ Code Generation Process (Single Step Execution) Finished.")
    logger.info(f"  ▶️ Next Steps for Human Operator:")
    logger.info(f"  1. Review the updated plan file: {plan_file_path}")
    logger.info(f"  2. Inspect the generated/modified code in: {working_code_base_path}")
    logger.info(f"  3. Based on the plan file's updated step status (set by the agent during human validation):")
    logger.info(f"     - If step was 'approved':")
    logger.info(f"       - Commit changes from '{working_code_base_path}' to version control.")
    logger.info(
        f"       - Update the source for the next run (e.g., by making '{working_code_base_path}' the new baseline for '{legacy_codebase_path.name}').")
    logger.info(f"     - If step was 'rejected' or marked for 'retry':")
    logger.info(
        f"       - The plan file reflects this. The working directory '{working_code_base_path}' contains the last attempt.")
    logger.info(
        f"  4. To process the next step (or retry), run this script again after making necessary manual preparations and plan file reviews.")


# --- Helper Function Definition ---
def prepare_working_codebase(source_path: Path, target_path: Path):
    # ... (as before) ...
    if not source_path.is_dir():
        logger.error(f"❌ Source path for codebase copy does not exist or is not a directory: {source_path}")
        raise FileNotFoundError(f"Source path for codebase copy not found: {source_path}")
    if target_path.exists():
        logger.info(f"🧹 Cleaning up existing working directory: {target_path}")
        shutil.rmtree(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"📂 Copying codebase from {source_path} to working directory {target_path}")
    shutil.copytree(source_path, target_path)


if __name__ == "__main__":
    main()