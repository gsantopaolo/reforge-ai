---
# Technology Inventory and Migration Notes for kitchensink Java Project

### 1. jakarta.enterprise: jakarta.enterprise.cdi-api
- Current Version & Usage: 4.0.1.redhat-00001 (provided)
- Usage Context: Core CDI (Contexts and Dependency Injection) API for dependency injection and lifecycle management.
- Migration Notes to Spring Boot Java 21:
  - Spring Framework 6 / Spring Boot 3 supports Jakarta EE 9 namespaces (`jakarta.*`).
  - Replace CDI annotations (`@Inject`, `@Named`, `@RequestScoped`, etc.) with Spring equivalents (`@Autowired`, `@Component`, `@Scope("request")`, etc.).
  - Use Spring’s `@Configuration` and `@Bean` for producer methods instead of CDI producers.
  - Pay attention to lifecycle changes and proxying semantics differences.
- References:
  - https://speakerdeck.com/ivargrimstad/from-spring-boot-2-to-spring-boot-3-with-java-21-and-jakarta-ee-4c860ab6-7721-42dc-bee0-1af675422dd5 (slides)
  - https://stackoverflow.com/questions/9556532/migrating-cdi-ejb-annotations-to-spring-annotations
  - https://jakartablogs.ee/ (general guidance on migration)

### 2. junit:junit
- Current Version & Usage: 4.13.1 (test)
- Usage Context: Unit testing framework.
- Migration Notes:
  - Consider migrating to JUnit 5 (Jupiter) which has better integration with Spring Boot 3 and Java 21.
  - JUnit 4 support continues, but JUnit 5 has improved features and native support in modern build tools.
- References:
  - https://junit.org/junit5/docs/current/user-guide/#overview

### 3. org.hibernate.orm: hibernate-jpamodelgen
- Current Version & Usage: 6.2.13.Final-redhat-00001 (provided)
- Usage Context: Hibernate JPA static metamodel generator for type-safe criteria queries.
- Migration Notes:
  - Hibernate 6+ is compatible with Jakarta Persistence 3.1.
  - Validate that persistence.xml or equivalent config uses `jakarta.persistence` namespace.
  - Migration to Spring Boot 3 includes upgrading to Hibernate 6 and adapting to jakarta namespaces.
- References:
  - https://hibernate.org/orm/releases/6.2/
  - https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#howto.spring-data.jpa.config.hibernates

### 4. jakarta.activation: jakarta.activation-api
- Current Version & Usage: 2.1.2.redhat-00001 (provided)
- Usage Context: JavaBeans Activation Framework for data type handling.
- Migration Notes:
  - Supported fully in Java 21 through Jakarta updates.
  - Ensure Java 21 module system includes activation if applicable.
- References:
  - https://javaee.github.io/jaf/

### 5. org.hibernate.validator: hibernate-validator
- Current Version & Usage: 8.0.0.Final-redhat-00001 (provided)
- Usage Context: Bean validation.
- Migration Notes:
  - Hibernate Validator 8 aligns with Jakarta Bean Validation 3 API.
  - Spring Boot 3 uses Jakarta Bean Validation support.
  - Confirm that validation annotations use `jakarta.validation` package.
- References:
  - https://hibernate.org/validator/
  - https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#validation-beanvalidation (Spring integration)

### 6. jakarta.validation: jakarta.validation-api
- Current Version & Usage: 3.0.2.redhat-00001 (provided)
- Usage Context: Bean validation API.
- Migration Notes:
  - As above, migrate to Jakarta Bean Validation API namespace.
  - Use Spring Boot's validated support and custom validator beans as needed.
- References:
  - https://jakarta.ee/specifications/validation/3.0/

### 7. org.hibernate.validator: hibernate-validator-annotation-processor
- Current Version & Usage: 8.0.0.Final-redhat-00001 (provided)
- Usage Context: Annotation processor for Bean Validation annotations during compilation.
- Migration Notes:
  - Compatible with Jakarta Validation APIs.
  - Ensure build tools are configured to use Jakarta namespace.
- References:
  - https://hibernate.org/validator/documentation/

### 8. jakarta.persistence: jakarta.persistence-api
- Current Version & Usage: 3.1.0.redhat-00001 (provided)
- Usage Context: JPA API for persisting entities.
- Migration Notes:
  - Migrate all references from `javax.persistence` to `jakarta.persistence`.
  - Spring Boot 3 and Hibernate 6 support JPA 3.1 and Jakarta namespace.
  - Validate persistence configuration and entity annotations.
