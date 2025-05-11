---

# Impact Analysis Document for kitchensink Project Migration to Java 21 and Spring Boot

## 1. Legacy → Java 21 Mapping

| Legacy Package                                      | Java 21 Equivalent                     | Notes                                    |
|---------------------------------------------------|--------------------------------------|------------------------------------------|
| `org.jboss.as.quickstarts.kitchensink.util`       | `org.jboss.as.quickstarts.kitchensink.util` | Utilities largely unchanged; Java 21 standard APIs applied for logging, concurrency enhancements if used |
| `org.jboss.as.quickstarts.kitchensink.model`      | Same package, updated Java 21 language features | Domain Model remains, enhanced with Java 21 features such as Records or sealed classes where applicable |
| `org.jboss.as.quickstarts.kitchensink.data`       | Same package, refactored for JPA and Spring Data JPA compatibility | JPA EntityManager replaced by Spring Data JPA Repositories, using modern JPA version (Jakarta Persistence 3.1) compatible with Java 21 |
| `org.jboss.as.quickstarts.kitchensink.service`    | Same package with Spring @Service annotations replacing EJB | Business logic remains, but moved to Spring-managed beans compatible with Java 21 |
| `org.jboss.as.quickstarts.kitchensink.controller` | Same package with Spring MVC controllers | Java 21 supports Spring MVC as primary web framework replacing legacy MVC or servlet approaches |
| `org.jboss.as.quickstarts.kitchensink.rest`       | Same package, using Spring Web MVC REST Controllers | JAX-RS replaced by Spring MVC annotations with Java 21 compatibility |
| `org.jboss.as.quickstarts.kitchensink.test`       | Same package, upgraded to JUnit 5 with Spring Boot Test | Test modernization to JUnit Jupiter and Spring TestContext support |

## 2. Legacy → Spring Boot Mapping

| Legacy Package                                      | Spring Boot Equivalent                                  | Migration Notes                                      |
|---------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------|
| `util.Resources`                                  | Spring Boot logging via SLF4J and Logback              | Replace legacy logging with SLF4J/Logback config    |
| `model.Member`                                    | Spring Boot entity class managed by Spring Data JPA   | Add Spring Data JPA annotations, enable repository support |
| `data.MemberRepository`                           | Spring Data JPA Repository interface extending JpaRepository<Member, Long> | Replace `EntityManager` usage with Spring Data repository methods |
| `data.MemberListProducer`                         | Bean or Service for member collection production       | Refactor producer logic as Spring bean               |
| `service.MemberRegistration`                      | Spring @Service annotated class, with @Transactional   | Replace EJB business logic with Spring components   |
| `controller.MemberController`                      | Spring MVC @Controller or @RestController              | Map servlet-based controllers to Spring MVC          |
| `rest.JaxRsActivator`                             | Spring Boot auto-configuration and main application enabling Spring MVC REST support | Drop JAX-RS Activator in favor of Spring Boot mechanisms |
| `rest.MemberResourceRESTService`                   | Spring MVC REST @RestController                          | Convert JAX-RS annotations to Spring MVC equivalents  |
| `test.*`                                          | Tests using @SpringBootTest and JUnit 5 Jupiter        | Migrate from Arquillian/JUnit 4 to Spring Boot testing stack |

## 3. Risk Register

| Risk ID | Component/Package             | Removed or Changed Construct                   | Potential Impact                            | Severity  | Mitigation Strategy                               |
|---------|------------------------------|------------------------------------------------|---------------------------------------------|-----------|--------------------------------------------------|
| R1      | data.MemberRepository         | EntityManager injection replaced by repository overlays | Query and data access implementation changes | High      | Refactor data access to Spring Data JPA repositories; comprehensive testing of queries |
| R2      | rest.JaxRsActivator           | JAX-RS Activator deprecated; replaced by Spring Boot auto-configuration | REST service activation may fail             | Medium    | Replace with Spring Boot @SpringBootApplication and use Spring MVC                               |
| R3      | rest.MemberResourceRESTService| JAX-RS annotations (@Path, @GET) removed       | Endpoint mappings must be converted           | High      | Refactor REST endpoints to Spring MVC annotations; validate routes                             |
| R4      | service.MemberRegistration    | EJB removal; transactional features via Spring  | Transaction management changes                 | High      | Use Spring @Transactional, adjust transaction boundaries and propagation                       |
| R5      | CDI injections (`@Inject`)   | CDI replaced with Spring DI (`@Autowired`)     | Dependency injection errors                    | Medium    | Replace annotations; ensure component scanning enabled                                        |
| R6      | Test Classes                  | Arquillian and JUnit 4 replaced with JUnit 5 and Spring Test | Test framework incompatibility                | Medium    | Migrate tests to use Spring Boot testing annotations, JUnit 5 Jupiter                         |
| R7      | Validation                   | Legacy Hibernate Validator replaced with Spring Boot starter | Validation annotations mostly compatible      | Low       | Configure Spring validation starter properly                                                  |
| R8      | Legacy Jakarta namespace     | javax.* to jakarta.* upgrade                     | API incompatibilities                          | High      | Utilize OpenRewrite scripts, code scanning to replace imports                                 |

## 4. Recommended Migration Patterns per Component

| Package                    | Recommended Migration Pattern       | Description and Rationale                                                            |
|----------------------------|-----------------------------------|--------------------------------------------------------------------------------------|
| All packages (general)     | **Strangler Fig Pattern**          | Incrementally replace legacy components with Spring Boot equivalents, enabling coexistence during migration |
| Data and Persistence       | **Branch-by-Abstraction**          | Introduce repository abstractions to allow switching between EntityManager and Spring Data JPA implementations |
| REST Layer                 | **Strangler Fig / Branch-by-Abstraction** | Map JAX-RS resources gradually to Spring MVC REST controllers; route traffic to new endpoints selectively |
| Business Logic (Service)   | **Branch-by-Abstraction**          | Gradually refactor EJBs to Spring @Service beans with transactional support, enabling fallbacks as needed |
| Testing                   | **Full Replacement/Upgrade**        | Migrate tests to JUnit 5 and Spring Boot Test all at once to ensure full compatibility in CI pipelines |
| Utilities and Logging     | **Encapsulate & Replace**            | Swap legacy logging frameworks to SLF4J-backed Spring Boot starters transparently       |

---

# Summary

This Impact Analysis provides thorough mappings of all legacy packages, classes, and namespaces to Java 21 standards and Spring Boot paradigms. It catalogs removed/changed constructs that pose migration risks, classifying them by severity to prioritize remediation efforts. Migration patterns such as Strangler Fig and Branch-by-Abstraction empower a phased, low-risk transition, allowing legacy and modern components to coexist while migration proceeds. The adoption of automated tools like OpenRewrite for namespace changes and refactorings, combined with sound architectural practices detailed here will ensure a successful modernization of the kitchensink Java project to the cutting-edge Java 21 and Spring Boot environment.

# References

- Official Jakarta EE 10 and Spring Boot 3 migration guides.
- OpenRewrite migration recipes.
- Red Hat Migration Toolkit for Runtimes documentation.
- Community migration case studies and industry best practices.

---

This document is intended as a core artifact guiding the modernization engineering efforts of the kitchensink application.