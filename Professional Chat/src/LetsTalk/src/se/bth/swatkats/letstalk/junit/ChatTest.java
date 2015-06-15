package se.bth.swatkats.letstalk.junit;

import static org.junit.Assert.fail;

import org.junit.Test;

import se.bth.swatkats.letstalk.connection.Connection;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;
import se.bth.swatkats.letstalk.user.User;
import se.bth.swatkats.letstalk.user.UserFactory;

public class ChatTest {
	
	@Test
	public void connectToClient() {
		int id2 = 2;
		int id3 = 3;
		Connection conn = new Connection(new User(id2));

		TextMessage m = new TextMessage(id3, id3, "This is a test Message.");
		conn.sendMessageObject(m);

		conn.closeConnection();
	}

	@Test
	public void test() {
		int id2 = 2;
		int id3 = 3;
		int idinvalid = -1;
		Connection conn = new Connection(new User(id2));
		Connection conn2 = new Connection(new User(id3));

		TextMessage m = new TextMessage(id2,id2, "This Message goes to id2.");
		TextMessage m1 = new TextMessage(id3,id3,
				"THIS is the second testmessage. It goes to id1.");
		TextMessage m2 = new TextMessage(idinvalid, idinvalid, "THIS Is the third testmessage");
		TextMessage m3 = new TextMessage(idinvalid, idinvalid,
				"THIS Is the fourth testmessage");
		TextMessage m4 = new TextMessage(id2, id2,
				"THIS Is the fifth testmessage to id2");

		conn.sendMessageObject(m);
		conn2.sendMessageObject(m1);
		try {
			conn.sendMessageObject(m2);
			fail("Exception should be thrown.");
		} catch (NullPointerException e) {

		}
		try {
			conn.sendMessageObject(m3);
			fail("Exception should be thrown.");
		} catch (NullPointerException e) {

		}
		
		conn2.sendMessageObject(m4);

		conn2.sendMessageObject(m);
		conn.sendMessageObject(m1);
		try {
			conn2.sendMessageObject(m2);
			fail("Exception should be thrown.");
		} catch (NullPointerException e) {

		}
		try {
			conn2.sendMessageObject(m3);
			fail("Exception should be thrown.");
		} catch (NullPointerException e) {

		}
		conn.sendMessageObject(m4);

		conn.closeConnection();
		conn2.closeConnection();
		try {
			conn.closeConnection();
			fail("Exception should be thrown.");
		} catch (NullPointerException e) {

		}

		// give it some time (multithreading)
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		// reconnect
		conn = new Connection(new User(id2));
		m = new TextMessage(id3, id3,
				"This message is sent by the next connection to id3.");
		conn.sendMessageObject(m);
		conn.closeConnection();

	}



}
