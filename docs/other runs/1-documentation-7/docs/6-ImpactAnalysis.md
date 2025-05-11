# Impact Analysis Document for Kitchensink Project Modernization to Java 21 and Spring Boot

---

## 1. Legacy → Java 21 Mapping

| Package       | Class Name                | Legacy Technology & Namespace                              | Java 21 Equivalent & Notes                                    |
|---------------|--------------------------|------------------------------------------------------------|---------------------------------------------------------------|
| util          | Resources                | Jakarta EE CDI (`jakarta.enterprise.context`), EntityManager (`jakarta.persistence`), Logger (java.util.logging) | CDI replaced by Spring Dependency Injection, EntityManager remains within Jakarta Persistence 3.1, migrate logger to SLF4J with Logback |
| controller    | MemberController         | JSF (`jakarta.faces.*`), CDI (`@Model`)                    | Replace JSF with Spring MVC controllers, use Spring Beans (`@Controller`), managed through Spring lifecycle and scopes              |
| model         | Member                   | Jakarta Persistence API (`jakarta.persistence.*`), Bean Validation API (`jakarta.validation.*`) | JPA entities compatible with Java 21; validation replaced with Hibernate Validator integrated via Spring Boot                        |
| service       | MemberRegistration       | CDI service layer                                           | Spring `@Service` annotated bean, transaction management with Spring `@Transactional`                                               |
| data          | MemberListProducer       | CDI Producers for injecting collections                     | Use Spring Beans or Spring Data projections to provide collections                                                        |
|               | MemberRepository         | JPA EntityManager-based data access                         | Spring Data JPA interface repository (`JpaRepository`) abstraction layer                                                     |
| rest          | JaxRsActivator           | JAX-RS Application class activating REST endpoints          | Spring Boot auto configuration activates REST automatically; no explicit activator required                                   |
|               | MemberResourceRESTService| JAX-RS REST resource class                                  | Spring Web MVC’s `@RestController` class exposing REST endpoints                                                      |

---

## 2. Legacy → Spring Boot Mapping

| Legacy Component               | Legacy API / Framework                  | Spring Boot Equivalent                                 | Migration Notes                                                                                                   |
|-------------------------------|---------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Resources (util)               | CDI `@Produces`, persistence context  | Spring `@Component` beans, `@Bean` producer methods    | Move resource provisioning to Spring Bean lifecycle management                                                   |
| MemberController (controller) | JSF Managed Bean (`@Model`)           | Spring `@Controller` + Thymeleaf Views                  | JSF lifecycle and scopes replaced by Spring MVC request/session/flow scopes                                       |
| Member (model)                 | JPA Entity (`@Entity`, `@Table`, etc)| Same JPA annotations; Spring Data JPA integration       | Use Spring Data repositories, fully compatible with Java 21                                                      |
| MemberRegistration (service)  | CDI Bean                             | Spring `@Service` with `@Transactional` annotation     | Adjust injection and transactional boundaries                                                                     |
| MemberListProducer, MemberRepository (data)| CDI Producer, JPA EntityManager| Spring Data Repository interfaces (`JpaRepository`)    | Rewrite producers as repositories, leverage Spring Data query methods                                            |
| JaxRsActivator (rest)          | JAX-RS Application class              | Spring Boot auto-configuration                         | No action needed; automatic REST configuration is default in Spring Boot                                          |
| MemberResourceRESTService (rest)| JAX-RS `@Path`, `@GET`, etc        | Spring MVC `@RestController` with `@RequestMapping`   | Change annotation from JAX-RS to Spring MVC, map exceptions and input/output formats accordingly                  |

---

## 3. Risk Register with Severity Levels

| Component                    | Risk Description                                         | Severity Level | Mitigation                                                                                          |
|------------------------------|---------------------------------------------------------|----------------|--------------------------------------------------------------------------------------------------|
| JSF `MemberController` UI     | Loss of JSF lifecycle and `@Model` semantics with Spring MVC | High           | Complete refactor of UI layer to Spring MVC and Thymeleaf; extensive UI testing required           |
| CDI injection and bean scope  | Differences in injection points, bean lifecycle, scopes | Medium         | Refactor to Spring DI patterns; verify scopes & lifecycles; unit testing recommended              |
| JPA Entities (`Member`)       | Possible API differences between Jakarta EE and Spring Data JPA | Medium         | Update imports; test entity behavior; consider Lombok/records for improved Java 21 compatibility     |
| Data Access Layer             | Change from EntityManager-based DAO to Spring Data JpaRepository | Low            | Rewrite repositories; migrate JPQL queries; implement query methods slowly with integration tests  |
| REST Layer                   | Different parameter binding and HTTP method mapping in JAX-RS to Spring | Medium         | Rewrite REST endpoints; adjust exception handling; integration test coverage                        |
| Validation Annotations        | Migration of Bean Validation compatibility                | Low            | Verify constraints run properly; adjust validator setup if necessary                              |
| Logger & Utility             | Java Util Logging vs SLF4J                                 | Low            | Switch to SLF4J with Logback, use OpenRewrite for automated codemods                               |

---

## 4. Recommended Migration Patterns per Component

| Package                | Recommended Migration Patterns                        | Comments                                                                                   |
|------------------------|-----------------------------------------------------|--------------------------------------------------------------------------------------------|
| util                   | Branch-by-Abstraction                                | Abstract and inject via Spring beans; maintain compatibility interfaces                     |
| controller             | Strangler Fig + Branch-by-Abstraction                | Slowly replace JSF MVC with Spring MVC controllers; run both side by side                   |
| model                  | Automated Refactoring (OpenRewrite)                   | Bulk adjust imports and annotations for compatibility; refactor to Java 21 idioms          |
| service                | Branch-by-Abstraction                                | Abstract business logic interfaces; provide parallel implementations                       |
| data                   | Branch-by-Abstraction + OpenRewrite                   | Migrate EntityManager DAO to Spring Data Repositories gradually                            |
| rest                   | Strangler Fig                                       | Parallel REST endpoints in JAX-RS and Spring MVC; migrate consumers incrementally           |

---

## Summary

The Kitchensink project modernization involves significant transitions in UI, DI, persistence, and REST layers, but well-defined mappings to Java 21 and Spring Boot 3+ constructs exist. Migration risks are mostly medium or high for UI and CDI lifecycle differences but manageable via tested patterns and automation.

Careful phased replacement leveraging Strangler Fig and Branch-by-Abstraction patterns, combined with codebase-wide automated tool support like OpenRewrite, will deliver a safe, scalable modernization to Java 21 with Spring Boot's mature ecosystem.

---

This completes the full Impact Analysis with legacy-to-modern mappings, risk registers, and migration guidance for the Kitchensink modernization initiative.