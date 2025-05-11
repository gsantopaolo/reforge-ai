import os
import subprocess
import json
from langtrace_python_sdk import langtrace

# Initialize LangTrace
langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))

from sympy.codegen.ast import Raise
from crews.gen_modern.gen_modern_crew import GenModernCrew

# Hardcoded paths
codebase_path = "/Users/gp/Developer/java-samples/reforge-ai/src/1-codegen-work/code"
state_path     = "/Users/gp/Developer/java-samples/reforge-ai/src/1-codegen-work/state"
kb_path        = "/Users/gp/Developer/java-samples/reforge-ai/src/1-codegen-work/kb"

# Validate that the provided directory exists
if not os.path.isdir(codebase_path):
    raise FileNotFoundError(f"📁 Directory '{codebase_path}' not found.")

# Optional compile step
# if os.path.exists(os.path.join(codebase_path, "pom.xml")):
#     subprocess.run([
#         "mvn", "-f", os.path.join(codebase_path, "pom.xml"), "clean", "compile"
#     ], check=False)
# elif os.path.exists(os.path.join(codebase_path, "build.gradle")):
#     subprocess.run([
#         "gradle", "-p", codebase_path, "build"
#     ], check=False)
# else:
#     print("ℹ️  No build file found; skipping compile.")

print(f"Codebase name: {os.path.basename(codebase_path)}")
print(f"KB path: {os.path.abspath(kb_path)}")

# Log which AI provider is in use
llm = os.getenv("LLM_PROVIDER", "").upper()
print(f"GenAI provider in use: {llm}")

# Run the GenModernCrew process
crew = GenModernCrew(codebase_path, kb_path).crew()
state = crew.kickoff({
    "code_path": codebase_path,
    "kb_path": os.path.basename(kb_path)
})

# Save state
out_file = os.path.join(state_path, "gen_modern_state.json")
with open(out_file, "w") as f:
    json.dump(
        state.model_dump() if hasattr(state, "model_dump") else dict(state),
        f,
        indent=2
    )

print(f"✅ Done. modernization in '{codebase_path}', state in '{state_path}'.")
