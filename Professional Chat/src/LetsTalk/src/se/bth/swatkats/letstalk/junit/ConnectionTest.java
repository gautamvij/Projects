package se.bth.swatkats.letstalk.junit;

import org.junit.Test;

import se.bth.swatkats.letstalk.connection.Connection;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;
import se.bth.swatkats.letstalk.user.User;
import se.bth.swatkats.letstalk.user.UserFactory;

public class ConnectionTest {

	@Test
	public void test() {
		int id4 = 4;
		int id3 = 3;
		Connection conn = new Connection(new User(id4));

		TextMessage m = new TextMessage(id3, id3, "This Message goes to id: 3.");
		conn.sendMessageObject(m);

		// stay online
		while (true) {
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

}
