package se.bth.swatkats.letstalk.connection.packet.message;

import java.sql.Timestamp;

import se.bth.swatkats.letstalk.connection.packet.Packet;

/**
 * Abstract class to represent "real" Messages, which are sent from one client
 * to another.
 * 
 * @author JS
 *
 */
public abstract class Message extends Packet {

	/**
	 * 
	 */
	private static final long serialVersionUID = -2537491720091187268L;

	private int senderid;

	private int conversationid;

	private String username;

	private Timestamp timestamp;

	/**
	 * @return the senderid
	 */
	public int getSenderid() {
		return senderid;
	}

	/**
	 * @param senderid
	 *            the senderid to set
	 */
	public void setSenderid(int senderid) {
		this.senderid = senderid;
	}

	/**
	 * @return the username
	 */
	public String getUsername() {
		return username;
	}

	/**
	 * @param username
	 *            the username to set
	 */
	public void setUsername(String username) {
		this.username = username;
	}

	/**
	 * @return the conversationid
	 */
	public int getConversationid() {
		return conversationid;
	}

	/**
	 * @param conversationid
	 *            the conversationid to set
	 */
	public void setConversationid(int conversationid) {
		this.conversationid = conversationid;
	}

	/**
	 * @return the timestamp
	 */
	public Timestamp getTimestamp() {
		return timestamp;
	}

	/**
	 * @param timestamp
	 *            the timestamp to set
	 */
	public void setTimestamp(Timestamp timestamp) {
		this.timestamp = timestamp;
	}

	public Message(int receiver, int conversationid) {
		super(receiver);
		this.conversationid = conversationid;
		setTimestamp(new Timestamp(System.currentTimeMillis()));
	}

	public Message(int senderid, String username, Timestamp time, int receiver,
			int conversationid, String senderip) {
		super(receiver, senderip);
		this.senderid = senderid;
		this.timestamp = time;
		this.username = username;
		this.conversationid = conversationid;
	}

}
