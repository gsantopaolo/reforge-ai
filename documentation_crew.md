**Clarifying documentation task**

The user seems to be asking for a comprehensive documentation focused on the first part of a migration involving defining crews, tasks, and tools. Their reference indicates a YAML configuration or code for agents and tasks. Since they mentioned documentation and previously worked with agents.yaml and tasks.yaml, I'll need to focus on providing documentational tools while considering if the tasks are sequential or hierarchical, based on the crewai Process. I'll clarify whether YAML files or specific code examples are needed.


**Searching CrewAI documentation**

I need to search for how tasks and tools should be defined in the CrewAI documentation. I'll specifically look up "tasks" and "creating custom tools" on docs.crewai.com. Once I find relevant information, I'll generate agents.yaml and tasks.yaml for the documentation phase, keeping in mind the need for at least 10 citations. I’ll also use markdown formatting, including summaries and appropriate headings, to organize the content clearly and cite each key statement. Time is tight, but I’ll aim for accuracy while approximating where necessary!


Thought for 15 seconds


## Summary

We’ll stand up an initial **CrewAI Crew** dedicated solely to creating a full, comprehensive documentation of the legacy Java 10 banking system—before any code migration begins. The crew will consist of specialized agents (Project Manager, Codebase Analyst, Documentation Specialist, Reviewer) working in a **sequential** workflow, since each documentation phase builds on the previous one (inventory → analysis → writing → review) . We’ll provision a set of **custom tools** (e.g. StaticAnalyzerTool, DiagramGeneratorTool) so agents can introspect code, extract schemas, and produce diagrams without writing implementations now—just naming and describing their function ([docs.crewai.com][1]). Each **task** is bound to exactly one responsible agent, and every task also designates a reviewer agent to enforce quality and request refinements, mirroring peer-review best practices in software documentation .

---

## 1. Crew Definition

We’ll create a single Crew, named **DocumentationCrew**, with a **sequential** process (tasks run one after another) to guarantee that module docs only start once the inventory and analysis are complete . The crew comprises the following agents:

| Agent ID                     | Role                           | Goal                                                                                                                   | Tools                                    | LLM Usage                  |
| ---------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------- |
| **project\_manager\_agent**  | Project Manager & Orchestrator | Kick off the documentation initiative, scaffold the knowledge base, prioritize modules, and sequence tasks.            | KnowledgeBaseTool, SchedulingTool        | Minimal (status summaries) |
| **codebase\_analyst\_agent** | Codebase Analyst               | Perform inventory and static code analysis: map modules, dependencies, detect Java 10-specific constructs to document. | StaticAnalyzerTool, DependencyMapperTool | None                       |
| **documentation\_agent**     | Documentation Specialist       | Generate Javadoc enhancements, module overviews, data-model docs, SQL/SP summaries, and architecture narratives.       | CodeParserTool, RetrievalTool            | High (GPT-4)               |
| **reviewer\_agent**          | Quality Reviewer & Critic      | Audit all outputs—reports, diagrams, prose—for accuracy, completeness, and clarity; request refinements as needed.     | DiffAnalyzerTool, LLMDiagnosticTool      | Moderate (critique)        |

*Crew composition follows the CrewAI “specialized agent” pattern: each agent has a clear role, goal, and restricted toolset to ensure predictable collaboration* .

---

## 2. Tools Catalog

Below are the **custom tools** we’ll declare (implementation TBD). Agents will invoke these to inspect the codebase and generate artifacts:

| Tool Name                 | Description                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **StaticAnalyzerTool**    | Scans Java source for deprecated APIs, code smells, and constructs removed in Java 11–21.                                    |
| **DependencyMapperTool**  | Reads Maven/Gradle metadata to list all external libraries, versions, and inter-module dependencies.                         |
| **CodeParserTool**        | Parses Java ASTs to extract class/method signatures, call graphs, and package hierarchies.                                   |
| **DiagramGeneratorTool**  | Renders UML diagrams (class, package, sequence) from AST or metadata to visualize architecture.                              |
| **DBSchemaExtractorTool** | Connects to the database or reads SQL files to output ER diagrams, table schemas, and stored procedure catalogs.             |
| **RiskAssessmentTool**    | Cross-references inventory data against known Java 21 deprecations and regulatory checklists (e.g. PCI, GDPR) to flag risks. |
| **KnowledgeBaseTool**     | Reads/writes to a markdown/wiki repository for storing generated docs and metadata.                                          |
| **RetrievalTool**         | Performs semantic lookup over existing docs or code using embeddings to provide context during writing.                      |
| **DiffAnalyzerTool**      | Compares two versions of a document or code diff to highlight inconsistencies or missing updates.                            |
| **LLMDiagnosticTool**     | Uses an LLM to critique prose or diagram captions for clarity, correctness, and completeness.                                |

