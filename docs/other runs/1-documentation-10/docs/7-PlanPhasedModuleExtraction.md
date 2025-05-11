# kitchensink Java 21 & Spring Boot Migration - Phased Extraction Plan

---

## 1. Identification of Least-Coupled Module and Domain-driven Boundaries

- After coupling analysis and DDD consideration, the **`util` package** is identified as the least coupled module suitable for first migration.
- It contains essential helper utilities (`Resources.java`), with limited dependencies on other modules.
- This package forms foundational support for other modules and can be migrated independently with low risk.

## 2. Spring Modulith as Intermediate Modular Monolith Step

- Spring Modulith provides conventions/APIs for defining logical **modules inside a Spring Boot monolith**.
- Use Spring Modulith to **introduce module boundaries incrementally** before splitting into microservices.
- Encapsulate `util` package as a Spring Modulith module implementing shared utilities.
- Benefits:
  - Enforces **module isolation and dependency rules**.
  - Supports **transaction management, events, and API encapsulation**.
  - Facilitates later decomposition into microservices.

## 3. Coexistence Strategy: Legacy + New Modules

- Use an **API Gateway or Proxy** (e.g., Spring Cloud Gateway or Zuul) for **routing requests between legacy and new modules**.
- Implement **Branch-by-Abstraction**: create interface layers abstracting calls to either legacy or new components.
- Monitor traffic with routing rules and **gradually switch client calls** to Spring Boot modules.
- Ensure both legacy and migrated modules can **run in parallel** during transition.
  
## 4. OpenRewrite and Modern Build/Config Enhancements

- Leverage **OpenRewrite recipes** specifically tailored for:
  - Migrating Jakarta EE namespaces to Spring Boot 3.2+ compatible APIs.
  - Refactoring `EntityManager` to Spring Data repositories.
  - Updating validation and CDI annotations to Spring equivalents.
- Automate build and config file migration (e.g., `pom.xml`, `application.properties` to Spring Boot starters).
- Use OpenRewrite as part of daily or sprint-based CI tasks to **enforce migration quality gates**.

## 5. Adoption of Virtual Threads in High-Throughput Components

- Identify components in `service` and `rest` modules that perform **blocking I/O or high concurrency tasks**.
- Plan **incremental replacement with virtual threads** by:
  - Using Java 21 Project Loom capabilities.
  - Gradually migrate request handler threads, database calls, and service orchestration code to **virtual threads**.
- Test extensively with Spring’s **reactive programming support** for compatibility.
  
## 6. Strangler Fig and Incremental Migration Principles

- Implement Strangler Fig pattern by:
  - Extracting modules incrementally.
  - Using feature toggles or API gateway routing to route traffic.
  - Avoiding big-bang migration; apply **phased co-existence strategies** instead.
  
---

# Migration Plan — YAML Format

```yaml
phases:
  - id: 1
    description: Extract and migrate `util` package as standalone Spring Modulith module with Java 21 features.
    output: Spring Boot Java 21 compatible `util` module with module boundaries, injected via Spring DI.
    suggested_tools:
      - KnowledgeBaseTool
      - DomainModelAnalyzerTool
      - OpenRewriteTool
      - CompilerTool
      - TestRunnerTool
      - DocumentationTool

  - id: 2
    description: Incrementally migrate `data` and `service` packages refactoring to Spring Data JPA repositories and Spring @Service beans.
    output: Modularized data and service layers supporting both legacy and Spring Boot coexistence.
    suggested_tools:
      - OpenRewriteTool
      - DomainModelAnalyzerTool
      - CodeLoaderTool
      - CompilerTool
      - TestRunnerTool
      - DocumentationTool

  - id: 3
    description: Migrate controller and rest packages to Spring MVC and Spring Boot REST controllers, integrating with API Gateway.
    output: Fully modularized Spring Boot REST API with routing configured for legacy coexistence.
    suggested_tools:
      - GatewayConfiguratorTool
      - OpenRewriteTool
      - CompilerTool
      - TestRunnerTool
      - DocumentationTool

  - id: 4
    description: Integrate virtual threads in high-throughput components, conduct performance and correctness testing.
    output: Optimized Spring Boot modules leveraging Java 21 virtual threads.
    suggested_tools:
      - CompilerTool
      - TestRunnerTool
      - KnowledgeBaseTool

  - id: 5
    description: Complete legacy system deprecation, consolidate codebase, optimize modularity for production microservices deployment.
    output: Fully modernized Java 21 Spring Boot application with modular microservices-ready architecture.
    suggested_tools:
      - KnowledgeBaseTool
      - DiagramGeneratorTool
      - DocumentationTool

---

# Detailed Agent Actions for Migration of `util` Module (Phase 1)

- Identify all files in `util` package, e.g., `Resources.java`.
- Refactor code using OpenRewrite Spring Boot 3.2 recipes to modernize annotations, logging, and dependencies.
- Break down `util` package into a Spring Modulith module, creating module descriptor using Spring Modulith APIs.
- Migrate codebase to Java 21 language features (e.g., Records, Pattern Matching, Sealed Classes) as appropriate.
- Add tests verifying functionality.
- Package and build as standalone jar/library to be referenced by other modules.
- Commit changes incrementally to central knowledge base documenting migration artifacts and issues.

---

# Coexistence Strategy to Enable Parallel Legacy and New Modules

- Establish API Gateway routing rules:
  - Route relevant REST paths to new Spring Boot modules.
  - Route remaining legacy functionality unchanged.
- Implement Branch-by-Abstraction via interfaces abstracting services that route to legacy or new services based on feature flags.
- Use proxy components to translate calls between legacy EJB and Spring Beans where needed.
- Continuously sync database schemas with Flyway to maintain compatibility.
- Monitor and log traffic flows for safe rollbacks or rapid fixes.
- Gradually increase traffic share to migrated modules controlled by rollout plans.

---

# Dependency Minimization Strategies

- Refactor service and data layers to use Spring Data repositories instead of tightly coupled EntityManager.
- Introduce API boundaries between modules using Spring Modulith.
- Avoid circular dependencies by enforcing module visibility rules.
- Leverage Dependency Injection for loose coupling.
- Use branch-by-abstraction to isolate legacy from new code during phased migration.

---

# List of Modules and Components to Migrate from Least to More Complex (Including Classes)

1. util  
   - Resources.java

2. model  
   - Member.java  (Enhanced with Java 21 features)

3. data  
   - MemberRepository.java (Migrate to Spring Data JPA Repository Interface)  
   - MemberListProducer.java (Spring Bean producer service)

4. service  
   - MemberRegistration.java (Convert to Spring @Service with @Transactional)

5. controller  
   - MemberController.java (Convert to Spring MVC Controller)

6. rest  
   - JaxRsActivator.java (Replace with Spring Boot auto configuration)  
   - MemberResourceRESTService.java (Spring REST @RestController)

---

This comprehensive plan harnesses modern Java 21 and Spring Boot best practices, strongly aligning with domain-driven design, modular monolith preparations with Spring Modulith, gateway routing for backward compatibility, OpenRewrite automation for safe migration, and progressive virtual thread adoption for performance gains. The YAML structured phased plan enhances clarity and automation readiness for execution by agentic AI with human collaboration.

```