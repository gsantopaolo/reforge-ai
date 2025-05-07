#!/usr/bin/env python3
# src/main.py

import sys, os, shutil, subprocess, json
from documentation_crew import DocumentationCrew

def prepare_codebase(target: str) -> str:
    if target.startswith("http"):
        tmp = "./temp_codebase"
        if os.path.exists(tmp): shutil.rmtree(tmp)
        r = subprocess.run(["git","clone","--depth","1",target,tmp],
                            capture_output=True, text=True)
        if r.returncode!=0:
            print("❌ Git clone failed:", r.stderr); sys.exit(1)
        code_path = tmp
    else:
        code_path = target

    if not os.path.isdir(code_path):
        print(f"📁 Directory `{code_path}` not found."); sys.exit(1)

    # optional compile
    if os.path.exists(os.path.join(code_path,"pom.xml")):
        subprocess.run(["mvn","-f",os.path.join(code_path,"pom.xml"),"clean","compile"], check=False)
    elif os.path.exists(os.path.join(code_path,"build.gradle")):
        subprocess.run(["gradle","-p",code_path,"build"], check=False)
    else:
        print("ℹ️  No build file found; skipping compile.")

    return os.path.abspath(code_path)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python3 main.py <codebase_or_git_url>"); sys.exit(0)
    codebase_path = prepare_codebase(sys.argv[1])
    os.environ["CODE_PATH"] = codebase_path

    docs_dir = "1-documentation/docs"
    state_dir= "1-documentation/state"
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(state_dir, exist_ok=True)

    print(f"code base: {codebase_path}")
    print(f"docs dir: {docs_dir}")
    print(f"codbase: {os.path.basename(codebase_path)}")

    crew = DocumentationCrew(codebase_path, docs_dir).crew()
    state = crew.kickoff({
        "codebase": os.path.basename(codebase_path),
        "code_path": codebase_path,
        "doc_path": os.path.abspath(docs_dir)
    })

    out_file = os.path.join(state_dir, "documentation_state.json")
    with open(out_file,"w") as f:
        json.dump(state.model_dump() if hasattr(state,"model_dump") else dict(state), f, indent=2)

    print(f"✅ Done. Docs in `{docs_dir}`, state in `{state_dir}`.")
