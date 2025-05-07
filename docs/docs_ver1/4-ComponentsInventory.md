# Technology Inventory and Migration Notes for Kitchensink Java Project

---

## Core Components and Frameworks Inventory

### 1. Jakarta Enterprise Edition (Jakarta EE) APIs and Frameworks

| Artifact | Version | Usage Context |
| -------- | ------- | ------------- |
| jakarta.enterprise.cdi-api | 4.0.1.redhat-00001 | CDI for dependency injection and context management. Used throughout layers for DI. |
| jakarta.persistence-api | 3.1.0.redhat-00001 | JPA for ORM and data persistence. Used in data and model layers. |
| jakarta.validation-api | 3.0.2.redhat-00001 | Bean validation API. Used for entity validation. |
| jakarta.ws.rs-api | 3.1.0.redhat-00001 | JAX-RS RESTful services API. Used in REST layer components. |
| jakarta.faces-api | 4.0.1.redhat-00001 | JSF user interface framework. Used in controller for UI interactions. |
| jakarta.ejb-api | 4.0.1.redhat-00001 | Enterprise Java Beans API, likely for business logic components. |
| jakarta.annotation-api | 2.1.1.redhat-00001 | Standard annotations for Jakarta EE components. |

### 2. Hibernate ORM and Validator

| Artifact | Version | Usage Context |
| -------- | ------- | ------------- |
| hibernate-jpamodelgen | 6.2.13.Final-redhat-00001 | JPA static metamodel generator, used for type-safe criteria queries. |
| hibernate-validator | 8.0.0.Final-redhat-00001 | Bean validation provider implementation. |

### 3. Other APIs and Utilities

| Artifact | Version | Usage Context |
| -------- | ------- | ------------- |
| jakarta.activation-api | 2.1.2.redhat-00001 | For activation framework, often used in JAXB etc. |
| jakarta.xml.bind-api | 4.0.0.redhat-00001 | JAXB APIs, used for XML binding. |
| jakarta.json-api | 2.1.2.redhat-00001 | JSON Processing API. May be used in REST components. |
| jakarta.inject-api | 2.0.1.redhat-00001 | Dependency injection standard annotations. |
| junit | 4.13.1 | Test scope for unit tests. |
| org.jboss.arquillian.junit | 1.7.0.Final | Test scope for integration testing with Arquillian. |

---

## Migration Pathways and Best Practices to Spring Boot on Java 21

### General Notes:

- Spring Boot 3.x supports Java 17+ and officially supports Java 21 as of Spring Boot 3.2/6.1.
- Jakarta EE namespaces changed from `javax.*` to `jakarta.*` from Jakarta EE 9 onwards. Spring Framework 6 and Spring Boot 3 support these new namespaces aligning with Jakarta EE 9+.
- Major migration involves replacing Jakarta EE APIs and annotations with Spring Boot equivalents. Business logic can often be adapted with smaller changes.
- Component model changes: CDI replaced by Spring's dependency injection; JPA usage remains but with Spring Data repositories; REST endpoints replaced with Spring MVC or WebFlux controllers.
- JSF based UI likely to be replaced with Spring-supported technologies, e.g., Thymeleaf or Spring MVC views.
- Hibernate persistence layer maps well into Spring Data JPA repositories.
- Use [OpenRewrite](https://docs.openrewrite.org/) community recipes to automate package namespace changes and dependency upgrades.
- Run a test suite progressively while migrating to ensure smooth transition.

### Detailed Best-Practice Resources:

- [Migrating from Java 8/11 to Java 21, and Spring Boot 2 to 3.2 (Unlogged.io)](https://www.unlogged.io/post/migrating-from-java-8-11-to-java-21-and-spring-boot-2-to-the-latest-spring-boot-3-2)
- [Spring Boot 3.x & Java 21 — Simplistic Migration Handbook](https://blog.stackademic.com/spring-boot-3-x-java-21-simplistic-migration-handbook-d93053978d27)
- [Migration Guide: Spring Boot 2.7.7 to Spring Boot 3.2.4 (Medium)](https://m-shahab-rauf.medium.com/migration-guide-spring-boot-2-7-7-to-spring-boot-3-2-4-8d0589e08e5a)
- [Spring Boot 3.2 and Spring Framework 6.1 Add Java 21 Support (InfoQ)](https://www.infoq.com/articles/spring-boot-3-2-spring-6-1/)
- [Best Practices To Deal With Javax to Jakarta Migration (DZone)](https://dzone.com/articles/best-practices-to-deal-with-javax-to-jakarta-migra)
- Use Eclipse Transformer or OpenRewrite to automate javax.* to jakarta.* namespace changes.

---

## Summary Table

| Technology | Current Version | Usage Context | Migration Notes | References |
|------------|-----------------|---------------|-----------------|------------|
| Jakarta EE APIs (e.g., jakarta.enterprise.cdi-api) | 4.0.1.redhat-00001 | Core DI, REST, persistence, validation | Replace with Spring Boot 3+ equivalents; match jakarta.* namespaces | Above URLs |
| Hibernate ORM/JPA | 6.2.13, 8.0.0.Final for validator | ORM persistence layer | Integrate with Spring Data JPA and spring-boot-starter-data-jpa | Above URLs |
| JSF (jakarta.faces-api) | 4.0.1.redhat-00001 | UI controller | Replace UI and controller with Spring MVC/WebFlux or Thymeleaf | Above URLs |
| JUnit | 4.13.1 | Unit tests | Upgrade to JUnit 5 Jupiter; adapt tests to Spring test framework if needed | Above URLs |
| Arquillian Test | 1.7.0.Final | Integration tests | Reassess test strategy, possibly migrate to Spring Boot Test | Above URLs |

---

This completes the technology inventory with usage context and migration best-practice notes for the kitchensink project modernizing to Spring Boot on Java 21.

Please let me know if you want detailed migration steps for each individual component or assistance with automated tool recommendations.