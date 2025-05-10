# Code Generation Technical Analysis

This document defines the streamlined agents, their responsibilities, the tools they use, and the overall workflow for the Java-to-Spring-Boot modernization pipeline (`gen_code`).

---

## 1. Agent & Tool Definitions

The following tools will be used by the agents: **PlanTool**, **FileSystemReadTool**, **CodeSearchTool**, **OpenRewriteTool**, **FileSystemReadWriteTool**, **LegacyCompilerTool**, and **SpringBootCompilerTool**.

### 1.1 TeamLead

**Role**: High-level orchestration and human-in-the-loop coordination.

**Goal**: Oversee the execution of each modernization step from the plan, ensure successful completion, flag issues, and solicit human validation.

**Responsibilities**:

1.  Receive the current step brief from the SoftwareArchitect.
2.  Delegate sub-tasks to worker agents: PrincipalSoftwareEngineer, BuildAndTestAgent.
3.  Track step state (“in progress”, “awaiting validation”, “completed”) by reading/updating the plan via **PlanTool**.
4.  Collate outputs (e.g., code diffs, build logs) and present a unified summary to the human user for validation.
5.  Handle human feedback:
    *   **Approve** → mark step as done in the plan (via **PlanTool**) and signal SoftwareArchitect to prepare for the next step.
    *   **Request changes** → instruct PrincipalSoftwareEngineer to iterate, providing the user's feedback.
6.  Enforce retry limits: after **N** failures from a worker (e.g., build failures), escalate to human for guidance.

**Tools Injected**:

*   **PlanTool**

---

### 1.2 SoftwareArchitect

**Role**: Context gathering, step validation, adaptive intervention, and guardian of `kb_code` wisdom.

**Goal**: Produce a comprehensive **Modernization Step Brief** for each modernization step. This brief integrates the detailed documentation from the `gen_docs` phase with the invaluable **`kb_code`** knowledge base—the definitive source of proven migration patterns, pitfalls, and solutions. Continuously monitor downstream work and intervene if code or process diverges from the brief or best practices.

**Responsibilities**:

1.  Parse and understand the current modernization step from the plan using **PlanTool**.
2.  Read and synthesize content from:
    *   All relevant documents within `1-documentation/docs` (the extremely detailed outputs from the `1-documentation/docs` phase, covering legacy system analysis, architecture, and component details).
    *   All `kb-docs/*` artifacts (for general modernization best practices and broader context).
    *   The entire `kb-code/*` directory (this is the curated set of findings, solutions, and code examples from the prior manual migration—*the migration “Bible”*).
3.  Compile these insights into a **Modernization Step Brief**. This brief must include:
    *   Clear objectives for the current plan step.
    *   Key discoveries and detailed analysis points extracted from the `1-documentation/docs` outputs relevant to the current step.
    *   Applicable best practices and patterns from `kb-docs`.
    *   **Specific code examples, warnings, workarounds, and direct guidance from `kb-code`**, with clear citations or references.
4.  Explicitly highlight where `kb-code` insights should override generic guidance or inform the interpretation of `1-documentation/docs` outputs.
5.  Provide the "Modernization Step Brief" as authoritative context to the TeamLead and, through the TeamLead, to other downstream agents.
6.  Optionally, monitor outputs from PrincipalSoftwareEngineer and BuildAndTestAgent (if delegation allows such feedback loops). If significant misalignment with the brief is detected or anticipated, the SoftwareArchitect can update the brief or provide corrective guidance to the TeamLead to re-task agents.
7.  Upon successful completion of a step (signaled by TeamLead), prepare the brief for the next pending step in the plan.

**Tools Injected**:

*   **PlanTool**
*   **FileSystemReadTool**
*   **CodeSearchTool**

---

### 1.3 PrincipalSoftwareEngineer

**Role**: Code transformation expert.

**Goal**: Generate or modify Java code to implement the modernization step according to the "Modernization Step Brief," using Java 21 and Spring Boot.

**Responsibilities**:

1.  Ingest the **Modernization Step Brief** (which includes detailed legacy analysis synthesized by the SoftwareArchitect and critical `kb_code` guidance).
2.  Apply Abstract Syntax Tree (AST)-based rewrites using **OpenRewriteTool** where applicable, guided by patterns identified in the brief (potentially derived from `kb_code`).
3.  Write new Java 21 / Spring Boot code (services, controllers, repositories, configurations, etc.) or modify existing code in a designated working directory using **FileSystemReadWriteTool**. The agent will leverage its underlying LLM and the rich context from the brief (especially `kb_code` examples) to generate accurate and idiomatic code.
4.  Ensure generated code adheres to idiomatic Spring Boot patterns, heavily referencing examples and solutions highlighted from `kb_code` in the brief.
5.  Produce a diff or patch file of the changes made for review by the TeamLead and SoftwareArchitect.

**Tools Injected**:

*   **OpenRewriteTool**
*   **FileSystemReadWriteTool**

---

### 1.4 BuildAndTestAgent

**Role**: Compile & validate legacy (if needed) and modernized code.

**Goal**: Ensure build integrity of the modified codebase.

**Responsibilities**:

1.  If specified by the plan step or brief, run the legacy compile using **LegacyCompilerTool**.
2.  Run the Spring Boot compile on the modernized code using **SpringBootCompilerTool**.
3.  Capture success/failure status and relevant logs from the compilation processes.
4.  Return these results to the TeamLead for review and decision-making.

**Tools Injected**:

*   **LegacyCompilerTool**
*   **SpringBootCompilerTool**

---

## 2. Workflow with Revised Agent Structure (with Delegation Enabled)

With `allow_delegation=True` for manager agents (TeamLead and SoftwareArchitect, if SoftwareArchitect is also set up as a manager in CrewAI), they can dynamically delegate subtasks or re-delegate tasks with new context. Worker agents like PrincipalSoftwareEngineer can also be allowed to delegate to tools or potentially request clarification if the CrewAI setup supports it. The primary flow remains guided.

```mermaid
flowchart TD
  CLI["gen_code.py / CodeModernizationCrew kickoff"] --> SA[SoftwareArchitect: Prepares Step Brief]
  SA -- Modernization Step Brief --> TL[TeamLead: Orchestrates Step Execution]
  
  TL -- Assigns Coding Task (with Brief) --> PSE[PrincipalSoftwareEngineer: Implements Code Changes]
  PSE -- Code Changes --> TL
  
  TL -- Requests Build (with path to changes) --> BT[BuildAndTestAgent: Compiles Code]
  BT -- Build Results --> TL
  
  TL -- Presents Diff & Build Results for Validation --> HUMAN[Human User]
  
  HUMAN -- Approves --> TL
  TL -- Marks Step Done (via PlanTool) & Signals SA --> SA
  
  HUMAN -- Requests Changes --> TL
  TL -- Re-assigns Coding Task with Feedback (to PSE) --> PSE

  %% Potential delegation/feedback loops (conceptual)
  PSE -.-> SA # PrincipalSoftwareEngineer might request clarification from SoftwareArchitect (if crew allows)
  SA -.-> TL # SoftwareArchitect might provide updated guidance to TeamLead based on observed issues