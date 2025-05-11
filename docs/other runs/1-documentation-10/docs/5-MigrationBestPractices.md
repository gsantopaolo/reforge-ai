Migration Practices Report for Migrating Java EE / Red Hat JBoss EAP to Spring Boot on Java 21 and Legacy Framework Modernization

1. Migration Patterns

- Strangler Fig Pattern:
  The Strangler Fig pattern is recommended for incrementally migrating a monolithic Java EE application to microservices or modular Spring Boot components. It involves gradually replacing parts of the legacy system by routing functionality either to the new system or retaining it in the legacy one until full migration is complete. This pattern reduces risk by allowing co-existence and phased rollout of components.

- Branch-by-Abstraction:
  This strategy uses an abstraction layer that both legacy and new implementations conform to, allowing seamless switching between legacy and modernized code paths. It supports parallel development and straightforward fallbacks and is suitable for refactoring legacy frameworks such as persistence, logging, and validation.

2. Tool Recommendations

- OpenRewrite:
  OpenRewrite provides automated source code refactoring recipes designed to upgrade and migrate Java applications. It has specific recipes for migrating to Spring Boot 3.0, adjusting deprecated API usage, and updating configurations. Utilizing OpenRewrite accelerates bulk code modifications and reduces errors in migration.

- jdeps:
  The Java dependency analysis tool jdeps helps identify dependencies and transitive libraries in current applications, critical for preparing migration by assessing compatibility and dependency footprint on Java 21 and Spring Boot stacks.

- Flyway and Liquibase:
  For database migrations, Flyway and Liquibase are robust tools to manage schema versioning and data transformations in a controlled, repeatable manner. They integrate well with Spring Boot and facilitate evolving the database schema alongside application refactoring.

3. Legacy Framework Modernization

- Logging:
  Migrate from legacy Java logging frameworks (e.g., java.util.logging, Log4j 1.x) to SLF4J with Logback or Log4j2 supported by Spring Boot starters, standardizing logging and making configuration simpler.

- Persistence:
  Transition from JPA EntityManager and Hibernate setups in Java EE to Spring Data JPA repositories, leveraging repository abstractions for cleaner code. Employ Flyway/Liquibase to version database schema migrations.

- Validation:
  Replace legacy bean validation with Spring Boot's integrated validation starter using Hibernate Validator, enabling robust and declarative validation mechanisms.

4. Case-Study References and Insights

- Red Hat's Migration Toolkit for Runtimes (MTR) provides insights into automating migration assessments and categorizing remediation steps. Although primarily targeting Red Hat environments, MTR principles apply broadly for modernizing Java apps.

- Community reports on migrating large-scale payments systems show success with the Strangler Fig pattern by incrementally replacing parts with Spring Boot microservices while continuing to route older logic.

- OpenRewrite users report significant reduction in manual changes when upgrading core dependencies, API versions, and migrating to Spring Boot 3 ecosystem leveraging OpenRewrite's codemod recipes.

- Flyway/Liquibase case studies highlight seamless database evolution management supporting continuous integration pipelines during refactoring.

Conclusion: Adopt phased migration strategies like the Strangler Fig Pattern and branch-by-abstraction to incrementally modernize Java EE / JBoss EAP applications. Utilize automated tooling such as OpenRewrite for codebase refactoring and jdeps for dependency analysis. Manage database evolution with Flyway or Liquibase integrated into Spring Boot. Modernize legacy frameworks stepwise to Spring Boot equivalents for logging, persistence, and validation. Leverage documented migration guides and case studies from Red Hat and community sources to tailor migration plans suited for Java 21 environments.

References:
- https://docs.openrewrite.org/
- https://medium.com/@rrbadam/strangler-fig-pattern-to-migrate-from-a-monolithic-java-application-to-spring-boot-microservices-1f260bb6e4c4
- https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide
- https://flywaydb.org/documentation/
- https://www.liquibase.org/get-started/migration-tutorial
- https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/1.2/html-single/introduction_to_the_migration_toolkit_for_runtimes/index