- References:
  - https://jakarta.ee/specifications/persistence/3.1/

### 9. org.jboss.arquillian.junit: arquillian-junit-container
- Current Version & Usage: 1.7.0.Final (test)
- Usage Context: Arquillian JUnit integration for in-container testing.
- Migration Notes:
  - Testing migration may require updating to compatible Arquillian versions supporting Java 21.
  - Consider alternative Spring Boot testing frameworks like Spring Boot Test for integration tests.
- References:
  - https://arquillian.org/

### 10. jakarta.annotation: jakarta.annotation-api
- Current Version & Usage: 2.1.1.redhat-00001 (provided)
- Usage Context: Common annotation API.
- Migration Notes:
  - Migrate to Jakarta Annotation API namespace.
  - Spring supports alternative lifecycle and component annotations.
- References:
  - https://jakarta.ee/specifications/annotation/2.1/

### 11. jakarta.ejb: jakarta.ejb-api
- Current Version & Usage: 4.0.1.redhat-00001 (provided)
- Usage Context: EJB API for enterprise beans.
- Migration Notes:
  - Spring Boot discourages EJBs; migration to Spring-managed components or Spring Boot starters preferred.
  - Replace EJB services with Spring `@Service` components; use Spring Data repositories instead of EJB QL.
- References:
  - https://spring.io/guides
  - https://stackoverflow.com/questions/9556532/migrating-cdi-ejb-annotations-to-spring-annotations

### 12. jakarta.faces: jakarta.faces-api
- Current Version & Usage: 4.0.1.redhat-00001 (provided)
- Usage Context: JavaServer Faces front-end framework.
- Migration Notes:
  - Spring Boot does not natively support JSF; consider porting UI to Spring MVC with Thymeleaf or alternative frameworks.
  - If retaining JSF, look for Spring-boot-compatible JSF starter libraries.
- References:
  - https://www.baeldung.com/spring-jsf-integration
  - https://stackoverflow.com/questions/44036925/jsf-in-spring-boot-applications

### 13. jakarta.ws.rs: jakarta.ws.rs-api
- Current Version & Usage: 3.1.0.redhat-00001 (provided)
- Usage Context: JAX-RS Java REST API.
- Migration Notes:
  - Spring Boot favors Spring Web MVC or Spring WebFlux for REST APIs.
  - Migrate REST service classes from JAX-RS annotations (`@Path`, `@GET`) to Spring MVC (`@RestController`, `@GetMapping`).
- References:
  - https://spring.io/guides/gs/rest-service/
  - https://www.baeldung.com/spring-rest-jax-rs

### 14. jakarta.xml.bind: jakarta.xml.bind-api
- Current Version & Usage: 4.0.0.redhat-00001 (provided)
- Usage Context: JAXB for XML binding.
- Migration Notes:
  - JAXB support in Java 21 requires adding external dependencies.
  - Use Jakarta JAXB libraries and configure modules as needed.
- References:
  - https://javaee.github.io/jaxb-v2/

### 15. jakarta.json: jakarta.json-api
- Current Version & Usage: 2.1.2.redhat-00001 (test)
- Usage Context: JSON-P API for JSON processing.
- Migration Notes:
  - Jakarta JSON-P is compatible with Java 21.
  - Spring Boot has native JSON support via Jackson or JSON-B; consider migrating to preferred JSON processing libraries.
- References:
  - https://eclipse-ee4j.github.io/jsonp/

### 16. org.eclipse.parsson: parsson
- Current Version & Usage: 1.1.2.redhat-00001 (test)
- Usage Context: JSON-P implementation.
- Migration Notes:
  - Ensure compatibility with Jakarta JSON-P APIs.
  - Consider migrating to Jackson or other libraries favored by Spring Boot.
- References:
  - https://www.eclipse.org/parsson/

---

This inventory details the current component versions and their usage within the kitchensink project, outlines necessary migration notes when moving to Spring Boot and Java 21, and provides reputable references for best practices and further reading.

Migration emphases:
- Adapting Jakarta EE 9 namespace changes (`javax.*` to `jakarta.*`).
- Replacing Java EE specific APIs and patterns (EJB, JAX-RS, CDI) with Spring Boot idiomatic equivalents.
- Upgrading supporting libraries to versions compatible with Spring Boot 3 and Java 21.
- Testing strategies evolution away from Arquillian/JUnit 4 to modern frameworks.

This document should guide development teams in prioritizing components during phased migration and serve as a baseline for sprint-level task planning and quality audits.