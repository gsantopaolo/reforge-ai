Migration Practices Report for Java EE / Red Hat JBoss EAP to Spring Boot on Java 21

1. Migration Patterns

- Strangler Fig Pattern: Incrementally replace legacy application parts with new Spring Boot components, letting the old and new code coexist during migration. Useful for minimizing downtime and risk.
- Branch-by-Abstraction: Introduce an abstraction layer to isolate legacy Java EE API usage, allowing seamless switching between legacy and modernized implementations behind the scenes.
- Anti-Corruption Layer: Implement a layer that reduces dependencies between legacy systems and new Spring Boot services, improving modularity and maintainability.

2. Tool Recommendations

- OpenRewrite: An automated code refactoring tool providing recipes to migrate Java EE codebases to Spring Boot 3 and Java 21 compatibility. Supports automatic transformation of deprecated APIs, package namespaces migrating from javax.* to jakarta.* and modernization of persistence and REST code.
- Spring Boot Migrator (SBM): A dedicated migration tool provided by VMware that helps convert existing non-Spring Boot Java EE-based applications (EJB, JMS, JAX-RS) into Spring Boot projects with best-practice configurations.
- Eclipse Transformer: Facilitates automatic replacement of javax.* namespace references to jakarta.* namespaces necessary for compatibility with Jakarta EE 9+ used by Spring Boot 3.
- jdeps: Java dependency analysis tool to analyze module dependencies and help identify Java EE dependencies for migration planning.
- Flyway / Liquibase: Database schema migration tools recommended to manage incremental changes to DB schemas alongside code migration safely and with version control.

3. Legacy Framework Modernization

- Logging: Migrate from legacy logging frameworks such as java.util.logging, log4j 1.x, or JBoss Logging to SLF4J with Logback or Log4J2 supported natively by Spring Boot.
- Persistence: Migrate from legacy Jakarta Persistence (JPA) or Hibernate versions tied to JBoss EAP to Spring Data JPA backed by Hibernate 6 or higher compatible with Java 21 and Spring Boot 3. Use annotation and configuration modernizations aligned with Spring Data.
- REST: Rewrite JAX-RS REST services as Spring MVC or Spring WebFlux controllers. Remove old JAX-RS annotations and transition to Spring’s @RestController and request mapping annotations.
- UI Frameworks: Replace Jakarta Faces (JSF) with Spring MVC using Thymeleaf or modern JavaScript frameworks. Spring Boot lacks native JSF support.
- Validation: Replace Jakarta Bean Validation with Hibernate Validator 8 compatible with Spring Boot's validation starter.

4. Case Study References

- CCEE Brazil: An organization described migrating a Java EE system to Spring Boot using PoCs, evaluating migration strategies, taking an incremental migration approach to minimize disruptions.
- OpenRewrite Java Recipes Community: Numerous examples and recipes available for real-world code transformations aligned with Spring Boot 3 migration.
- VMware’s Spring Boot Migrator user feedback: Helps enterprises convert large monolithic Java EE apps with EJB and JMS technologies efficiently.
- Articles and blog posts describing migrations from Java 8/11 to Java 21 in combination with Spring Boot 3.2+ provide concrete guidelines on preparing for Java 21 runtime features, including virtual threads and module system adjustments.

5. Additional Best Practices

- Plan phased migration targeting business-critical modules that provide highest value first.
- Maintain a central knowledge base documenting legacy-to-modern equivalent mappings and migration decisions.
- Schedule weekly documentation and code refactoring sprints with frequent audits against quality gates.
- Ensure strong integration and performance testing to verify that migration does not affect functionality.
- Continuously upgrade libraries and frameworks to versions compatible with Java 21 and Spring Boot 3.

References:

- https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/
- https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.0/html-single/migration_guide/
- https://docs.openrewrite.org/recipes/java/spring/boot3/
- https://www.infoq.com/news/2022/09/spring-boot-migrator/
- https://www.kloia.com/blog/migrating-to-java-21-with-spring-framework-and-spring-boot-technical-tips-and-strategies
- https://www.infoq.com/presentations/ccee-java-ee-spring/

This comprehensive report addresses migration patterns, key tooling, framework upgrades, and provides case-study references to support an effective migration from traditional Java EE / Red Hat JBoss EAP architectures to Spring Boot on the latest Java 21 runtime environment.