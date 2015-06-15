package se.bth.swatkats.letstalk.connection.packet;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.packet.internal.NotificationChangeScope;

/**
 * Message containing a query for the database, and/or the returning result.
 * 
 * @author JS
 *
 */
public class DatabaseQuery extends Packet {

	private Object result;

	private Object[] params;

	private NotificationChangeScope notificationscope = new NotificationChangeScope();

	/**
	 * @return the notificationscope
	 */
	public NotificationChangeScope getNotificationscope() {
		return notificationscope;
	}

	/**
	 * @param notificationscope
	 *            the notificationscope to set
	 */
	public void setNotificationscope(NotificationChangeScope notificationscope) {
		this.notificationscope = notificationscope;
	}

	/**
	 * @return the result
	 */
	public Object getResult() {
		return result;
	}

	/**
	 * @param result
	 *            the result to set
	 */
	public void setResult(Object result) {
		this.result = result;
	}

	public DatabaseQuery(String method, Object[] params) {
		super(Constants.SERVERID);
		this.params = params;
		this.method = method;
		setNotificationscope(new NotificationChangeScope());
	}

	/**
	 * @return the params
	 */
	public Object[] getParams() {
		return params;
	}

	/**
	 * @param params
	 *            the params to set
	 */
	public void setParams(Object[] params) {
		this.params = params;
	}

	/**
	 * @return the method
	 */
	public String getMethod() {
		return method;
	}

	/**
	 * @param method
	 *            the method to set
	 */
	public void setMethod(String method) {
		this.method = method;
	}

	private String method;

	/**
	 * 
	 */
	private static final long serialVersionUID = 2015644623917894325L;

}
