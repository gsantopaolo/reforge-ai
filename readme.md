## 🚀 ReforgeAI

ReforgeAI is an agentic AI system designed to modernize legacy Java codebases. It automatically analyzes existing code, generates comprehensive documentation and a transformation plan, and then carries out code modernization tasks. The system updates package dependencies, refactors deprecated or inefficient components, migrates to new frameworks, and embeds security best practices. Human feedback ensures accuracy and quality at every stage. 🤖✨

---

## 📋 Table of Contents

* [Features](#-features)
* [Requirements](#-requirements)
* [Installation](#-installation)
* [Usage](#-usage)
* [Process Overview](#-process-overview)
* [Human-in-the-Loop Feedback](#-human-in-the-loop-feedback)
* [Known Issues & Troubleshooting](#-known-issues--troubleshooting)
* [Next Steps](#-next-steps)
* [License](#-license)

---

## 🔧 Features

* **Automated Analysis**: Scans legacy code and produces detailed documentation. 📄
* **Transformation Plan**: Generates a YAML plan outlining modernization steps. 📝
* **Automated Refactoring**: Updates dependencies, replaces deprecated APIs, and optimizes inefficient code. 🔄
* **Framework Migration**: Switches to modern language frameworks (e.g., from Java EE to Spring Boot). 🏗️
* **Security Best Practices**: Incorporates OWASP guidelines and secure coding patterns. 🔒
* **Build & Test Integration**: Runs builds and unit tests, reporting results for review. ✅
* **Human Feedback Integration**: Allows reviewers to approve plans and transformations. 👥

---

## 🛠️ Requirements

To compile and run both the legacy (`gen_docs.py`) and modern (`gen_modern.py`) pipelines, you will need:

1. **Java Environments**

   * Java 8 JDK (for legacy code compilation) ☕
   * Java 21 JDK (for modernized codebase) 🔧
2. **Maven 3.8+** (build tool and dependency manager) 🎯
3. **Python 3.8+**

   * `openai` library for LLM integration 🤖
   * `pyyaml` for YAML plan generation 📨
   * `langtrace-sdk` (optional) for monitoring 🔍
4. **Git** (version control) 🐙
5. **Network Access** (to pull dependencies and contact AI APIs) 🌐

---

## 🚀 Installation

1. **Clone the Repo**

   ```bash
   git clone https://github.com/your-org/ReforgeAI.git
   cd ReforgeAI
   ```
2. **Set up Python Env**

   ```bash
    conda create -n reforgeai python=3.11.7 -y
    conda activate reforgeai
    pip install -r requirements.txt
   ```
3. **Configure API Keys**

   * Set `OPENAI_API_KEY` in your environment, see ```.env.example```.

---

## 🎬 Usage

1. **Generate Documentation & Plan**

   ```bash
   python3 gen_docs.py <path_to_legacy_codebase>
   ```
2. **Execute Modernization**

   ```bash
   python3 gen_modern.py
   ```
3. **Review Changes**

   * Inspect `plan.yaml`, build logs, and test reports.
   * Accept or provide feedback on transformations.

---

## 🔄 Process Overview

1. **Analysis Phase**

   * `gen_docs.py` reads and documents code.
   * Outputs detailed docs and `plan.yaml` draft.
1.1 **Plan Review**
   * Human reviewers validate or adjust the plan.

3. **Transformation Phase**

   * `gen_modern.py` executes plan tasks:

     * Dependency updates
     * Refactorings
     * Framework migrations
     * Security enhancements
   * Generates build/test reports for each module.

4. **Analysis and agents breakdown:**
   * [Documentation Generation Agents, Tasks, and Crew](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/documentation_crew.md)
   * [Documentation Generation Pipeline Analysis](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/documentation_generation.md)
   * [Code Generation Agents, Tasks, and Crew](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/gen_code_crew.md)
   * [Code Generation Pipeline Analysis](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/gen_code_generation.md)


## 📝 Human-in-the-Loop Feedback

* Every document includes a feedback section (see `feedback/`).
* Critical review points:

  * Did the agent read all docs correctly? 🧐 (`feedbackj` tasks)
  * Were the intended changes applied? ✅ (`feedback` tasks)

---

## ⚠️ Known Issues & Troubleshooting

* **Inconsistent Model Outputs**: Running `gen_docs.py` multiple times may yield different results. Models may degrade under heavy usage.
* **Build Agent Hallucinations**: Simulated build logs can be inaccurate. Monitor via Langtrace: [Traces Dashboard](https://app.langtrace.ai/project/cmadwbajj0007yfqm1yefsv96/traces)
* **Agent Tools Errors**: Sometimes the LLm refuses to read docs due to tool selection issues. Restarting the pipeline often helps.
* **Folder Cleanup**: The agent cannot delete folders. Manual cleanup may be required.

---

## 🚧 Next Steps

* Implement better path guardrails to avoid file-scope issues.
* Add per-document feedback sections for granular review.
* Explore upgrading to Gemini 2.5 Pro & Claude 3.7 for consistent performance.
* Enhance agent monitoring and error reporting.

For the complete list of improvements/next steps, read:
- [Code Generation Improvement Suggestions](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/gen_code_improvements.md)
- [Documentation Generation Improvement Suggestions](https://github.com/gsantopaolo/reforge-ai/blob/main/docs/documentation_improvements.md)
---

---

## 📚 References
- [MongoDB Launches New Program for Enterprises to Build Modern Applications with Advanced Generative AI Capabilities](https://www.mongodb.com/press/mongodb-launches-new-program-for-enterprises-to-build-modern-applications-with-advanced-generative-ai-capabilities) :contentReference[oaicite:0]{index=0}
- [Leveraging Large Language Models for Automated Code Migration and Repository-Level Tasks — Part II: Supplement — Specialized Language Models for Code](https://medium.com/@jelkhoury880/leveraging-large-language-models-for-automated-code-migration-and-repository-level-tasks-part-ii-24d23c3cc7a0) :contentReference[oaicite:1]{index=1}
- [Upgrading Java versions with Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-transformation.html) :contentReference[oaicite:2]{index=2}
- [Generative AI in application modernization](https://www.ibm.com/think/topics/generative-ai-for-application-modernization) :contentReference[oaicite:3]{index=3}
- [Generative AI: A Transformative Force in Legacy App Modernization](https://www.nttdata.com/global/en/insights/focus/2025/generative-ai-a-transformative-force-in-legacy-app-modernization) :contentReference[oaicite:4]{index=4}
- [The Unreasonable Effectiveness of Generative AI in Legacy Application Modernization](https://medium.com/@adnanmasood/the-unreasonable-effectiveness-of-generative-ai-in-legacy-application-modernization-0e81d294f894) :contentReference[oaicite:5]{index=5}
- [Application Modernization | MongoDB](https://www.mongodb.com/resources/solutions/use-cases/application-modernization) :contentReference[oaicite:6]{index=6}
- [Why General-Purpose LLMs Won’t Modernize Your Codebase — And What Will](https://medium.com/@jelkhoury880/why-general-purpose-llms-wont-modernize-your-codebase-and-what-will-eaf768481d38)
- [Modernizing Legacy Java Applications — Best Practices and Considerations](https://medium.com/@AlexanderObregon/modernizing-legacy-java-applications-best-practices-and-considerations-a01b3b52ee7a)
- [janus-llm/janus-llm: Leveraging LLMs for modernization through intelligent chunking, iterative prompting and reflection, and retrieval augmented generation (RAG)](https://github.com/janus-llm/janus-llm)
- [spring-projects-experimental/spring-boot-migrator: Spring Boot Migrator (SBM) is a tool for automated code migrations to upgrade or migrate to Spring Boot](https://github.com/spring-projects-experimental/spring-boot-migrator)
- [This Year in Uber's AI-Driven Developer Productivity Revolution](https://www.youtube.com/watch?v=jp-fBw07r7c)  


---