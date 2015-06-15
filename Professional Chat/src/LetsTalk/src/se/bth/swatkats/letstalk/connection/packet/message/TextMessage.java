package se.bth.swatkats.letstalk.connection.packet.message;

import java.sql.Timestamp;

/**
 * Standard text Message.
 * 
 * @author JS
 *
 */
public class TextMessage extends Message {

	/**
	 * 
	 */
	private static final long serialVersionUID = 3873427887735611133L;

	private String text;


	/**
	 * @return the text
	 */
	public String getText() {
		return text;
	}

	/**
	 * @param text the text to set
	 */
	public void setText(String text) {
		this.text = text;
	}

	public TextMessage(int receiver, int conv, String message) {
		super(receiver, conv);
		this.text = message;
	}

	public TextMessage(int senderid, String username, String text,
			Timestamp time, int receiver, int conv_id, String senderip) {
		super(senderid, username, time, receiver, conv_id, senderip);
		this.text = text;

	}
}
