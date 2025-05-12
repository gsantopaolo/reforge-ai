package org.jboss.as.quickstarts.kitchensink.util;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import jakarta.enterprise.inject.spi.InjectionPoint;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.util.logging.Logger;

/**
 * This class uses CDI to alias Jakarta EE resources, such as
 * the persistence context, to CDI beans.
 */
@ApplicationScoped                                       // ← bean‐defining CDI annotation
public class Resources {

    @Produces
    @PersistenceContext
    private EntityManager em;

    @Produces
    public Logger produceLog(InjectionPoint injectionPoint) {
        return Logger.getLogger(
                injectionPoint.getMember()
                        .getDeclaringClass()
                        .getName()
        );
    }
}
