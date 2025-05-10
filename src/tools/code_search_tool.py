# tools/code_search_tool.py
from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


def _get_keywords(query: str) -> List[str]:
    return [kw.strip().lower() for kw in query.split() if kw.strip()]


class CodeSearchToolInput(BaseModel):
    query: str = Field(..., description="The natural language query or keywords to search for.")
    target_knowledge_bases: Optional[List[str]] = Field(
        None,
        description="Specify which KBs to search. Valid options: 'kb-code', 'kb-docs', '1-documentation/docs'. Searches all configured KBs if None."
    )
    max_results_per_kb: Optional[int] = Field(3,
                                              description="Maximum number of matching file snippets to return per knowledge base.")
    context_lines: Optional[int] = Field(2,
                                         description="Number of lines before and after the match to include as context.")


class CodeSearchTool(BaseTool):
    name: str = "CodeSearchTool"  # CHANGED TO MATCH YOUR YAML if it uses "CodeSearchTool"
    # OR "KnowledgeBaseSearchTool" if your YAML uses that.
    # MAKE SURE THIS MATCHES agents.yaml
    description: str = (
        "Searches for a query within specified knowledge bases (kb-code, kb-docs). "
        "Returns relevant snippets from files containing the query terms."
    )
    args_schema: Type[BaseModel] = CodeSearchToolInput

    _kb_paths_internal: Dict[str, Path]  # Internal instance attribute

    def __init__(self,
                 kb_code_path: str,
                 kb_docs_path: str,
                 gen_docs_path: str,
                 **kwargs: Any):
        super().__init__(**kwargs)

        self._kb_paths_internal = {
            "kb-code": Path(kb_code_path).resolve(),
            "kb-docs": Path(kb_docs_path).resolve(),
            "1-documentation/docs": Path(gen_docs_path).resolve()
        }
        for name, path_val in self._kb_paths_internal.items():
            if not path_val.is_dir():
                logger.warning(
                    f"CodeSearchTool: Knowledge base path for '{name}' not found or not a directory: {path_val}")

    def _search_in_file(self, file_path: Path, keywords: List[str], context_lines: int) -> List[str]:
        found_snippets = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line_content in enumerate(lines):
                line_lower = line_content.lower()
                if all(keyword in line_lower for keyword in keywords):
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    snippet_lines = []
                    for idx, l_content in enumerate(lines[start:end]):
                        actual_line_num_in_file = start + idx + 1
                        prefix = "> " if (start + idx) == i else "  "
                        snippet_lines.append(f"{prefix}L{actual_line_num_in_file}: {l_content.rstrip()}")

                    snippet = "\n".join(snippet_lines)
                    found_snippets.append(snippet)
        except Exception:
            pass
        return found_snippets

    def _run(self, query: str, target_knowledge_bases: Optional[List[str]] = None, max_results_per_kb: int = 3,
             context_lines: int = 2) -> str:
        keywords = _get_keywords(query)
        if not keywords:
            return "Error: No keywords provided in the query."

        results_str = f"Search Results for query: '{query}' (keywords: {', '.join(keywords)})\n"
        found_any = False

        kbs_to_search_names = []
        if target_knowledge_bases:
            for kb_name in target_knowledge_bases:
                if kb_name in self._kb_paths_internal:
                    kbs_to_search_names.append(kb_name)
                else:
                    results_str += f"\nWarning: Unknown target knowledge base '{kb_name}'. Configured: {list(self._kb_paths_internal.keys())}. Skipping.\n"
        else:
            kbs_to_search_names = list(self._kb_paths_internal.keys())

        for kb_name in kbs_to_search_names:
            kb_path = self._kb_paths_internal.get(kb_name)
            if not kb_path or not kb_path.is_dir():
                results_str += f"\nSkipping knowledge base '{kb_name}': Path not configured or not found ({kb_path}).\n"
                continue

            results_str += f"\n--- Results from {kb_name} ({kb_path.name}) ---\n"
            kb_found_count = 0

            for file_path in kb_path.rglob('*'):
                if file_path.is_file():
                    snippets_in_file = self._search_in_file(file_path, keywords, context_lines)
                    if snippets_in_file:
                        if kb_found_count >= max_results_per_kb:
                            results_str += f"  (Reached max results for {kb_name}, more might exist in other files)\n"
                            break
                        try:
                            display_path = file_path.relative_to(self._kb_paths_internal[kb_name])
                        except ValueError:
                            display_path = file_path.name
                        results_str += f"\n  In File: {display_path}:\n"
                        for snippet_idx, snippet in enumerate(snippets_in_file):
                            if kb_found_count >= max_results_per_kb:
                                results_str += f"    (Reached max results for {kb_name}, more snippets in this file not shown)\n"
                                break
                            results_str += snippet + "\n---\n"
                            kb_found_count += 1
                            found_any = True
                        if kb_found_count >= max_results_per_kb:
                            break

            if kb_found_count == 0:
                results_str += "  No matches found in this knowledge base.\n"

        if not found_any:
            results_str += "\nOverall: No relevant information found for the query across specified knowledge bases."

        return results_str.strip()