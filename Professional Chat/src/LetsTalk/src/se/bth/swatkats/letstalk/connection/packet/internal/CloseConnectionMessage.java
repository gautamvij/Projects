package se.bth.swatkats.letstalk.connection.packet.internal;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.packet.Packet;
import se.bth.swatkats.letstalk.user.UserFactory;

/**
 * Special Message to signal to close the connection.
 * 
 * @author JS
 *
 */
public class CloseConnectionMessage extends Packet {

	public CloseConnectionMessage() {
		super(UserFactory.getClientById(Constants.SERVERID).getId());
	}

	/**
	 * 
	 */
	private static final long serialVersionUID = 382693496076966183L;

}