*Defining custom tools via `BaseTool` subclasses is standard practice in CrewAI; this ensures agents can call them by name and adhere to a shared API contract* ([docs.crewai.com][1]).

---

## 3. Task Breakdown

We’ll sequence the following tasks under **Process.sequential**, each with a designated owner and reviewer:

| Task ID                       | Description                                                                                                                                            | Responsible Agent        | Reviewer Agent          | Tools                                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ | ----------------------- | ------------------------------------------------ |
| **initialize\_kb**            | Scaffold the documentation repository/wiki: create top-level sections for architecture, modules, data model, SQL/SP, and risk registers.               | project\_manager\_agent  | reviewer\_agent         | KnowledgeBaseTool, SchedulingTool                |
| **inventory\_codebase**       | Traverse the code repository to catalog all packages, modules, and external dependencies; tag high-impact modules by size/commit history.              | codebase\_analyst\_agent | reviewer\_agent         | StaticAnalyzerTool, DependencyMapperTool         |
| **extract\_architecture**     | Generate an overall system architecture diagram and narrative: show module interactions, deployment topology, and data flows.                          | codebase\_analyst\_agent | reviewer\_agent         | DiagramGeneratorTool, CodeParserTool             |
| **extract\_data\_model**      | Produce ER diagrams and table schemas for all database objects, and document core stored procedures and triggers.                                      | codebase\_analyst\_agent | reviewer\_agent         | DBSchemaExtractorTool, DiagramGeneratorTool      |
| **generate\_module\_docs**    | For each key module, auto-generate Javadoc comments, class/method summaries, and a human-readable module overview.                                     | documentation\_agent     | reviewer\_agent         | CodeParserTool, RetrievalTool, LLMDiagnosticTool |
| **generate\_sql\_sp\_docs**   | Summarize each stored procedure: inputs, outputs, business purpose, and performance considerations in plain English.                                   | documentation\_agent     | reviewer\_agent         | DBSchemaExtractorTool, LLMDiagnosticTool         |
| **compile\_risk\_report**     | Cross-reference deprecated API findings and schema changes to create a **Migration Risk Analysis** document with mitigation recommendations.           | documentation\_agent     | reviewer\_agent         | RiskAssessmentTool, StaticAnalyzerTool           |
| **review\_and\_refine\_docs** | Perform a holistic review of all generated artifacts, normalize formatting, ensure cross-references are correct, and finalize style consistency.       | reviewer\_agent          | project\_manager\_agent | DiffAnalyzerTool, LLMDiagnosticTool              |
| **finalize\_doc\_handbook**   | Publish the consolidated **Documentation Handbook** (PDF/markdown site), complete with TOC, versioning info, and handoff notes for the migration team. | project\_manager\_agent  | reviewer\_agent         | KnowledgeBaseTool                                |

All tasks proceed in strict order—no document is created until its inputs exist—maximizing clarity and traceability . Each task’s **reviewer** provides immediate feedback; if the responsible agent’s output falls short, the reviewer will request a rerun or refinement, ensuring the final documentation meets high professional standards (akin to human technical reviews) .

---

With this crew, task list, and tool catalog in place, you can implement `agents.yaml`, `tasks.yaml`, and the corresponding `crew.py`/`main.py` to spin up your **DocumentationCrew** in CrewAI, ready to autonomously generate the exhaustive documentation you need before any code migration begins.

[1]: https://docs.crewai.com/how-to/create-custom-tools "Create Custom Tools - CrewAI"
