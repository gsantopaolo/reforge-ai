package org.jboss.as.quickstarts.kitchensink.event;

import org.jboss.as.quickstarts.kitchensink.model.Member;

public class MemberRegisteredEvent {
    private final Member member;

    public MemberRegisteredEvent(Member member) {
        this.member = member;
    }

    public Member getMember() {
        return member;
    }
}
