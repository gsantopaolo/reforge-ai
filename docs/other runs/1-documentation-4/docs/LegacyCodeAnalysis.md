```
# Modernization Incidents List

## Deprecated APIs Usage
1. **Jakarta EE API Usage:**
   - **API:** `jakarta.enterprise.cdi-api` version 4.0.1.redhat-00001
   - **Status:** Ensure that no deprecated features are utilized in this version. It should be validated against the Jakarta EE specifications.

2. **Hibernate Validator:**
   - **API:** `hibernate-validator` version 8.0.0.Final-redhat-00001 
   - **Status:** Check and replace deprecated validation annotations as of this version.

3. **Jakarta Transaction API:**
   - **API:** `jakarta.transaction-api` version 2.0.1.redhat-00002
   - **Status:** Verify any deprecated transaction management practices that may exist in older frameworks.

## Library Upgrade Needs
1. **Jakarta Activation API:**
   - **Current Version:** 2.1.2.redhat-00001
   - **Upgrade Recommendation:** Investigate latest versions to align with Jakarta specifications.

2. **Hibernate ORM:**
   - **Current Version:** 6.2.13.Final-redhat-00001
   - **Recommendation:** Always check Hibernate release notes for deprecated methods and class usages based on the latest stable version.

3. **JUnit:**
   - **Current Version:** 4.13.1
   - **Upgrade Recommendation:** It is advisable to upgrade to JUnit 5 for enhanced features including better support for newer Java versions.

## Migration Blockers
1. **Arquillian Container API:**
   - **Current Version:** 1.7.0.Final
   - **Status:** Ensure migration to newer Arquillian versions if outdated features or APIs that have been replaced exist.

2. **Dependency upon `jboss-eap` profiles:**
   - **Current Version:** 8.0.0.GA
   - **Status:** Depending on JBoss EAP within the project can lead to potential conflicts with the evolution of external libraries. Review the compatibility regularly.

3. **Potential Scope Limitations:**
   - **Various Libraries with `provided` Scope:**
   - **Status:** Ensure that all `provided` dependencies are indeed available in the runtime, especially in production environments, to avert runtime exceptions.

## Additional Recommendations
- Conduct a full scan of the codebase to identify any deprecated calls or classes directly impacting application functioning. Utilize static analysis tools that are compatible with current Java standards.
- Set up integration tests to ensure that any changes or upgrades introduced do not break existing functionalities.
- Maintain communication within development teams regarding ongoing assessments and updates to dependencies to uphold best practices in software maintenance.
```