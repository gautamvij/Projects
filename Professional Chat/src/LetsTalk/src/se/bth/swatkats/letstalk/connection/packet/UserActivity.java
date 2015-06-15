package se.bth.swatkats.letstalk.connection.packet;

import java.io.Serializable;
import java.sql.Timestamp;

public class UserActivity implements Serializable {

	private static final long serialVersionUID = -1240895579941690877L;
	Integer userId;
	Timestamp checkIn, checkOut;

	public UserActivity(Integer userId, Timestamp checkIn, Timestamp checkOut) {
		super();
		this.userId = userId;
		this.checkIn = checkIn;
		this.checkOut = checkOut;
	}

	public Integer getUserId() {
		return userId;
	}

	public void setUserId(Integer userId) {
		this.userId = userId;
	}

	public Timestamp getCheckIn() {
		return checkIn;
	}

	public void setCheckIn(Timestamp checkIn) {
		this.checkIn = checkIn;
	}

	public Timestamp getCheckOut() {
		return checkOut;
	}

	public void setCheckOut(Timestamp checkOut) {
		this.checkOut = checkOut;
	}

}
