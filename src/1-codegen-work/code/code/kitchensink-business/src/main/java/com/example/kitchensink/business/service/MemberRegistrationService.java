package com.example.kitchensink.business.service;

import com.example.kitchensink.business.model.Member;
import com.example.kitchensink.business.repo.MemberRepository;
import com.example.kitchensink.business.event.MemberRegisteredEvent; // Using the created event
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class MemberRegistrationService {
    private static final Logger log = LoggerFactory.getLogger(MemberRegistrationService.class);

    private final MemberRepository memberRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Autowired
    public MemberRegistrationService(MemberRepository memberRepository, ApplicationEventPublisher eventPublisher) {
        this.memberRepository = memberRepository;
        this.eventPublisher = eventPublisher;
    }

    @Transactional // Default propagation REQUIRED, rolls back on RuntimeException
    public void register(Member member) { // Consider specific exceptions for more granular error handling
        log.info("Registering member: " + member.getName());
        memberRepository.save(member);
        // Publish a Spring application event
        eventPublisher.publishEvent(new MemberRegisteredEvent(member));
        log.info("Member " + member.getName() + " registered.");
    }
}