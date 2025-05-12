package com.example.kitchensink.webui;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(
        scanBasePackages = {
                "com.example.kitchensink.webui",
                "com.example.kitchensink.business"     // <— include your business package
        }
)
@EntityScan("com.example.kitchensink.business.model")       // <— your JPA entities
@EnableJpaRepositories("com.example.kitchensink.business.repo") // <— your Spring Data repos
public class WebUiApplication {
    public static void main(String[] args) {
        SpringApplication.run(WebUiApplication.class, args);
    }
}
