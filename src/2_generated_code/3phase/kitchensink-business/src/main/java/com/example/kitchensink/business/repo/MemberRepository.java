package com.example.kitchensink.business.repo;

import com.example.kitchensink.business.model.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface MemberRepository extends JpaRepository<Member, Long> {
    List<Member> findAllByOrderByNameAsc();
}
