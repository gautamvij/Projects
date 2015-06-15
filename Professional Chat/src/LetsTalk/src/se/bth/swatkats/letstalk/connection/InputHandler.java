package se.bth.swatkats.letstalk.connection;

import se.bth.swatkats.letstalk.connection.packet.DatabaseQuery;
import se.bth.swatkats.letstalk.connection.packet.LoginMessage;
import se.bth.swatkats.letstalk.connection.packet.NotificationChangeMessage;
import se.bth.swatkats.letstalk.connection.packet.Packet;
import se.bth.swatkats.letstalk.connection.packet.message.FileMessage;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;

/**
 * This class is responsible for reacting on different kinds of Message Objects
 * on the client side
 * 
 * @author JS
 *
 */
public class InputHandler implements Runnable {

	private Packet in;

	public InputHandler(Packet in) {
		this.in = in;
	}

	@Override
	public void run() {
		if (in instanceof TextMessage) {
			GuiHandler.getInstance().receiveTextMessage(((TextMessage) in));
		} else if (in instanceof LoginMessage) {
			// ignore -- Login is handled somewhere else
		} else if (in instanceof DatabaseQuery) {
			GuiHandler.getInstance().receiveDatabaseResult(
					((DatabaseQuery) in).getResult());
		} else if (in instanceof FileMessage) {
			GuiHandler.getInstance().receiveFileMessage((FileMessage) in);
		} else if (in instanceof NotificationChangeMessage) {
			notification((NotificationChangeMessage) in);
		} else {
			System.err.print("Error. Message type not supported.");
		}
	}

	private void notification(NotificationChangeMessage message) {
		switch (message.getScope().getType()) {
		case LOCALADDRESSBOOK:
			GuiHandler.getInstance().updateLocalAddressBook();
			break;
		case CONVERSATIONHISTORIES:
			GuiHandler.getInstance().updateConversationHistories();
			break;
		case NOTHING:
			// do nothing
			break;
		default:
			// should not occur
			System.err.print("Unknown update type " + message.getScope().getType());
			break;
		}
	}
}
