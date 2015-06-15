package se.bth.swatkats.letstalk.connection;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.security.PublicKey;

import javax.crypto.SealedObject;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.encryption.CryptModule;
import se.bth.swatkats.letstalk.connection.packet.LoginMessage;
import se.bth.swatkats.letstalk.connection.packet.Packet;
import se.bth.swatkats.letstalk.connection.packet.internal.CloseConnectionMessage;
import se.bth.swatkats.letstalk.connection.packet.internal.OpenConnectionMessage;
import se.bth.swatkats.letstalk.connection.packet.message.Message;
import se.bth.swatkats.letstalk.user.User;

/**
 * The main class to handle Basic connections.
 * 
 * @author JS
 *
 */
public class Connection {

	private User user;

	private Socket socket;

	private ObjectInputStream in;

	private ObjectOutputStream out;

	private boolean connected;

	private CryptModule crypt;

	/**
	 * Creates a new Connection, where all the traffic can be handled. This
	 * method uses the default values from Constants.
	 * 
	 */
	public Connection(User user) {
		this.user = user;
		openConnection(Constants.HOST, Constants.SERVERPORT);
	}

	/**
	 * Creates a new Connection, where all the traffic can be handled.
	 * 
	 * 
	 * @param host
	 *            The host to connect to
	 * @param serverport
	 *            The port to connect to
	 */
	public Connection(User user, String host, int serverport) {
		this.user = user;
		openConnection(Constants.HOST, Constants.SERVERPORT);
	}

	/**
	 * @return the connected
	 */
	public boolean isConnected() {
		return connected;
	}

	/**
	 * Called to install a connection to the server
	 * 
	 * @param host
	 *            the host
	 * 
	 */
	public boolean openConnection(String host, int serverport) {
		if (socket != null) {
			System.out
					.println("Closing old connection and opening new one to host "
							+ host + ", Port: " + serverport);
		}
		try {
			socket = new Socket(host, serverport);
			in = new ObjectInputStream(socket.getInputStream());
			out = new ObjectOutputStream(socket.getOutputStream());

		} catch (IOException e) {
			socket = null;
			System.err.print("Connection could not be established. Host "
					+ host + ", Port: " + serverport);
			e.printStackTrace();
			return false;
		}

		Thread t = new Thread(new Listener(in));
		t.start();

		crypt = new CryptModule();
		try {
			PublicKey publicKey = crypt.initKeyExchange();
			OpenConnectionMessage m = new OpenConnectionMessage(publicKey);
			m.setSenderip(socket.getInetAddress().getHostAddress());
			out.writeObject(m);
		} catch (Exception e) {
			System.err.print("Key exchange failed.");
			e.printStackTrace();
			return false;
		}

		// wait for connection to establish
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		System.out.println("Connected to " + host);
		return true;
	}

	/**
	 * Used to pass one MessageObject to the Server. Is encrypted and sent.
	 * 
	 * @param object
	 *            the object to pass
	 */
	public boolean sendMessageObject(Packet object) {
		if (object == null) {
			throw new NullPointerException("Sended object must not be null.");
		} else if (object.getReceiverid() < 0 && object.getReceiverid() != -10) {
			//throw new NullPointerException("Receiver must not be null or negative.");
                    System.out.println("Receiver must not be null or negative.");
                }
		// mark sender

		object.setSenderip(socket.getInetAddress().getHostAddress());

		if (object instanceof Message) {
			((Message) object).setSenderid(user.getId());
		}

		if (socket == null || socket.isClosed()) {
			throw new NullPointerException("Client is not connected.");
		}
		try {
			out.writeObject(crypt.encrypt(object));
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;

	}

	/**
	 * Called to close the connection. After calling, no further objects can be
	 * send, but another reopening of the connection may happen.
	 */
	public void closeConnection() {
		sendMessageObject(new CloseConnectionMessage());
		while (connected) {
			// wait for disconnection message
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		System.out.println("Disconnecting.");
	}

	/**
	 * Listener is the "backchannel" of the User listens to the input of the
	 * sockets, reads objects sent to the client, and forwards it to the
	 * InputHandler.
	 * 
	 * @author JS
	 *
	 */
	private class Listener implements Runnable {

		ObjectInputStream in;

		public Listener(ObjectInputStream in) {
			super();
			this.in = in;
		}

		@Override
		public void run() {
			try {
				Packet openmessage = (Packet) in.readObject();
				if (openmessage instanceof OpenConnectionMessage) {
					crypt.retreiveKey(((OpenConnectionMessage) openmessage)
							.getKey());
				} else {
					System.err
							.print("Expecting OpenConnection Message first.\n");
				}
				connected = true;

				while (true) {
					Packet message = (Packet) crypt.decrypt(((SealedObject) in
							.readObject()));

					// handle Close connection
					if (message instanceof CloseConnectionMessage) {
						System.out.printf("Server disconnected.");
						connected = false;
						try {
							in.close();
							out.close();
							socket.close();
						} catch (IOException e) {
							System.err
									.print("Problems with closing connection.");
							e.printStackTrace();
						}
						socket = null;
						in = null;
						out = null;
						break;
					}

					// handle Login
					if (message instanceof LoginMessage) {
						user = ((LoginMessage) message).getUser();
					}

					Thread t = new Thread(new InputHandler(message));
					t.start();
				}

			} catch (Exception e) {
				System.err.print("Receiving object failed.\n");
				e.printStackTrace();
			}
		}
	}

	public User sendLoginObject(LoginMessage m) {
		sendMessageObject(m);
		while (user.getId() < -1) {
			// wait until server answer received
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		return user;
	}

}
