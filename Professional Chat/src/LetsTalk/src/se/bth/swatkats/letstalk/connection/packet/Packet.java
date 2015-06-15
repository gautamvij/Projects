package se.bth.swatkats.letstalk.connection.packet;

import java.io.Serializable;

/**
 * Abstract Class for Packets going through the Channel. Conataining basic
 * information. Every Message over the channel should subclass this class.
 * 
 * @author JS
 *
 */
public abstract class Packet implements Serializable {

	/**
	 * Generated
	 */
	private static final long serialVersionUID = -444519389366236917L;

	private String senderip;

	private int receiverid;

	/**
	 * @return the senderip
	 */
	public String getSenderip() {
		return senderip;
	}

	/**
	 * @param senderip
	 *            the senderip to set
	 */
	public void setSenderip(String senderip) {
		this.senderip = senderip;
	}

	/**
	 * @return the receiverid
	 */
	public int getReceiverid() {
		return receiverid;
	}

	/**
	 * @param receiverid
	 *            the receiverid to set
	 */
	public void setReceiverid(int receiverid) {
		this.receiverid = receiverid;
	}

	public Packet(int receiver) {
		super();
		this.receiverid = receiver;
	}

	public Packet(int receiver, String senderip) {
		super();
		this.receiverid = receiver;
		this.senderip = senderip;
	}

}
