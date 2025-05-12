package org.jboss.as.quickstarts.kitchensink.util;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/resources")
public class ResourceController {

    private final Resources resources;

    public ResourceController(Resources resources) {
        this.resources = resources;
    }

    @GetMapping("/ping")
    public String ping() {
        // for demo, call any Resources method or just return a static string
        return "PONG from Resources: " + resources.toString();
    }
}
