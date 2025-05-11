# Migration Practices Report: Java EE / Red Hat JBoss EAP to Spring Boot on Java 21 and Legacy Framework Modernization

---

## 1. Migration Patterns

### Strangler Fig Pattern
- Gradual migration strategy where new functionality is developed in Spring Boot services, incrementally replacing legacy Java EE modules.
- Useful for minimizing risk while preserving existing system behavior.
- The legacy system is wrapped or proxied, routing new feature requests to new Spring Boot microservices while legacy functionality remains operational.
- Applied in case studies migrating monolithic Java payment systems and other enterprise apps.

### Branch-by-Abstraction
- Introduce abstraction layers isolating legacy code from new implementations.
- Swap internal implementations behind interfaces enabling incremental refactoring or replacement.
- Allows parallel development and integration testing without disrupting production.

---

## 2. Tool Recommendations

### OpenRewrite
- Automated source code refactoring tool to facilitate large scale API migration.
- Provides recipes to update Spring Boot versions, migrate configuration properties, update deprecated APIs.
- Supports migration from Java EE to Spring Boot idioms.
- Integrates into CI pipelines for continuous modernization.

### jdeps
- Java dependency analysis tool useful for assessing module dependencies.
- Helps identify legacy library dependencies and migration impact.
- Essential to understand transitive dependencies before migration to Spring Boot.

### Flyway / Liquibase
- Database schema migration/versioning tools.
- Critical for managing persistent schema evolution during migration.
- Support rollback, version tracking, seamless database refactoring.
- Integrates well with Spring Boot to automate migration steps on startup.

---

## 3. Case Studies and References

### Case Study: Monolithic Java to Spring Boot Microservices
- Used Strangler Fig pattern for incremental module migration.
- Employed OpenRewrite for automated codebase updates.
- Managed database changes during migration with Flyway.
- Outcome: Reduced risk migration with progressive rollout and retrofit.

### Migration Toolkit for Runtimes (Red Hat)
- Offers tools for automated migration analysis and advice.
- Supports upgrading Java versions and migrating from JBoss EAP to modern runtimes.
- Reference: https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/

### Research Paper on Strangler Fig Pattern Microservice Migration
- Detailed strategy and outcomes on migrating legacy green button system to microservices.
- Reference: https://www.researchgate.net/publication/349568403_Microservice_Migration_Using_Strangler_Fig_Pattern_A_Case_Study_on_the_Green_Button_System

### OpenRewrite Spring Boot Migration Recipes
- Granular step-by-step code refactoring guidance.
- Examples upgrading from Spring Boot 2 to 3.
- Reference: https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_0

### Flyway and Liquibase Reference
- Official documentation for managing database migrations in Spring ecosystems.
- Reference: https://flywaydb.org/documentation/ and https://www.liquibase.org/get-started/quickstart

---

This report consolidates best practices, recommended tools, and references to support efficient, repeatable, and low-risk migration of Java EE / Red Hat JBoss EAP applications and legacy frameworks to modern Spring Boot on Java 21 environments.