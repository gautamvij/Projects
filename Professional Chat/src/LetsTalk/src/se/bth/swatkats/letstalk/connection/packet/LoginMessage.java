package se.bth.swatkats.letstalk.connection.packet;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.user.User;

/**
 * Message to singal Login.
 * 
 * @author JS
 *
 */
public class LoginMessage extends Packet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 7985809437396989915L;

	private String username;

	private String pw;

	private User user;

	public LoginMessage(String username, String pw) {
		super(Constants.SERVERID);
		this.username = username;
		this.pw = pw;
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
	 * @return the pw
	 */
	public String getPw() {
		return pw;
	}

	/**
	 * @param pw
	 *            the pw to set
	 */
	public void setPw(String pw) {
		this.pw = pw;
	}

	/**
	 * @return the user
	 */
	public User getUser() {
		return user;
	}

	/**
	 * @param user
	 *            the user to set
	 */
	public void setUser(User user) {
		this.user = user;
	}

}
