---

# Migration Practices Report: Java EE/Red Hat JBoss EAP to Spring Boot on Java 21

This report consolidates best practices, recommended tools, migration patterns, and case study references for modernizing Java EE applications running on Red Hat JBoss EAP to Spring Boot on Java 21. Legacy framework updates for logging and persistence are also covered.

---

## 1. Migration Patterns

### 1.1 Strangler Fig Pattern
- The Strangler Fig pattern advocates incrementally replacing legacy system components by building new functionality around or alongside the old system.
- Gradually, new Spring Boot services can replace Java EE components, allowing coexistence and phased migration.
- This approach minimizes risk by avoiding a big-bang rewrite and supports continuous delivery and testing.

### 1.2 Branch-by-Abstraction Pattern
- This pattern involves introducing abstraction layers or interfaces to isolate legacy code.
- Implement new Spring Boot services behind these abstractions.
- Switch traffic between old and new implementations transparently.
- Enables rollback and iterative modernization without disrupting users.

---

## 2. Tool Recommendations

### 2.1 OpenRewrite
- An open-source automated refactoring tool that applies codemods and structural transformations.
- Provides community recipes for migrating from Java EE (javax.* to jakarta.*) to Spring Boot 3 and upgrading Java versions all the way to Java 21.
- Example use cases:
  - Rewriting package namespaces.
  - Updating deprecated API usage.
  - Refactoring persistence and Spring annotations.
- Integrates with build tools (Maven/Gradle).
- [OpenRewrite documentation on Java 21 Migration](https://docs.openrewrite.org/running-recipes/popular-recipe-guides/migrate-to-java-21)
- [OpenRewrite Spring Boot 3 Migration Recipes](https://docs.openrewrite.org/recipes/java/spring/boot3/springboot3bestpractices)

### 2.2 jdeps
- A Java class dependency analyzer tool.
- Used to detect dependencies on unsupported or deprecated APIs in the codebase before migrating.
- Helps map dependencies that need updates or replacements.

### 2.3 Flyway and Liquibase
- Tools for database migrations that support version-controlled schema changes.
- Essential for migrating persistence layers safely.
- Flyway and Liquibase migration scripts can be integrated into the Spring Boot application lifecycle.
- When migrating, ensure credentials and connection strings are updated appropriately.
- See [OpenRewrite Database Credential Migration](https://docs.openrewrite.org/recipes/java/spring/boot2/migratedatabasecredentials) for automating credential configuration migration.

### 2.4 Migration Toolkit for Runtimes (Red Hat)
- Rule-based tool that automates and assists in migrating Java applications, particularly from Red Hat JBoss EAP.
- Analyzes code for deprecated APIs and provides guidance on replacements.
- Useful for entreprise-specific migration requirements.

---

## 3. Legacy Frameworks Modernization

### 3.1 Logging Framework
- Replace Java Util Logging or JBoss logging with Spring Boot’s default logging (`spring-boot-starter-logging`).
- Use SLF4J abstraction for flexibility.
- OpenRewrite offers codemods to assist automated logging migration.

### 3.2 Persistence Framework
- Migrate from legacy JPA implementations towards Spring Data JPA repositories.
- Hibernate ORM remains the ORM of choice, with Spring Boot providing automatic configuration and integration.
- Manage database schema migrations explicitly via Flyway or Liquibase.

---

## 4. Java and Spring Boot Version Upgrades

- Upgrade Java in steps (e.g., Java 8 → 11 → 17 → 21) to catch deprecations early.
- Spring Boot 3.x requires Java 17+ and supports Java 21 in recent releases (3.2 and later).
- Review and replace deprecated APIs like Servlet, CDI, and JPA annotations due to namespace shifts (javax.* to jakarta.*).
- Use OpenRewrite recipes to automate transformation to the new Jakarta namespaces and Spring idioms.
- Upgrade tests to JUnit 5 and Spring Boot Test framework.

---

## 5. Case Study References

- [Red Hat JBoss EAP 8 Migration Guide](https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.0/html-single/migration_guide/index): Comprehensive guidance from Red Hat on migrating EAP applications.
- [OpenRewrite User Stories](https://docs.openrewrite.org/recipes/java/spring/boot3/springboot3bestpractices): Demonstrates real migrations to Spring Boot 3 and Java 21.
- [Migration Toolkit for Runtimes](https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/1.2/html-single/introduction_to_the_migration_toolkit_for_runtimes/index): Rules-based transformation tool from Red Hat.

---

## 6. Summary

| Migration Aspect     | Best Practices & Tools                              |
|---------------------|----------------------------------------------------|
| Approach/Patterms   | Strangler Fig, Branch-by-Abstraction                |
| Refactoring Tools    | OpenRewrite (namespace and API update recipes)     |
| Dependency Analysis  | jdeps                                               |
| DB Migrations        | Flyway, Liquibase for schema version control        |
| Legacy Frameworks    | Switch logging to SLF4J with Spring Boot logging    |
| Java Version Upgrades| Stepwise upgrade Java 8 → 11 → 17 → 21              |
| Testing Frameworks   | Upgrade to JUnit 5 and Spring Boot Test              |
| Enterprise Support   | Red Hat Migration Toolkit for Runtimes               |

---

This comprehensive report aims to guide you through a phased, automated, and risk-mitigated migration from Java EE/Red Hat JBoss EAP to modern Spring Boot applications running on Java 21.

Please let me know if you require detailed migration steps per individual component or further automation scripts.

---