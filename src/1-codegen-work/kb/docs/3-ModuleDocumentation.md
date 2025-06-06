/*
 * JBoss, Home of Professional Open Source
 * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
 * contributors by the @authors tag. See the copyright.txt in the
 * distribution for a full listing of individual contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.jboss.as.quickstarts.kitchensink.data;

import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import java.util.List;
import org.jboss.as.quickstarts.kitchensink.model.Member;

public class MemberRepository {

    @Inject
    private EntityManager em;

    public Member findById(Long id) {
        return em.find(Member.class, id);
    }

    public Member findByEmail(String email) {
        List<Member> members = em.createQuery("SELECT m FROM Member m WHERE m.email = :email", Member.class)
                .setParameter("email", email).getResultList();
        if (members.isEmpty()) {
            return null;
        }
        return members.get(0);
    }

    public List<Member> findAllOrderedByName() {
        return em.createQuery("SELECT m FROM Member m ORDER BY m.name", Member.class).getResultList();
    }
}
