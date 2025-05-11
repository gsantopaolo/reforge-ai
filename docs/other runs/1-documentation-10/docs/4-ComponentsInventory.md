Technology Inventory for kitchensink Java Project Migration to Spring Boot on Java 21:

1. jakarta.enterprise.cdi-api (4.0.1)
- Usage: Dependency Injection (CDI)
- Migration Notes:
  * Replace CDI injections with Spring's @Autowired and @Component annotations.
  * Consider Weld CDI integration if advanced CDI features are needed.
  * Update namespace from javax.* to jakarta.*.
- References:
  * https://jakarta.ee/specifications/cdi/4.0/
  * https://docs.openrewrite.org/recipes/java/migrate/jakarta/javaxinjectmigrationtojakartainject
  * https://stackoverflow.com/questions/46862500/equivalent-of-javax-enterprise-inject-instance-in-spring-boot-for-dynamic-inject

2. jakarta.persistence-api (3.1.0)
- Usage: Java Persistence API for ORM
- Migration Notes:
  * Use Spring Data JPA starter for repository abstraction.
  * Refactor EntityManager usage to Spring repositories.
  * Verify Hibernate versions compatible with Java 21.
- References:
  * https://docs.spring.io/spring-data/jpa/docs/current/reference/html/
  * https://github.com/spring-projects/spring-data-jpa

3. jakarta.ws.rs-api (3.1.0)
- Usage: REST API with JAX-RS
- Migration Notes:
  * Convert JAX-RS annotations (@Path, @GET) to Spring MVC (@RestController, @GetMapping).
  * Use Spring Boot embedded Tomcat/Jetty.
- References:
  * https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc
  * https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#howto-create-a-restful-web-service

4. jakarta.ejb-api (4.0.1)
- Usage: Enterprise Java Beans for business logic
- Migration Notes:
  * Refactor EJBs to Spring @Service/@Component beans.
  * Use Spring @Transactional for transaction management.
- References:
  * https://spring.io/guides/gs/managing-transactions/

5. hibernate-validator (8.0.0)
- Usage: Bean validation
- Migration Notes:
  * Use spring-boot-starter-validation to integrate validation.
  * Replace ValidatorFactory with Spring Validation.
- References:
  * https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#boot-features-validation

6. Testing: junit (4.13.1), arquillian
- Usage: Unit and integration tests
- Migration Notes:
  * Upgrade to JUnit 5 (Jupiter).
  * Use @SpringBootTest for integration tests in place of Arquillian.
- References:
  * https://spring.io/guides/gs/testing-web/
  * https://junit.org/junit5/docs/current/user-guide/

7. Additional Jakarta APIs (activation-api, annotation-api, interceptor-api, inject-api, xml.bind-api, json-api)
- Usage: Jakarta EE core APIs for various functionality
- Migration Notes:
  * Update to Jakarta EE 10 namespaces.
  * Rely on Spring Boot starters to manage transitive dependencies.
- References:
  * https://spring.io/blog/2023/06/30/what-s-new-in-spring-boot-3-2#migrating-to-jakarta-ee-10

This concludes the technology inventory and migration pathways research for the kitchensink project to migrate to Spring Boot on Java 21 successfully.