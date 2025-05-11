**Kitchensink Java 21 Util Migration Guide**

## Overview

Extract the `util` code from the legacy **kitchensink** quickstart into its own Java 21 module (`kitchensink-util`), modernize it for CDI/Spring Boot compatibility, then reintegrate it into the legacy WAR so that CDI injections (EntityManager, Logger) resolve correctly in JBoss EAP 8.0.

---

## 1. Project Structure

Your **root** directory name (e.g. `2phase1/`) contains exactly three items:

```
2phase1/              ← Root aggregator directory
├─ pom.xml           ← Parent POM (aggregator)
├─ kitchensink-util/ ← New util JAR module
└─ kitchensink/      ← Legacy WAR module
```

> **Note:** you may name the parent folder anything (here `2phase1`); the key is that it holds your `pom.xml` plus the two sub‑modules.

## 2. Create `kitchensink-util` Module

### 2.1 Directory Layout

```text
kitchensink-util/
├─ pom.xml
└─ src/
   └─ main/
      └─ java/
         └─ org/jboss/as/quickstarts/kitchensink/util/
            └─ Resources.java
```

### 2.2 `pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <!-- Inherit from parent aggregator -->
  <parent>
    <groupId>com.example.kitchensink</groupId>
    <artifactId>kitchensink-parent</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>

  <artifactId>kitchensink-util</artifactId>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <!-- CDI API (provided by EAP) -->
    <dependency>
      <groupId>jakarta.enterprise</groupId>
      <artifactId>jakarta.enterprise.cdi-api</artifactId>
      <version>4.0.1</version>
      <scope>provided</scope>
    </dependency>
    <!-- JPA API -->
    <dependency>
      <groupId>jakarta.persistence</groupId>
      <artifactId>jakarta.persistence-api</artifactId>
      <version>3.1.0</version>
      <scope>provided</scope>
    </dependency>
    <!-- Bean Validation API -->
    <dependency>
      <groupId>jakarta.validation</groupId>
      <artifactId>jakarta.validation-api</artifactId>
      <version>3.0.2</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
</project>
```

### 2.3 Java Source (`Resources.java`)

```java
package org.jboss.as.quickstarts.kitchensink.util;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import jakarta.enterprise.inject.spi.InjectionPoint;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.util.logging.Logger;

/**
 * CDI producer for EntityManager and Logger.
 */
@ApplicationScoped  // ← bean‑defining CDI annotation
public class Resources {

    @Produces
    @PersistenceContext
    private EntityManager em;

    @Produces
    public Logger produceLog(InjectionPoint injectionPoint) {
        return Logger.getLogger(
            injectionPoint.getMember().getDeclaringClass().getName()
        );
    }
}
```

---

### 2.4 Copy & Delete File Operations (CLI-based)

1. From root `2phase1/`, run:

   ```sh
   mkdir -p kitchensink-util/src/main/java/org/jboss/as/quickstarts/kitchensink/util
   cp kitchensink/src/main/java/org/jboss/as/quickstarts/kitchensink/util/Resources.java \
      kitchensink-util/src/main/java/org/jboss/as/quickstarts/kitchensink/util/
   rm kitchensink/src/main/java/org/jboss/as/quickstarts/kitchensink/util/Resources.java
   ```
2. This ensures only the util module contains `Resources.java`.

---

## 3. Update the Legacy WAR module

1. Open `kitchensink/pom.xml`.
2. Under `<project>` replace the existing `<groupId>`, `<version>`, `<packaging>` blocks with:

   ```xml
   <modelVersion>4.0.0</modelVersion>
   <parent>
     <groupId>com.example.kitchensink</groupId>
     <artifactId>kitchensink-parent</artifactId>
     <version>1.0-SNAPSHOT</version>
   </parent>
   <artifactId>kitchensink</artifactId>
   <packaging>war</packaging>
   ```
3. In its `<dependencies>` add **only once**:

   ```xml
   <dependency>
     <groupId>com.example.kitchensink</groupId>
     <artifactId>kitchensink-util</artifactId>
     <version>${project.version}</version>
   </dependency>
   ```
4. Remove any `<dependency>` entries or exclusions that bundled a Servlet or Tomcat JAR: rely on the server’s provided API.

---

## 4. Verify Parent POM modules order

Ensure your **2phase1/pom.xml** lists modules **in this** order:

```xml
<modules>
  <module>kitchensink-util</module>
  <module>kitchensink</module>
</modules>
```

This guarantees the util JAR builds first.

---

## 5. Final structure recap

```
2phase1/                          
├─ pom.xml        ← parent aggregator
├─ kitchensink-util/               
│  ├ pom.xml                      
│  └ src/main/java/.../Resources.java  
└─ kitchensink/                    
   ├ pom.xml                      
   └ src/... (legacy code minus Resources.java)
```

You can hand these CLI‑driven file operations and POM edits directly to your AI agent—no IDE shortcuts required.  All annotation and dependency changes are listed explicitly.  Good luck!
