# crewai_tools/diagram_generator.py

import os
import subprocess
from pathlib import Path
from typing import Optional, Type, Dict

from pydantic import BaseModel, Field
from crewai.tools.base_tool import BaseTool

class DiagramGeneratorInput(BaseModel):
    puml_path: Optional[str] = Field(
        None,
        description="Path to a .puml file or directory containing .puml files."
    )
    output_format: str = Field(
        "svg",
        description="Desired output format for PlantUML diagrams (e.g., svg, png)."
    )

class DiagramGeneratorTool(BaseTool):
    name: str = "diagram_generator"
    description: str = "Render PlantUML (.puml) files into diagrams via the PlantUML CLI."
    args_schema: Type[DiagramGeneratorInput] = DiagramGeneratorInput

    def _run(
        self,
        puml_path: Optional[str] = None,
        output_format: str = "svg"
    ) -> Dict:
        # Determine the source path (file or directory)
        path = Path(puml_path or os.getcwd()).resolve()
        outputs = []

        # Collect all .puml files
        puml_files = [path] if path.is_file() and path.suffix == ".puml" else list(path.rglob("*.puml"))

        for file in puml_files:
            out_dir = file.parent
            cmd = [
                "plantuml",
                f"-t{output_format}",
                "-o",
                str(out_dir),
                str(file)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"PlantUML failed on {file}:\n{result.stderr.strip()}")
            outputs.append(str(out_dir / f"{file.stem}.{output_format}"))

        return {"diagrams": outputs}
