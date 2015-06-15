package se.bth.swatkats.letstalk.connection.packet.internal;

import java.io.Serializable;

/**
 * Class containing information about what has to be updated in the GUI.
 * 
 * @author JS
 *
 */
public class NotificationChangeScope implements Serializable {

	private static final long serialVersionUID = -9021191659082519069L;

	private QueryNotificationScope scope;

	private QueryNotificationType type;

	private Integer id;

	public NotificationChangeScope(QueryNotificationScope scope,
			QueryNotificationType type) {
		super();
		this.scope = scope;
		this.type = type;
	}

	public NotificationChangeScope() {
		super();
		scope = QueryNotificationScope.NOONE;
		type = QueryNotificationType.NOTHING;
	}

	public NotificationChangeScope(QueryNotificationScope scope,
			QueryNotificationType type, Integer user_id) {
		this.scope = scope;
		this.type = type;
		this.id = user_id;
	}

	/**
	 * @return the scope
	 */
	public QueryNotificationScope getScope() {
		return scope;
	}

	/**
	 * @param scope
	 *            the scope to set
	 */
	public void setScope(QueryNotificationScope scope) {
		this.scope = scope;
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
	public void setType(QueryNotificationType type) {
		this.type = type;
	}

	/**
	 * @return the id
	 */
	public Integer getId() {
		return id;
	}

	/**
	 * @param id
	 *            the id to set
	 */
	public void setId(Integer id) {
		this.id = id;
	}

}
