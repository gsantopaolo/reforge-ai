# tools/code_search_tool.py
from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pathlib import Path
import re


# Helper function to normalize query into keywords
def _get_keywords(query: str) -> List[str]:
    # Simple split and lowercasing. Could be more sophisticated (e.g., remove common words).
    return [kw.strip().lower() for kw in query.split() if kw.strip()]


class CodeSearchToolInput(BaseModel):
    """Input for searching code and documentation knowledge bases."""
    query: str = Field(..., description="The natural language query or keywords to search for.")
    target_knowledge_bases: Optional[List[str]] = Field(
        None,
        description="Specify which KBs to search. Valid options: 'kb_code', 'kb_docs', 'gen_docs'. Searches all configured KBs if None."
    )
    max_results_per_kb: Optional[int] = Field(3,
                                              description="Maximum number of matching file snippets to return per knowledge base.")
    context_lines: Optional[int] = Field(2,
                                         description="Number of lines before and after the match to include as context.")


class CodeSearchTool(BaseTool):
    name: str = "KnowledgeBaseSearchTool"
    description: str = (
        "Searches for a query within specified knowledge bases (kb_code, kb_docs, gen_docs). "
        "Returns relevant snippets from files containing the query terms."
    )
    args_schema: Type[BaseModel] = CodeSearchToolInput

    # Paths to the knowledge bases, configured at instantiation
    kb_paths: Dict[str, Path]

    def __init__(self,
                 kb_code_path: str,
                 kb_docs_path: str,
                 gen_docs_path: str,
                 **kwargs: Any):
        super().__init__(**kwargs)
        self.kb_paths = {
            "kb_code": Path(kb_code_path).resolve(),
            "kb_docs": Path(kb_docs_path).resolve(),
            "gen_docs": Path(gen_docs_path).resolve()
        }
        for name, path_val in self.kb_paths.items():
            if not path_val.is_dir():
                print(f"Warning: Knowledge base path for '{name}' not found or not a directory: {path_val}")
                # Or raise an error if these are critical:
                # raise FileNotFoundError(f"Knowledge base path for '{name}' not found: {path_val}")

    def _search_in_file(self, file_path: Path, keywords: List[str], context_lines: int) -> List[str]:
        """Searches for keywords in a single file and returns context snippets."""
        found_snippets = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line_content in enumerate(lines):
                line_lower = line_content.lower()
                # Check if all keywords are in the line (simple AND logic)
                # For more complex matching, consider OR or proximity.
                if all(keyword in line_lower for keyword in keywords):
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    snippet_lines = [f"  {l.rstrip()}" for l in lines[start:end]]
                    # Highlight the matching line (optional)
                    snippet_lines[i - start] = f"> {lines[i].rstrip()}"

                    snippet = f"Line {i + 1}:\n" + "\n".join(snippet_lines)
                    found_snippets.append(snippet)
        except Exception as e:
            # Silently ignore files that can't be read or specific line errors for now
            # print(f"Error reading or processing file {file_path}: {e}")
            pass
        return found_snippets

    def _run(self, query: str, target_knowledge_bases: Optional[List[str]] = None, max_results_per_kb: int = 3,
             context_lines: int = 2) -> str:
        keywords = _get_keywords(query)
        if not keywords:
            return "Error: No keywords provided in the query."

        results_str = f"Search Results for query: '{query}' (keywords: {', '.join(keywords)})\n"
        found_any = False

        kbs_to_search = []
        if target_knowledge_bases:
            for kb_name in target_knowledge_bases:
                if kb_name in self.kb_paths:
                    kbs_to_search.append(kb_name)
                else:
                    results_str += f"\nWarning: Unknown target knowledge base '{kb_name}'. Skipping."
        else:  # Search all configured KBs
            kbs_to_search = list(self.kb_paths.keys())

        for kb_name in kbs_to_search:
            kb_path = self.kb_paths.get(kb_name)
            if not kb_path or not kb_path.is_dir():
                results_str += f"\nSkipping knowledge base '{kb_name}': Path not configured or not found.\n"
                continue

            results_str += f"\n--- Results from {kb_name} ({kb_path}) ---\n"
            kb_found_count = 0

            # Iterate through files in the directory (recursive)
            # Consider limiting file types (e.g., .java, .md, .txt)
            for file_path in kb_path.rglob('*'):  # rglob for recursive
                if file_path.is_file():
                    # Add file type filtering if desired:
                    # if file_path.suffix not in ['.md', '.txt', '.java', '.xml', '.adoc']:
                    #     continue

                    snippets_in_file = self._search_in_file(file_path, keywords, context_lines)
                    if snippets_in_file:
                        if kb_found_count >= max_results_per_kb:
                            results_str += f"  (Reached max results for {kb_name}, more might exist)\n"
                            break  # Stop searching this KB

                        results_str += f"\n  In File: {file_path.relative_to(kb_path.parent)}:\n"  # Show relative path
                        for snippet in snippets_in_file:
                            results_str += snippet + "\n---\n"
                            kb_found_count += 1
                            found_any = True
                            if kb_found_count >= max_results_per_kb:
                                break
                    if kb_found_count >= max_results_per_kb:
                        break

            if kb_found_count == 0:
                results_str += "  No matches found in this knowledge base.\n"

        if not found_any:
            results_str += "\nOverall: No relevant information found for the query across specified knowledge bases."

        return results_str.strip()