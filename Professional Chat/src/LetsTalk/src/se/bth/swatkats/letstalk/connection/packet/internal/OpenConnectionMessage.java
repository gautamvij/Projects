package se.bth.swatkats.letstalk.connection.packet.internal;

import java.security.PublicKey;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.packet.Packet;
import se.bth.swatkats.letstalk.user.UserFactory;

/**
 * Special Message to signal to open the connection.
 * 
 * @author JS
 *
 */
public class OpenConnectionMessage extends Packet {

	private PublicKey key;

	public OpenConnectionMessage(PublicKey key) {
		super(UserFactory.getClientById(Constants.SERVERID).getId());
		this.key = key;
	}
	
	public OpenConnectionMessage(PublicKey key, int receiver) {
		super(receiver);
		this.key = key;
	}

	/**
	 * 
	 */
	private static final long serialVersionUID = 382693496076966183L;

	public PublicKey getKey() {
		return key;
	}

	public void setKey(PublicKey key) {
		this.key = key;
	}

}
