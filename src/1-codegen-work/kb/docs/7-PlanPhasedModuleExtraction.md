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
