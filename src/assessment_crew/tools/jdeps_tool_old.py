# # src/assessment_crew/tools/jdeps_tool.py
#
# import os
# import subprocess
# from pathlib import Path
# from typing import Optional, Type, List
#
# from pydantic import BaseModel, Field, PrivateAttr
# from crewai.tools.base_tool import BaseTool
#
# # Common Java build output candidates (relative to any root)
# BUILD_OUTPUT_CANDIDATES = [
#     "build/classes/java/main",  # Gradle default
#     "target/classes",  # Maven default
# ]
#
#
# def resolve_target_path(base_path: Optional[str] = None) -> str:
#     """
#     Resolve where the .class files (or JAR) live, even if buried under subfolders:
#       1) If base_path is a JAR, use it.
#       2) If base_path is a folder, scan recursively for any of the BUILD_OUTPUT_CANDIDATES.
#       3) If none found, error.
#     """
#     if not base_path:
#         raise RuntimeError("No base_path provided and no CODE_PATH override.")
#
#     root = Path(base_path)
#
#     # 1) direct jar?
#     if root.is_file() and root.suffix == ".jar":
#         return str(root)
#
#     # 2) recursively search for any build output folder
#     for candidate in BUILD_OUTPUT_CANDIDATES:
#         # e.g. root/**/target/classes
#         for path in root.rglob(candidate):
#             if path.is_dir():
#                 return str(path)
#
#     # 3) as a last resort, if there are any .class files under root, use root itself
#     if any(root.rglob("*.class")):
#         return str(root)
#
#     # nothing worked
#     raise RuntimeError(
#         f"Could not locate any of {BUILD_OUTPUT_CANDIDATES} under {root}. "
#         "Did you compile your code? Please build first or point --base-path at the class output."
#     )
#
#
# class JDepsInput(BaseModel):
#     base_path: Optional[str] = Field(
#         None,
#         description=(
#             "Filesystem path to compiled class files or JAR. "
#             "If omitted, will scan standard output dirs or CODE_PATH"
#         )
#     )
#     jdk_internals: bool = Field(True, description="Include JDK internals")
#     recursive: bool = Field(True, description="Recurse into subpackages")
#
#
# class JDepsTool(BaseTool):
#     name: str = "jdeps"
#     description: str = "Analyze Java dependencies via jdeps"
#     args_schema: Type[JDepsInput] = JDepsInput
#
#     _jdeps_cmd: str = PrivateAttr()
#
#     def __init__(self, java_home: Optional[str] = None):
#         super().__init__()
#         self._jdeps_cmd = os.path.join(java_home, "bin", "jdeps") if java_home else "jdeps"
#
#
#     # todo: read this for more possible usages of jdeps https://chatgpt.com/share/681a0107-9954-8005-aedc-3abd90f6ade6
#     def _run(self, *, base_path: Optional[str], jdk_internals: bool, recursive: bool) -> dict:
#         import os, subprocess
#         from pathlib import Path
#
#         # 1) Resolve root_dir, treating non-existent/relative base_path as under CODE_PATH
#         if base_path:
#             candidate = Path(base_path)
#             if not candidate.exists() and not candidate.is_absolute():
#                 env_root = os.getenv("CODE_PATH")
#                 if env_root and Path(env_root, base_path).exists():
#                     root_dir = Path(env_root, base_path)
#                 else:
#                     root_dir = candidate
#             else:
#                 root_dir = candidate
#         else:
#             root_dir = Path(os.getenv("CODE_PATH") or os.getcwd())
#
#         # 2) If it's a JAR, use it; otherwise find the closest build output
#         if root_dir.is_file() and root_dir.suffix == ".jar":
#             target = root_dir
#         else:
#             candidates = list(root_dir.rglob("target/classes")) \
#                          + list(root_dir.rglob("build/classes/java/main"))
#             if candidates:
#                 target = min(candidates, key=lambda p: len(p.parts))
#             elif any(root_dir.rglob("*.class")):
#                 target = root_dir
#             else:
#                 raise RuntimeError(
#                     f"Could not locate any of ['build/classes/java/main','target/classes'] under {root_dir}. "
#                     "Did you compile your code? Please build first or point --base-path at the class output."
#                 )
#
#         # 3) Build and run jdeps (no -s flag, to get full detail)
#         cmd = [self._jdeps_cmd] + (["--jdk-internals"] if jdk_internals else [])
#         if recursive:
#             cmd.append("-R")
#         cmd.append(str(target))
#
#         result = subprocess.run(cmd, capture_output=True, text=True)
#         if result.returncode != 0:
#             raise RuntimeError(f"jdeps failed (exit {result.returncode}): {result.stderr.strip()}")
#
#         # 4) Capture “not found” and internal-API warnings
#         output = result.stdout
#         issues = [
#             line.strip()
#             for line in output.splitlines()
#             if "not found" in line
#                or "JDK internal API" in line
#                or line.startswith("jdeps:")
#         ]
#
#         return {"jdeps_output": output, "identified_issues": issues}
