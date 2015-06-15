package se.bth.swatkats.letstalk.connection.packet;

import se.bth.swatkats.letstalk.connection.packet.internal.NotificationChangeScope;

/**
 * Message to signal a change in the GUI.
 * 
 * @author JS
 *
 */
public class NotificationChangeMessage extends Packet {

	public NotificationChangeMessage(int receiver, NotificationChangeScope scope) {
		super(receiver);
		this.scope = scope;
	}

	private static final long serialVersionUID = 7852374571684274740L;

	private NotificationChangeScope scope;

	/**
	 * @return the type
	 */
	public NotificationChangeScope getScope() {
		return scope;
	}

	/**
	 */
	public void setType(NotificationChangeScope scope) {
		this.scope = scope;
	}

}
