package com.example.kitchensink.business.service;

import java.util.List;
import com.example.kitchensink.business.event.MemberRegisteredEvent;
import com.example.kitchensink.business.model.Member;
import com.example.kitchensink.business.repo.MemberRepository;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
@Service
public class MemberRegistration {
    private final MemberRepository repo;
    private final ApplicationEventPublisher events;

    public MemberRegistration(MemberRepository repo,
                              ApplicationEventPublisher events) {
        this.repo   = repo;
        this.events = events;
    }

    @Transactional
    public Member register(Member m) {
        Member saved = repo.save(m);
        events.publishEvent(new MemberRegisteredEvent(this, saved));
        return saved;
    }

    // ← Add this!
    public List<Member> findAll() {
        return repo.findAll();
    }
}
