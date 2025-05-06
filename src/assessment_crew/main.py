# src/assessment_crew/main.py

#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
import json

from crew import AssessmentCrew

def prepare_codebase(target: str) -> str:
    """
    Prepare the codebase for analysis.
    If the target is a GitHub URL, clone it to a temp directory.
    If it's a local path, ensure it's accessible.
    Also, attempt to compile the code (e.g., via Maven) so that bytecode analysis can run.
    Returns the filesystem path to the codebase source.
    """
    if target.startswith("http"):
        temp_dir = "./temp_codebase"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", target, temp_dir],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Git clone failed:", result.stderr)
            sys.exit(1)
        code_path = temp_dir
    else:
        code_path = target

    # Compile with Maven or Gradle if possible
    if os.path.exists(os.path.join(code_path, "pom.xml")):
        subprocess.run(
            ["mvn", "-f", os.path.join(code_path, "pom.xml"), "clean", "compile"]
        )
    elif any(fname.endswith(".gradle") for fname in os.listdir(code_path)):
        subprocess.run(
            ["gradle", "-p", code_path, "build"]
        )
    else:
        print("No Maven/Gradle build file found. Skipping compilation.")

    return code_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/assessment_crew/main.py <codebase_path_or_git_url>")
        sys.exit(0)

    target = sys.argv[1]
    codebase_path = prepare_codebase(target)

    # Ensure output directories exist
    os.makedirs("1-assessment/docs", exist_ok=True)
    os.makedirs("1-assessment/state", exist_ok=True)

    # Build the crew (no args here—crew() is memoized and takes no parameters)
    crew_instance = AssessmentCrew().crew()

    # Kick off the crew: pass a single positional dict containing ALL context
    kickoff_inputs = {
        "codebase": os.path.basename(codebase_path),
        "code_path": codebase_path
    }
    result_state = crew_instance.kickoff(kickoff_inputs)  # TypeError if you use keywords :contentReference[oaicite:0]{index=0}

    # Save the final state to JSON
    output_file = "1-assessment/state/assessment_state.json"
    state_dict = (
        result_state.model_dump()
        if hasattr(result_state, "model_dump")
        else dict(result_state)
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(state_dict, f, indent=2)

    print("Assessment completed. Results saved in 1-assessment/ directory.")