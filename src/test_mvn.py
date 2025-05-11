#!/usr/bin/env python3
"""
Simple script to invoke the custom MavenBuildTool from your crewai toolset.
"""
import argparse
import sys

# Adjust the import path as needed so Python can find your tool module
# e.g., if your MavenBuildTool is in crewai/tools/maven_build.py, ensure that path is on PYTHONPATH
from tools.maven_build_tool import MavenBuildTool  # or the correct module path


def main():
    parser = argparse.ArgumentParser(
        description="Invoke the MavenBuildTool to build a project via Maven or Gradle"
    )
    parser.add_argument(
        "--base-path", "-b",
        help="Filesystem path to the Maven/Gradle project to build (overrides default)",
        default=None
    )
    args = parser.parse_args()

    tool = MavenBuildTool()

    try:
        result = tool._run(base_path=args.base_path)
    except Exception as e:
        print(f"❌ Error running build tool: {e}", file=sys.stderr)
        sys.exit(1)

    # Pretty‑print the results
    print("🔧 Tool used:", result.get("tool", "n/a"))
    print("🚀 Return code:", result.get("returncode"))
    print("=== STDOUT ===")
    print(result.get("stdout", ""))
    print("=== STDERR ===")
    print(result.get("stderr", ""))

    # Exit with the same code as Maven/Gradle
    sys.exit(result.get("returncode", 0))


if __name__ == "__main__":
    main()
