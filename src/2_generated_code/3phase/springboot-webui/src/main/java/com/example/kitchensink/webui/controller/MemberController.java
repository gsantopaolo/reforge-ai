// src/main/java/com/example/kitchensink/webui/controller/MemberController.java
package com.example.kitchensink.webui.controller;

import com.example.kitchensink.business.model.Member;
import com.example.kitchensink.business.service.MemberRegistration;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class MemberController {

    private final MemberRegistration registration;

    public MemberController(MemberRegistration registration) {
        this.registration = registration;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("member", new Member());
        model.addAttribute("members", registration.findAll());
        return "index";
    }

    @PostMapping("/register")
    public String register(Member member, Model model) {
        registration.register(member);
        model.addAttribute("member", member);
        return "success";
    }
}
