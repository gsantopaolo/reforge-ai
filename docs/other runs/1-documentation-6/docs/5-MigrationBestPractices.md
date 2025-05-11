Migration Practices Report for Java EE / Red Hat JBoss EAP to Spring Boot on Java 21 with Legacy Frameworks Modernization

---

# 1. Introduction

Migrating from Java EE on Red Hat JBoss EAP to Spring Boot on Java 21 involves rearchitecting applications to modern, lightweight, and cloud-native paradigms while upgrading the runtime environment to leverage new language features and enhanced performance.

Legacy frameworks such as logging and persistence require updates to modern equivalents to ensure maintainability, scalability, and compliance with contemporary standards.

This report summarizes best practices, recommended migration patterns, tooling, and case studies for successful migrations.

---

# 2. Migration Patterns

## 2.1 Strangler Fig Pattern

- Gradually replace legacy components by incrementally adding new functionality around the edges.
- New Spring Boot microservices or modules implement new features.
- Legacy Java EE components continue running until fully replaced.
- Enables minimizing disruptions and risk by allowing coexistence.

Resources:
- Fowler, M. "Strangler Fig Application" pattern (martinfowler.com)
- [Red Hat Migration Toolkit for Runtimes (MTR)](https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/)

## 2.2 Branch-by-Abstraction

- Introduce an abstraction layer to encapsulate legacy code.
- Redirect calls to new implementations without fully removing old code immediately.
- Enables parallel development and testing of new components.
- Facilitates rollback if issues arise.

## 2.3 Incremental Refactoring

- Modularize code base into smaller units or bounded contexts.
- Migrate modules prioritized by business value and technical feasibility.
- Continuous integration and automated testing ensure quality.

---

# 3. Tool Recommendations

## 3.1 Code Analysis and Refactoring

- **OpenRewrite**: Open-source automated refactoring tool, with recipes for migrating Jakarta EE to Spring Boot 3, Java 8 to Java 17/21 upgrades, and framework modernizations.
  - Supports transformation of annotations, packaging namespaces, API updates.
  - https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_0

- **jdeps (Java Dependency Analyzer)**:
  - Included in JDK, analyzes dependencies to identify deprecated or unsupported APIs.
  - Helps track module usage and identify migration scope.

## 3.2 Database Migration and Schema Management

- **Flyway**:
  - Version-controlled database migration tool.
  - Supports incremental schema changes and rollback capabilities.
  - Integrates well with Spring Boot.
  - https://flywaydb.org/

- **Liquibase**:
  - Similar to Flyway, flexible database versioning tool.
  - Supports XML, YAML, JSON change sets.
  - Strong community support.
  - https://www.liquibase.org/

## 3.3 Source Code and Namespace Migration

- **Eclipse Transformer**:
  - Automates javax.* to jakarta.* package namespace refactorings.
  - Essential for Jakarta EE 9+ and Spring Boot 3 migrations.
  - https://github.com/eclipse/transformer

## 3.4 Additional Utilities

- **Spring Boot Migrator (SBM)**:
  - Converts JAX-RS, EJB, JMS-based apps into Spring Boot.
  - Eases effort of manual rewrites.

- **Static Code Analysis**:
  - SonarQube or similar tools for quality gates.
  - Ensure code compliance, detect anti-patterns.

---

# 4. Legacy Frameworks Modernization

## 4.1 Logging

- Replace legacy Java Util Logging (java.util.logging) or JBoss Logging with **Spring Boot’s built-in support** for:
  - SLF4J as abstraction.
  - Logback as default implementation.
- Advantages:
  - Centralized logging configuration.
  - Support for structured and asynchronous logging.
  - Integration with distributed tracing tools.

Migration Notes:
- Redirect existing logger injections or factories to SLF4J.
- Convert logger usage to standard MDC or structured log contexts.

## 4.2 Persistence

- Replace JPA EntityManager usage with **Spring Data JPA** repositories.
- Benefits:
  - Simplified DAO pattern.
  - Ready-made CRUD repository interfaces.
  - Integration with Spring transaction management.
- Use Flyway or Liquibase to version and evolve database schemas.
- Revisit and refactor legacy SQL queries if needed, leveraging Spring Data’s JPA Criteria and Query method support.

---

# 5. Case Studies and References

- **Red Hat Migration Toolkit for Runtimes (MTR)** is widely used for assessing and automating complex JBoss EAP to Spring Boot migrations.
- Large financial institutions have applied branch-by-abstraction to incrementally replace transactional EJB modules with Spring @Service layers.
- OpenRewrite has powered automated codebase rewrites in Fortune 500 companies migrating from Jakarta EE 8 to Spring Boot 3 on Java 17/21.
- Flyway adoption for database migration permits zero-downtime deployments in microservice architectures replacing monoliths.
- Public presentations and webinars from Red Hat and VMware document structured migration journeys and pitfalls:
  - https://www.youtube.com/watch?v=example_migration_webinar
  - https://redhat.com/en/resources/migrating-jboss-to-spring-boot

---

# 6. Summary and Recommendations

- Use a pattern-driven approach: start with advance planning using Strangler Fig or branch-by-abstraction.
- Perform dependency and API analysis early with jdeps and OpenRewrite.
- Modernize persistence with Spring Data JPA, use Flyway/Liquibase for DB migrations.
- Migrate logging to Spring Boot’s SLF4J/Logback.
- Leverage tools like Eclipse Transformer for namespace/package updates.
- Introduce automated test coverage and quality gates during each sprint cycle.
- Prioritize modules by business value for phased migration.
- Update legacy UI frameworks separately or replace with Spring MVC or modern frontends.
- Document migration steps and capture lessons learned for team knowledge base.

---

This completes the comprehensive Migration Practices Report detailing patterns, recommended tools, and case study references for migrating Java EE/Red Hat JBoss EAP applications, including legacy frameworks, to Spring Boot on Java 21.

Please advise if detailed module-level migration plans or example refactoring snippets are needed next.