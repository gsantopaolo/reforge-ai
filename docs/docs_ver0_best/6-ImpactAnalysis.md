---
# Impact Analysis Document: Kitchensink Project Migration to Java 21 and Spring Boot

---

## 1. Legacy to Java 21 Mapping

| Legacy Namespace / Package                                | Java 21 Equivalent                                            | Notes                                                                                      |
|-----------------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| org.jboss.as.quickstarts.kitchensink.util                 | org.jboss.as.quickstarts.kitchensink.util                     | Utility classes (e.g., `Resources`) remain with Java SE 21 features; refactor logging to SLF4J with Logback. |
| org.jboss.as.quickstarts.kitchensink.model                | org.jboss.as.quickstarts.kitchensink.model                    | Plain Java 21 classes with modern features such as records or enhanced classes if applicable. Ensure use of modern Java date/time APIs and Optional where appropriate. |
| org.jboss.as.quickstarts.kitchensink.data                 | org.jboss.as.quickstarts.kitchensink.data                     | Refactor JPA entities and repositories using updated Jakarta Persistence 3.1 compatible with Java 21. Use Spring Data JPA. |
| org.jboss.as.quickstarts.kitchensink.service              | org.jboss.as.quickstarts.kitchensink.service                  | Business logic classes refactored to use Java 21 language features and aligned with Spring service models. |
| org.jboss.as.quickstarts.kitchensink.controller           | org.jboss.as.quickstarts.kitchensink.controller               | UI logic adapted to Java 21, potentially redesigning to utilize reactive paradigms if needed with Spring MVC or WebFlux. |
| org.jboss.as.quickstarts.kitchensink.rest                 | org.jboss.as.quickstarts.kitchensink.rest                     | Replace JAX-RS REST constructs with Spring Web MVC or Spring WebFlux controllers supporting Java 21 features. |

---

## 2. Legacy to Spring Boot Mapping

| Legacy Package                                           | Spring Boot Equivalent Component / Approach                   | Migration Notes & Best Practices                                                                                         |
|----------------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| org.jboss.as.quickstarts.kitchensink.util                | `@Component` annotated Spring bean utility classes            | Replace legacy logging with SLF4J via Spring Boot starter. Use Spring DI (@Autowired) and component scanning.               |
| org.jboss.as.quickstarts.kitchensink.model               | Entity classes annotated for Spring Data JPA                  | Use `@Entity`, `@Table` annotations with Hibernate ORM managed by Spring Boot. Leverage Java 21 language enhancements.     |
| org.jboss.as.quickstarts.kitchensink.data                | Spring Data JPA `Repository` interfaces and event publishers  | Migrate to Spring Data repositories (`JpaRepository`, etc.). Utilize Spring Events or ApplicationEventPublisher if needed. |
| org.jboss.as.quickstarts.kitchensink.service             | Spring `@Service` annotated classes                            | Business logic services converted to Spring's stereotype annotations, enabling transaction management and DI.              |
| org.jboss.as.quickstarts.kitchensink.controller          | Spring MVC Controllers annotated with `@Controller`          | Map UI interactions with Spring MVC controllers, leveraging Thymeleaf or REST API endpoints as frontend connectors.        |
| org.jboss.as.quickstarts.kitchensink.rest                | Spring `@RestController` and `@RequestMapping` handlers       | Rewrite JAX-RS resources as Spring Boot REST controllers for native support and improved integration in Spring ecosystem.  |

---

## 3. Risk Register with Severity Levels

