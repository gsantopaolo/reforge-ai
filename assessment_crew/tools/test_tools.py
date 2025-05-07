#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

from jdeps_tool import JDepsTool

def resolve_base_path(arg_path: str = None) -> str:
    """
    Determine which path to pass into JDepsTool:
      1) --base-path argument
      2) CODE_PATH env var
      3) fallback to the temp_codebase folder next to this repo
    """
    # 1) explicit CLI override
    if arg_path:
        return arg_path

    # 2) env override
    env = os.getenv("CODE_PATH")
    if env:
        return env

    # 3) repo-local default
    #   <repo-root>/src/assessment_crew/temp_codebase
    repo_root = Path(__file__).parent.parent
    default = repo_root / "temp_codebase"
    if default.exists():
        return str(default)

    print(
        f"Error: no --base-path, no $CODE_PATH, "
        f"and fallback folder not found at {default}",
        file=sys.stderr
    )
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Test runner for JDepsTool"
    )
    parser.add_argument(
        "-p", "--base-path",
        help="Path to compiled classes or JAR (fallback: $CODE_PATH then temp_codebase/)"
    )
    parser.add_argument(
        "-i", "--jdk-internals",
        action="store_true",
        help="Include JDK internal API usage"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recurse into subpackages (-R)"
    )
    parser.set_defaults(jdk_internals=False, recursive=True)

    args = parser.parse_args()

    base_path = resolve_base_path(args.base_path)
    print(f"Using base_path = {base_path}")
    print(f"Using jdk_internals = {args.jdk_internals}")
    print(f"Using recursive = {args.recursive}")

    # instantiate & call
    tool = JDepsTool(base_path=base_path, java_home=os.getenv("JAVA_HOME"))
    try:
        result = tool._run()
    except Exception as e:
        print(f"Error running JDepsTool: {e}", file=sys.stderr)
        sys.exit(1)

    # print results
    print("\n=== Raw jdeps output ===")
    print(result["jdeps_output"])
    print("\n=== Identified internal-API issues ===")
    for issue in result["identified_issues"]:
        print(issue)
    if not result["identified_issues"]:
        print("None found.")


if __name__ == "__main__":
    main()
