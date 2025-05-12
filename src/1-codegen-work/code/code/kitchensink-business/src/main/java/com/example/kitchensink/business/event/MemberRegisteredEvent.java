package com.example.kitchensink.business.event;

import com.example.kitchensink.business.model.Member;

// Using a simple POJO event, could also extend org.springframework.context.ApplicationEvent
public class MemberRegisteredEvent {
    private final Member member;

    public MemberRegisteredEvent(Member member) {
        this.member = member;
    }

    public Member getMember() {
        return member;
    }
}