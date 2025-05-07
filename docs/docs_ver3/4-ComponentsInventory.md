# Kitchensink Technology Inventory and Migration to Spring Boot on Java 21

---

## 1. Jakarta EE APIs and Specifications

| Technology                       | Current Version               | Usage Context                                     | Migration Notes & Best Practices                                                                                      |
|---------------------------------|-------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Jakarta CDI (jakarta.enterprise.cdi-api) | 4.0.1.redhat-00001            | Dependency Injection, Context and Lifecycle      | Migration path involves updating namespaces from `javax.*` to `jakarta.*`. Spring Boot 3 natively supports Jakarta EE 9 namespaces. Use Spring DI annotations (`@Component`, `@Autowired`) when migrating to Spring based architecture. Use Eclipse Transformer for automated code refactoring of namespaces. |
| Jakarta Persistence (jakarta.persistence-api) | 3.1.0.redhat-00001            | ORM & Database Interaction via JPA               | Replace Jakarta Persistence config with Spring Data JPA. Ensure use of Hibernate compatible with Java 21 and Spring Boot 3. Use annotation replacements and review entity scanning. |
| Jakarta REST (jakarta.ws.rs-api) | 3.1.0.redhat-00001            | RESTful web services                              | Consider Spring MVC or Spring WebFlux for REST endpoints. Rewrite JAX-RS resources as Spring Controllers and Services. |
| Jakarta Validation (jakarta.validation-api) | 3.0.2.redhat-00001            | Bean validation                                  | Use Spring Boot's native support with Hibernate Validator 8.x compatible with Java 21. Migrate validation annotations accordingly. |
| Jakarta Faces (jakarta.faces-api) | 4.0.1.redhat-00001            | JSF web UI framework                              | Migrate to Spring MVC with Thymeleaf or alternative modern UI frameworks, as Spring Boot does not support JSF natively. Use Spring Boot starters for MVC and Thymeleaf integration. |

---

## 2. Hibernate Components

| Technology                       | Current Version               | Usage Context                                     | Migration Notes & Best Practices                                                                                      |
|---------------------------------|-------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Hibernate Validator             | 8.0.0.Final-redhat-00001       | Bean validation implementation                    | Use same version or newer Hibernate Validator compatible with Spring Boot 3 and Java 21. Support integrated via Spring Boot starter. |
| Hibernate JPA Model Gen         | 6.2.13.Final-redhat-00001      | Compile-time metamodel generator for JPA entities| Use compatible version or migrate to supported annotation processors in Spring ecosystem. |
| Hibernate ORM (via dependencies) | Managed transitively           | JPA provider (ORM)                               | Ensure Hibernate ORM version is compatible with Jakarta Persistence API 3.x and Java 21. Spring Boot 3 manages this internally. |

---

## 3. Testing Frameworks

| Technology                       | Current Version               | Usage Context                                     | Migration Notes & Best Practices                                                                                      |
|---------------------------------|-------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| JUnit                          | 4.13.1                        | Unit testing framework                           | Migrate to JUnit 5 (JUnit Jupiter) for better Java 21 compatibility and new features. Spring Boot 3 supports JUnit 5 by default. |
| Arquillian                    | 1.7.0.Final                   | Container managed integration testing            | Evaluate migration to Spring Boot Test support with embedded containers or test slices; Arquillian setups may not be compatible directly. |

---

## 4. Utility and Supporting Libraries

| Technology                       | Current Version               | Usage Context                                     | Migration Notes & Best Practices                                                                                      |
|---------------------------------|-------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Jakarta Annotation API          | 2.1.1.redhat-00001             | General Java EE annotations support               | Ensure annotation imports migrated from `javax.annotation` to `jakarta.annotation` namespace per Jakarta EE 9 standards. |
| JAXB API and Runtime (jakarta.xml.bind) | 4.0.0.redhat-00001            | XML Binding                                      | Spring Boot 3 supports JAXB via external dependencies; configure accordingly, upgrade to Jakarta versions. |
| Jakarta Activation API          | 2.1.2.redhat-00001             | MIME Data Handling                               | Migrate with Jakarta namespace changes, add explicit dependencies in Spring Boot if needed. |
| JSON Processing API (jakarta.json-api) | 2.1.2.redhat-00001            | JSON-P API for JSON Handling                      | Use Jakarta JSON Processing APIs compatible with Java 21 along with Spring Boot starters or Jackson library as preferred. |

---

## 5. Runtime Environment

| Technology                       | Current Version               | Usage Context                                     | Migration Notes & Best Practices                                                                                      |
|---------------------------------|-------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Java SE                        | Java 8 (current)                | Java runtime environment                          | Upgrade all code and dependencies to support Java 21 SE, which introduces language features and JVM changes. Use Spring Boot 3 which requires Java 17+. |
| Application Server             | JBoss EAP 8.0                   | Jakarta EE Certified runtime                      | Spring Boot apps typically run standalone with embedded server (Tomcat/Jetty/Undertow). Consider migration to Spring Boot’s embedded server or deploy on Spring Boot supported containers. |

---

## Migration Best-Practice References

- Use Eclipse Transformer tool (https://github.com/eclipse/transformer) for automated migration of `javax.*` to `jakarta.*` namespaces.
- Follow Spring Framework 6 and Spring Boot 3+ upgrade notes for Java 21 support: https://spring.io/blog/2023/11/01/spring-framework-6-0-goes-ga
- Leverage OpenRewrite recipes for automated codebase refactoring to Java 21 and Spring Boot 3: https://docs.openrewrite.org/recipes/java/spring/boot3/
- Replace JSF UI with Spring MVC and Thymeleaf templates for a maintainable modern UI.
- Replace JAX-RS REST services with Spring MVC REST controllers or Spring WebFlux handlers.
- Migrate test suites to JUnit 5 and Spring Boot test support for container-less testing.
- Review and upgrade all dependencies to versions compatible with Jakarta EE 9+ and Java 21.

This Technology Inventory ensures visibility on current technologies and practical actionable steps and references for smooth migration to Spring Boot on Java 21.

If you want, I can expand the inventory with additional details or walk you through individual migration paths in more depth.

# End of Inventory and Migration Notes