package se.bth.swatkats.letstalk.user;

import java.io.Serializable;

/**
 * This class describes a user in the system.
 * @author JS + SP
 *
 */
public class User implements Serializable {
    

    private static final long serialVersionUID = -8420577662079428268L;

    private int id;
    private String username;
    private String email;
    private int status; // 0=Available, 1=Busy, 2=Idle, 3=Offline
    private int admin_flag;
        
    /**
     * Creates a user without any specifications.
     */
    public User(){
        this.id = -1;
        this.username = "Test Name";
        this.email = "test@email.com";
        this.status = 0;
        this.admin_flag = 1;
    }
    
    public User(int userid){
    	this.id = userid;
        this.username = "Test Name";
        this.email = "test@email.com";
        this.status = 0;
        this.admin_flag = 1;
    }
    
    /**
     * Creates a user providing all its variables.
     * 
     * @param id
     * @param username
     * @param email
     * @param status 
     * @param admin_flag 
     */
    public User(int id, String username, String email, int status, int admin_flag){
        this.id = id;
        this.username = username;
        this.email = email;
        this.admin_flag = admin_flag;
        this.status = status;
    }

	/**
	 * @return the id
	 */
	public int getId() {
		return id;
	}

	/**
	 * @param id the id to set
	 */
	public void setId(int id) {
		this.id = id;
	}

	/**
	 * @return the username
	 */
	public String getUsername() {
		return username;
	}

	/**
	 * @param username the username to set
	 */
	public void setUsername(String username) {
		this.username = username;
	}

	/**
	 * @return the email
	 */
	public String getEmail() {
		return email;
	}

	/**
	 * @param email the email to set
	 */
	public void setEmail(String email) {
		this.email = email;
	}

	/**
         *  0=Available, 1=Busy, 2=Idle, 3=Offline
	 * @return the status
	 */
	public int getStatus() {
		return status;
	}

	/**
	 * @param status the status to set
	 */
	public void setStatus(int status) {
		this.status = status;
	}

	/**
	 * @return the admin_flag
	 */
	public int getAdmin_flag() {
		return admin_flag;
	}

	/**
	 * @param admin_flag the admin_flag to set
	 */
	public void setAdmin_flag(int admin_flag) {
		this.admin_flag = admin_flag;
	}

}
