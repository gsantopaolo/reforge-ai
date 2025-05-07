# src/gen_code.py
#!/usr/bin/env python3
import sys, os, shutil, subprocess, json
from langtrace_python_sdk import langtrace

# Initialize tracing (requires LANGTRACE_API_KEY)
langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))

from crews.code_gen.code_gen_crew import CodeGenCrew


def prepare_codebase(target: str) -> str:
    """
    Clone or validate the provided codebase path or Git URL.
    Returns absolute path to the codebase directory.
    """
    if target.startswith("http"):
        tmp = "./temp_codebase"
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
        r = subprocess.run(["git", "clone", "--depth", "1", target, tmp],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("❌ Git clone failed:", r.stderr)
            sys.exit(1)
        code_path = tmp
    else:
        code_path = target

    if not os.path.isdir(code_path):
        print(f"📁 Directory `{code_path}` not found.")
        sys.exit(1)

    # Optional compile step
    if os.path.exists(os.path.join(code_path, "pom.xml")):
        subprocess.run(["mvn", "-f", os.path.join(code_path, "pom.xml"), "clean", "compile"], check=False)
    elif os.path.exists(os.path.join(code_path, "build.gradle")):
        subprocess.run(["gradle", "-p", code_path, "build"], check=False)
    else:
        print("ℹ️  No build file found; skipping compile.")

    return os.path.abspath(code_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gen_code.py <codebase_or_git_url>")
        sys.exit(0)

    codebase_path = prepare_codebase(sys.argv[1])
    os.environ["CODE_PATH"] = codebase_path

    # Directories for refactoring outputs and state
    output_dir = "2-refactoring/output"
    state_dir = "2-refactoring/state"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(state_dir, exist_ok=True)

    # Knowledge base directory
    kb_dir = "kb"

    print(f"codebase: {codebase_path}")
    print(f"output dir: {output_dir}")
    print(f"kb dir: {os.path.abspath(kb_dir)}")

    # Instantiate and run the RefactoringCrew
    crew = CodeGenCrew(codebase_path, output_dir, kb_dir).crew()
    state = crew.kickoff({
        "codebase": os.path.basename(codebase_path),
        "code_path": codebase_path,
        "output_path": os.path.abspath(output_dir),
        "kb_path": os.path.basename(kb_dir)
    })

    # Persist state to JSON
    out_file = os.path.join(state_dir, "refactoring_state.json")
    with open(out_file, "w") as f:
        json.dump(state.model_dump() if hasattr(state, "model_dump") else dict(state), f, indent=2)

    print(f"✅ Refactoring complete. Output in `{output_dir}`, state in `{state_dir}`.")
