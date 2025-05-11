---
# Phased Extraction Plan and Migration Strategy for kitchensink Legacy Application to Java 21 with Spring Boot

This document provides a detailed, stepwise, phased extraction plan to incrementally migrate the kitchensink legacy Java EE application to Java 21, Spring Boot 3.2 using domain-driven design principles, Spring Modulith as an intermediate modular monolith step, coexistence strategies leveraging gateway/proxy routing per the Strangler Fig pattern, OpenRewrite recipes for automated code migration, and adoption of virtual threads for high-throughput components. The plan is designed for execution by an agentic AI augmented by human supervision.

---

## 1. Summary of Identified Modules and Coupling Analysis

Based on the current project package structure and dependency graph:

- **Modules identified:**
  - util: `Resources` (Utility class, minimal dependencies)
  - model: `Member` (Domain entity)
  - data: `MemberRepository`, `MemberListProducer` (Persistence layer interacting with model)
  - service: `MemberRegistration` (Business logic depending on data and model)
  - controller: `MemberController` (UI interaction depending on service)
  - rest: `JaxRsActivator`, `MemberResourceRESTService` (REST API layer interacting with service and data)

- **Coupling considerations:**
  - `util` is a low-dependency utility module.
  - `model` encapsulates core domain entities, serves as a stabilized API.
  - `data` depends on `model` entities.
  - `service` depends on `data` and `model`.
  - `controller` depends on `service`.
  - `rest` depends on `service` and `data`.

- **Least-coupled candidate module to extract first:**
  - `util` due to minimal dependencies.
  - However, its business value and domain importance are low.
  - Next is `model` module since it provides stable domain abstraction.
  - For migration impact and business value, `service` or `data` may be more beneficial.
  - Balancing domain-driven boundaries and low coupling: `service` module `MemberRegistration` is a good candidate first incremental extraction.
  
---

## 2. Migration Criteria

- **Domain-Driven Design:** Respect bounded contexts — migrate cohesive domain service `MemberRegistration` and associated data access with minimal coupling on third-party legacy APIs.
- **Spring Modulith intermediate modularization:** Organize the service and related modules into Spring Modulith modular jar maintaining boundaries to ease transition.
- **Incremental migration:** Extract modules incrementally following the Strangler Fig pattern; migrate one module fully before next.
- **Coexistence strategy:** Use gateway/proxy routing to forward requests to new Spring Boot modules or legacy components based on URI path or feature flags.
- **OpenRewrite Spring Boot 3.2 recipes:** Automate source updates for build, configuration properties, and code refactoring for Spring Boot compatibility.
- **Virtual threads:** Adopt virtual threads for high-throughput services (such as registration workflows) after proof of concept.
  
---

## 3. Phased Extraction Plan

### Phase 1: Extract Service Module (`MemberRegistration`)

- **Description:** Extract the business logic service `MemberRegistration` along with its dependencies on `MemberRepository` and `Member` domain entity for independent compile and run in Spring Boot 3.2.
- **Output:** Standalone Spring Boot module implementing member registration business rules.
- **Steps:**
  1. Create new Spring Modulith module `member-service`.
  2. Migrate `MemberRegistration.java`.
  3. Include `Member.java` entity to respect domain boundary.
  4. Migrate essential repository interface `MemberRepository`.
  5. Refactor code using OpenRewrite recipes to adopt Spring Boot idioms, Jakarta namespace.
  6. Setup gateway routing to forward registration service calls to new module while legacy continues handling other requests.
  7. Validate via integration tests.
- **Tools:**  
  - KnowledgeBaseTool  
  - DomainModelAnalyzerTool  
  - ModulithGeneratorTool  
  - GatewayConfiguratorTool  
  - OpenRewriteTool  
  - CompilerTool  
  - TestRunnerTool

### Phase 2: Extract Data Module (`MemberRepository`, `MemberListProducer`)

- **Description:** Extract data access components enabling independent database interaction in Spring Boot with JPA/Hibernate updated for Jakarta.
- **Output:** Spring Boot data access module supporting service module.
- **Steps:**  
  1. Create new Spring Modulith module `member-data`.  
  2. Migrate `MemberRepository`, `MemberListProducer`, and related configuration.  
  3. Apply transformations via OpenRewrite recipes.  
  4. Adjust `MemberRegistration` to consume new data module as dependency.  
  5. Route data access calls via gateway as needed.  
  6. Validate database connectivity and behavior.  
- **Tools:** As Phase 1

### Phase 3: Extract REST API Module (`MemberResourceRESTService`, `JaxRsActivator`)

- **Description:** Expose business services through Spring MVC-based REST API replacing JAX-RS legacy.
- **Output:** Spring Boot REST module exposing updated APIs.
- **Steps:**  
  1. Refactor REST layer from JAX-RS annotations to Spring Web annotations.  
  2. Create Spring Modulith module `member-rest`.  
  3. Forward API gateway routes selectively.  
  4. Migrate tests to JUnit 5 with Spring Boot test support.  