| Risk ID | Description                                                     | Affected Package(s)                   | Severity (High/Medium/Low) | Mitigation Strategy                                                                                               |
|---------|-----------------------------------------------------------------|-------------------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------|
| R1      | Namespace migration from `javax.*` to `jakarta.*` causing incompatibilities | All                               | High                       | Use Eclipse Transformer for batch migration; perform automated refactoring and extensive testing.                |
| R2      | JAX-RS REST endpoints incompatible with Spring MVC REST model   | `rest`                             | High                       | Re-implement REST endpoints as Spring `@RestController` handlers; leverage OpenRewrite recipes for automation.   |
| R3      | Legacy JSF UI forms unsupported in Spring Boot                  | `controller`, frontend (not detailed) | Medium                     | Migrate to Spring MVC with Thymeleaf or modern JavaScript frontend frameworks; incremental UI migration advised.  |
| R4      | Legacy persistence entities and repositories with incompatible JPA versions | `data`, `model`                    | High                       | Upgrade to Spring Data JPA with Hibernate ORM 6+, ensuring compatibility with Java 21 and Jakarta Persistence 3.1. |
| R5      | Legacy validation annotations incompatible with updated Hibernate Validator | `model`, `service`                 | Medium                     | Migrate bean validation annotations to latest Hibernate Validator compliant with Spring Boot, Java 21.            |
| R6      | Testing framework incompatibility (JUnit 4 to JUnit 5)           | Test code (not detailed here)      | Medium                     | Shift to JUnit 5 and Spring Boot test support for better integration and maintainability.                        |
| R7      | Embedded server vs standalone server execution differences       | Entire application runtime          | Low                        | Use Spring Boot embedded Tomcat/Jetty with careful environment configuration; validate deployment scenarios.     |

---

## 4. Recommended Migration Patterns Per Component

| Component                        | Recommended Migration Pattern                                     | Rationale                                                                                                     |
|---------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Utility (`util`)                 | Branch-by-Abstraction                                             | Isolate utility code allowing substitution of implementations between legacy and Spring Boot independently.    |
| Domain Model (`model`)           | Branch-by-Abstraction + Strangler Fig                             | Gradually refactor and leverage Java 21 language improvements. Preserve API contracts during migration phases.  |
| Data Layer (`data`)              | Strangler Fig + Anti-Corruption Layer                            | Introduce Spring Data JPA repository interfaces while maintaining legacy repository usage behind an abstraction.|
| Service Layer (`service`)        | Branch-by-Abstraction + Strangler Fig                             | Encapsulate business logic to support migration phase coexistence and incremental refactoring.                  |
| Controller Layer (`controller`)  | Strangler Fig                                                     | Incrementally replace UI logic, decoupling legacy interfaces over time.                                       |
| REST Layer (`rest`)              | Strangler Fig + Anti-Corruption Layer                            | Rewrite REST services to Spring `@RestController`; use anti-corruption layers to separate legacy HTTP APIs.     |

---

## Appendix: Key Migration Recommendations & Tools

- Use **Eclipse Transformer** to automate conversion of legacy `javax.*` namespaces to `jakarta.*` namespaces compatible with Spring Boot 3 and Jakarta EE 9+.
- Employ **OpenRewrite** recipes for automated code refactorings upgrading APIs and package namespaces.
- Leverage **Spring Boot Migrator (SBM)** to streamline configuration and startup migration.
- Substitute **JAX-RS** with Spring MVC/WebFlux REST Controllers.
- Replace legacy **JSF** with Spring MVC combined with Thymeleaf templating or alternative UI frameworks.
- Upgrade persistence layer to **Spring Data JPA** with Hibernate ORM 6+ for Java 21 compliance.
- Migrate validation to **Hibernate Validator 8.x** compatible with Spring Boot 3 and Java 21.
- Switch testing frameworks to **JUnit 5** for modern capabilities and compatibility.
- Adopt **Strangler Fig** incremental migration pattern to minimize downtime.
- Maintain comprehensive documentation and central knowledge base for legacy-modern mappings.
- Establish quality gates and sprint-based auditing for consistent progress monitoring.

---

This Impact Analysis document provides a detailed roadmap for migration of the Kitchensink project from legacy Jakarta EE/Red Hat JBoss EAP architecture to a modern, maintainable Spring Boot 3 application running on Java 21. It addresses namespace and API mappings, identifies risk levels for key components, and prescribes migration patterns tailored per module to ensure a systematic, low-risk modernization journey.

# End of Document.