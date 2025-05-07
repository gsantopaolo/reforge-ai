from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class LLMDebuggerInput(BaseModel):
    error_log: str = Field(..., description="Compiler or test failure logs.")

class LLMDebuggerTool(BaseTool):
    name: str = "LLMDebuggerTool"
    description: str = "Proposes code fixes for errors by querying an LLM with logs."
    args_schema: Type[BaseModel] = LLMDebuggerInput

    def _run(self, error_log: str) -> str:
        # TODO: Send errors to LLM, parse suggested fix diff
        return ""  # stub: return diff for fix
