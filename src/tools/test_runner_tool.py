from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class TestRunnerInput(BaseModel):
    code_path: str = Field(..., description="Path to project root for running tests.")

class TestRunnerTool(BaseTool):
    name: str = "TestRunnerTool"
    description: str = "Runs unit and integration tests, returning a summary report."
    args_schema: Type[BaseModel] = TestRunnerInput

    def _run(self, code_path: str) -> dict:
        # TODO: Execute 'mvn test' or 'gradle test', parse results into JSON
        return {}  # stub: empty report
