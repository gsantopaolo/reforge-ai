package org.jboss.as.quickstarts.kitchensink.model;

import jakarta.annotation.Generated;
import jakarta.persistence.metamodel.EntityType;
import jakarta.persistence.metamodel.SingularAttribute;
import jakarta.persistence.metamodel.StaticMetamodel;

@StaticMetamodel(Member.class)
@Generated("org.hibernate.jpamodelgen.JPAMetaModelEntityProcessor")
public abstract class Member_ {

	
	/**
	 * @see org.jboss.as.quickstarts.kitchensink.model.Member#phoneNumber
	 **/
	public static volatile SingularAttribute<Member, String> phoneNumber;
	
	/**
	 * @see org.jboss.as.quickstarts.kitchensink.model.Member#name
	 **/
	public static volatile SingularAttribute<Member, String> name;
	
	/**
	 * @see org.jboss.as.quickstarts.kitchensink.model.Member#id
	 **/
	public static volatile SingularAttribute<Member, Long> id;
	
	/**
	 * @see org.jboss.as.quickstarts.kitchensink.model.Member
	 **/
	public static volatile EntityType<Member> class_;
	
	/**
	 * @see org.jboss.as.quickstarts.kitchensink.model.Member#email
	 **/
	public static volatile SingularAttribute<Member, String> email;

	public static final String PHONE_NUMBER = "phoneNumber";
	public static final String NAME = "name";
	public static final String ID = "id";
	public static final String EMAIL = "email";

}