- **Tools:** As above

### Phase 4: Extract Controller/UI Module (`MemberController`)

- **Description:** Migrate UI controllers to Spring MVC.
- **Output:** Spring Boot compatible UI controllers.
- **Steps:**  
  1. Create `member-controller` module.  
  2. Migrate `MemberController` adapting to Spring MVC idioms.  
  3. Integrate with rest module or service module as needed.  
  4. Gateway routes for UI interactions.  
- **Tools:** As above

### Phase 5: Extract Utility Module (`Resources`)

- **Description:** Isolate utility components with minimal dependencies.
- **Output:** Utility jar module.
- **Steps:**  
  1. Migrate `Resources` class.  
  2. Update references across modules.  
- **Tools:** As above

---

## 4. Dependency Minimization Strategies

- Use interface-based abstractions for interactions across modules.
- Enforce module boundaries using Spring Modulith’s enforced modularity.
- Limit dependencies on legacy APIs by using anti-corruption layers.
- Use virtual threads primarily in `member-service` module for improved concurrency and throughput where registration requests are high.
- Apply automated refactoring with OpenRewrite for consistent update of dependencies and configuration.

---

## 5. Coexistence and Gateway/Proxy Routing Strategy

- Introduce an API Gateway (e.g., Spring Cloud Gateway or Zuul) to act as a facade.
- Routes incoming client requests based on context path or feature flags either to legacy monolith endpoints or to new Spring Boot modules.
- Gradually migrate and switch routes from legacy to new modules with automatic fallback.
- Maintain session and authentication across modules.
- Monitor and log requests for monitoring incremental migration success.
- Use HTTP reverse proxying, service discovery as needed for dynamic routing in containerized or cloud environments.

---

## 6. Agentic AI Detailed Actions for Migration Execution

- Create new maven modules per phased plan: `member-service`, `member-data`, `member-rest`, `member-controller`, `member-util`.
- Migrate Java source files per module:
  - `member-service`: `src/main/java/org/jboss/as/quickstarts/kitchensink/service/MemberRegistration.java`
  - `member-data`: `MemberRepository.java`, `MemberListProducer.java`
  - `member-rest`: `MemberResourceRESTService.java`, `JaxRsActivator.java`
  - `member-controller`: `MemberController.java`
  - `member-util`: `Resources.java`
- Apply OpenRewrite Spring Boot 3.2 recipes: update dependencies, refactor Jakarta namespaces, configuration migrations.
- Modify build scripts and configs to support Java 21.
- Implement gateway configuration for routing proxy coexistence.
- Introduce virtual threads in service methods with high concurrency.
- Run automated tests and validate module isolation.
- Generate updated UML and dependency diagrams.
- Update documentation with migration notes and plans.

---

## 7. YAML-Formatted Extraction Plan

```yaml
phases:
  - id: 1
    description: Extract MemberRegistration service module with domain entities and migrate to Spring Boot using OpenRewrite
    output: member-service Spring Boot module with isolated business logic
    suggested_tools:
      - KnowledgeBaseTool
      - DomainModelAnalyzerTool
      - ModulithGeneratorTool
      - GatewayConfiguratorTool
      - OpenRewriteTool
      - CompilerTool
      - TestRunnerTool
      - DiagramGeneratorTool
      - DocumentationTool

  - id: 2
    description: Extract data access module including repository and data producers, adapt to Spring Boot and JPA
    output: member-data Spring Boot module with repository components
    suggested_tools: [As phase 1]

  - id: 3
    description: Migrate REST API layer to Spring MVC and expose services via Spring Boot restful endpoints
    output: member-rest Spring Boot module with REST endpoints
    suggested_tools: [As phase 1]

  - id: 4
    description: Extract controller layer to Spring MVC controllers, migrate UI interaction components
    output: member-controller Spring Boot module with MVC controllers
    suggested_tools: [As phase 1]

  - id: 5
    description: Extract utility classes into separate module for reuse across modules
    output: member-util utility module
    suggested_tools: [As phase 1]
```

---

## 8. References and Resources

- OpenRewrite Spring Boot 3.2 recipes: https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_0
- Spring Modulith documentation and guides
- Strangler Fig migration pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig
- Java 21 virtual threads: https://openjdk.org/jeps/444
- Jakarta EE to Spring Boot migration guides and best practices

---

This phased plan provides a practical, incremental pathway for efficient modernization of the kitchensink legacy Java EE application to Java 21 Spring Boot, incorporating modularity, domain-driven design, automated code refactoring, and low-risk coexistence with the legacy system. The plan supports execution by intelligent agents with human oversight and detailed monitoring.

# End of Plan