package se.bth.swatkats.letstalk.connection.packet.internal;

/**
 * Different types of Users to be notified. 
 * 
 * @author JS
 *
 */
public enum QueryNotificationScope {
	NOONE, LOCALADDRESSBOOK, SINGLEUSER;

	private QueryNotificationType type;

	private Integer userid;

	/**
	 * @return the userid
	 */
	public Integer getId() {
		return userid;
	}

	/**
	 * @param userid
	 *            the userid to set
	 */
	public QueryNotificationScope setUserid(Integer userid) {
		this.userid = userid;
		return this;
	}

	private QueryNotificationScope() {
		this.type = QueryNotificationType.NOTHING;
	}

	/**
	 * @return the type
	 */
	public QueryNotificationType getType() {
		return type;
	}

	/**
	 * @param type
	 *            the type to set
	 */
	public QueryNotificationScope setType(QueryNotificationType type) {
		this.type = type;
		return this;
	}
}
