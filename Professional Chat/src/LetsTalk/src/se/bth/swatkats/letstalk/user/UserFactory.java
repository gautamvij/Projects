package se.bth.swatkats.letstalk.user;

/**
 * Factory class providing basic functionality when handling clients.
 * 
 * @author JS
 *
 */
public class UserFactory {

	/**
	 * Returns the client object to the corresponding id string.
	 * 
	 * @param id
	 *            the id string of the client
	 * @return the client or null if client with the given id exists
	 */
	public static User getClientById(int id) {
		// TODO DATABASE provide a client database
		User c = new User();
		c.setId(id);
		return c;
	}

}
