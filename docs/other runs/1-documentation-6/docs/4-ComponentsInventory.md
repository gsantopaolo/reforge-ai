---

# Technology Inventory and Migration Notes for Kitchensink Java EE Example

| Component / Library / Framework | Version                                   | Usage Context                                                                                                   | Migration Notes & Best Practice References                                                                                                           |
|---------------------------------|-------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Jakarta CDI (jakarta.enterprise.cdi-api) | 4.0.1.redhat-00001                        | Used for Dependency Injection and Contexts in all layers, e.g. @Inject in MemberController, MemberRegistration, etc. | Spring Boot uses its own DI via Spring Framework. Replace `@Inject` with Spring `@Autowired` or constructor injection. Ref: [Spring Migration](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans) |
| Jakarta Persistence (JPA, jakarta.persistence-api) | 3.1.0.redhat-00001                        | Entity mapping of Member class, persistence management with EntityManager in MemberRepository & MemberRegistration | Use Spring Data JPA starter for repo layers. Adapt EntityManager injections to Repository interfaces extending JpaRepository.                       |
| Jakarta Bean Validation (jakarta.validation-api) | 3.0.2.redhat-00001                        | Bean validation annotations on Member entity, validation injected in REST service                              | Use Spring Validation with Hibernate Validator starter. Replace javax validation annotations with jakarta namespace if needed.                      |
| Hibernate Validator | 8.0.0.Final-redhat-00001                  | Bean validation provider integrated with Jakarta Validation API                                                | Hibernate Validator integrates well with Spring Boot's validation. Ensure compatibility with version and Jakarta namespace.                          |
| Jakarta RESTful WS (jakarta.ws.rs-api) | 3.1.0.redhat-00001                        | RESTful API layer in MemberResourceRESTService using JAX-RS annotations and injection                          | Spring Boot REST controllers replace JAX-RS. Use `@RestController`, `@GetMapping`, etc. Migrate resources accordingly.                              |
| Jakarta Faces (JSF) | 4.0.1.redhat-00001                         | UI layer in MemberController, managing UI interactions                                                         | Spring Boot typically uses Spring MVC + Thymeleaf or other templating engines instead of JSF. Complete rewrite of UI layer recommended.              |
| Jakarta EJB (jakarta.ejb-api) | 4.0.1.redhat-00001                        | Business logic in MemberRegistration as Stateless EJB                                                          | Replace EJBs with Spring @Service components. Stateless session beans map to plain Spring services.                                                 |
| Jakarta Annotations (jakarta.annotation-api) | 2.1.1.redhat-00001                        | Various annotations used throughout                                                                              | Most annotations have Spring equivalents or are supported.                                                                                           |
| Jakarta JSON (jakarta.json-api) | 2.1.2.redhat-00001                        | JSON handling in REST endpoints                                                                                  | Spring Boot uses Jackson by default for JSON processing. Adjust JSON bindings accordingly.                                                          |
| JUnit 4 | 4.13.1                                       | Unit and integration tests                                                                                        | Upgrade to JUnit 5 recommended for new Spring Boot projects.                                                                                         |
| Arquillian | 1.7.0.Final                                    | Integration testing framework                                                                                     | May be deprecated in favor of Spring Boot Test with embedded containers or mocks.                                                                    |

---

# Migration Pathway Highlights and Best Practice References

- **Migration Toolkit for Runtimes (MTR)** by Red Hat: Rule-based tool assisting Java EE apps migration. Useful for preliminary impact analysis and automated code refactoring. https://docs.redhat.com/en/documentation/migration_toolkit_for_runtimes/

- **Spring Boot Migrator (SBM)**: Automated utility to convert JAX-RS, EJB, JMS-based apps to Spring Boot. Reduces manual refactoring effort. https://www.infoq.com/news/2022/09/spring-boot-migrator/

- **Eclipse Transformer**: Effective for migrating javax.* to jakarta.* namespace changes, crucial for Jakarta EE 9+ and Spring Boot 3+. https://github.com/eclipse/transformer

- **OpenRewrite Migration Recipes**: Scripts and tools to automate codebase upgrades for Spring Boot 3, Jakarta EE 9, and Java 17/21. https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_0

- **General Best Practices**:
  - Migrate framework dependencies first, adjusting Maven coordinates for Spring Boot starters and updated Jakarta namespaces.
  - Replace EJB business logic with Spring @Service annotated classes.
  - Replace JPA EntityManager usage with Spring Data JPA repositories.
  - Convert JAX-RS REST endpoints to Spring MVC REST controllers using `@RestController`.
  - Refactor JSF UI to Spring MVC (or modern SPA framework) views as needed.
  - Upgrade test frameworks to Spring Boot Test support and JUnit 5.
  - Use Java 21 LTS with latest Spring Boot 3.x for full language and runtime benefits.
  - Before full migration, consider modularizing codebase for incremental changes and regression testing.

---

This completes the comprehensive technology inventory along with migration guidance for transforming the Kitchensink Java EE application to Spring Boot on Java 21.

Please let me know if you want me to prepare detailed module-level migration checklists or schedules.