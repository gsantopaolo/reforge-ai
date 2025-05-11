# Modernization Incidents List

## 1. Deprecated APIs Usage
- **Incident ID:** API_DEPRECATION_01
  - **Affected Library:** `jakarta.enterprise.cdi-api`
  - **Version:** 4.0.1.redhat-00001
  - **Description:** The `javax` namespace has been deprecated and replaced with `jakarta`. Some usages may still point to javax APIs.
  - **Root Cause:** Legacy code using previous versions of Jakarta EE which relied on Java 10 APIs.
  - **Resolution:** Refactor code to utilize the new `jakarta.` namespace.
  - **Status:** Pending

## 2. Required Library Upgrades
- **Incident ID:** LIBRARY_UPGRADE_01
  - **Affected Library:** `hibernate-validator`
  - **Current Version:** 8.0.0.Final-redhat-00001
  - **Upgrade Required To:** 9.0.0 or later for compatibility with Java 11.
  - **Impact:** Affects validation logic and constraints in the application.
  - **Actions Taken:** Prepare dependency for migration in upcoming release.
  - **Status:** Open

## 3. Migration Blockers
- **Incident ID:** MIGRATION_BLOCKER_01
  - **Affected Module:** `arquillian-junit-container`
  - **Version:** 1.7.0.Final
  - **Description:** Does not support Jakarta EE 9 or later; requires major rework to adapt to new testing frameworks that leverage updated Jakarta APIs.
  - **Root Cause:** This version is not designed for newer Java versions or Jakarta specifications.
  - **Resolution:** Plan for an overhaul using Arquillian's new version or switch to alternative testing tools such as TestNG or JUnit 5.
  - **Status:** Critical

## 4. Removed JVM Flags
- **Incident ID:** JVM_FLAGS_01
  - **Affected Component:** Application startup
  - **Removed JVM Flag:** `-XX:+UseSplitVerifier`
  - **Description:** The flag was deprecated in JDK 9 and removed in later versions.
  - **Root Cause:** Legacy configuration settings that are no longer valid.
  - **Resolution:** Remove the flag from the JVM options and replace with validation settings as per Java 11 and above.
  - **Status:** In Progress

## Additional Notes
- Review all dependencies for their respective updates to ensure compliance with Jakarta EE 9 standards and Java 11+ requirements.
- Continuous monitoring needed for usage of new Java language features that may be introduced in future versions.