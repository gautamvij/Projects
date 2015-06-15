package se.bth.swatkats.letstalk.connection;

import java.util.ArrayList;
import java.util.Hashtable;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.packet.DatabaseQuery;
import se.bth.swatkats.letstalk.connection.packet.FileRepo;
import se.bth.swatkats.letstalk.connection.packet.LoginMessage;
import se.bth.swatkats.letstalk.connection.packet.UserActivity;
import se.bth.swatkats.letstalk.connection.packet.internal.NotificationChangeScope;
import se.bth.swatkats.letstalk.connection.packet.internal.QueryNotificationScope;
import se.bth.swatkats.letstalk.connection.packet.internal.QueryNotificationType;
import se.bth.swatkats.letstalk.connection.packet.message.FileMessage;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;
import se.bth.swatkats.letstalk.gui.Conversation;
import se.bth.swatkats.letstalk.gui.HomePage;
import se.bth.swatkats.letstalk.user.User;
import se.bth.swatkats.letstalk.statistics.TopFileChats;
import se.bth.swatkats.letstalk.statistics.TopTextChats;

/**
 * This class acts as interface between
 * 
 * @author Sokratis Papadopoulos and Johannes Grohmann
 */
@SuppressWarnings("unchecked")
public class GuiHandler implements IDatabase {

	private Connection conn;
	private User user;
	private Object databaseresult = null;

	private HomePage gui;

	private static volatile GuiHandler instance;

	public static GuiHandler getInstance() {
		if (instance == null) {
			synchronized (GuiHandler.class) {
				if (instance == null) {
					instance = new GuiHandler();
				}
			}
		}
		return instance;
	}

	/**
	 * get the User object
	 * 
	 * @return the user
	 */
	public User getUser() {
		return user;
	}

	/**
	 * Establish connection to server and database, if not done yet.
	 * 
	 * @return true if successful, false if not.
	 */
	public boolean openConnection() {
		if (conn.isConnected()) {
			return true;
		}
		return conn.openConnection(Constants.HOST, Constants.SERVERPORT);
	}

	/**
	 * Function is called to log in.
	 * 
	 * @param usernameGiven
	 *            the username to log in with
	 * @param passwordGiven
	 *            the password to log in with
	 * @return the User object of the username, if login successful. If the
	 *         login is unsuccessful, the User.getId() will be less than 0.
	 */
	public User login(String usernameGiven, String passwordGiven) {
		LoginMessage m = new LoginMessage(usernameGiven, passwordGiven);
		user = conn.sendLoginObject(m);
		return user;
	}

	/**
	 * Sends a message to the given clientid.
	 * 
	 * @param receiverid
	 *            the userid of the receiver
	 * @param text
	 *            the text message
	 * @return true if successful, false if not
	 */
	public boolean sendMessage(int receiverid, int conversationid, String text) {
		TextMessage m = new TextMessage(receiverid, conversationid, text);
		return conn.sendMessageObject(m);
	}

	/**
	 * Called to close the connection to the server.
	 * 
	 * @return true if successful, false if not
	 */
	public boolean closeConnection() {
		conn.closeConnection();
		return true;
	}

	/**
	 * Method is called if the GUI receives a new TextMessage from a different
	 * client.
	 * 
	 * @param m
	 */
	public void receiveTextMessage(TextMessage m) {
		if (gui == null) {
			System.err.print("GUI has not been set yet.");
		}
		gui.receivedMessage(m);
	}

	private synchronized Object execute(NotificationChangeScope notify,
			String method, Object... params) {
		DatabaseQuery query = new DatabaseQuery(method, params);
		query.setNotificationscope(notify);
		databaseresult = null;
		conn.sendMessageObject(query);
		while (databaseresult == null) {
			// wait until databaseresult has the result stored
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		// clear databaseresult again
		Object answer = databaseresult;
		databaseresult = null;
		return answer;
	}

	private synchronized Object execute(String method, Object... params) {
		return execute(new NotificationChangeScope(), method, params);
	}

	public void receiveDatabaseResult(Object result) {
		databaseresult = result;
	}

	@Override
	public Integer changeUserPassword(Integer user_id, String username,
			String oldPass, String newPass) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id, username, oldPass, newPass);
	}

	@Override
	public Boolean setUserStatusAvailable(Integer userid) {
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.LOCALADDRESSBOOK,
				QueryNotificationType.CONVERSATIONHISTORIES), Thread
				.currentThread().getStackTrace()[1].getMethodName(), userid);
	}

	@Override
	public Boolean setUserStatusBusy(Integer userid) {
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.LOCALADDRESSBOOK,
				QueryNotificationType.CONVERSATIONHISTORIES), Thread
				.currentThread().getStackTrace()[1].getMethodName(), userid);
	}

	@Override
	public ArrayList<User> searchLocalUsers(Integer user_id, String phrase) {
		if (phrase == null) {
			phrase = "";
		}
		return (ArrayList<User>) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id, phrase);
	}

	@Override
	public Integer createUser(String username, String password, String email,
			Boolean isAdmin) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				username, password, email, isAdmin);
	}

	@Override
	public Integer createConversation(Integer user_one, Integer user_two,
			Integer chat_type, String g_name) {
		if (chat_type == 0) {
			return (Integer) execute(new NotificationChangeScope(
					QueryNotificationScope.LOCALADDRESSBOOK,
					QueryNotificationType.CONVERSATIONHISTORIES), Thread
					.currentThread().getStackTrace()[1].getMethodName(),
					user_one, user_two, chat_type, g_name);
		}
		return (Integer) execute(new NotificationChangeScope(
				QueryNotificationScope.SINGLEUSER,
				QueryNotificationType.CONVERSATIONHISTORIES, user_two), Thread
				.currentThread().getStackTrace()[1].getMethodName(), user_one,
				user_two, chat_type, g_name);
	}

	@Override
	public ArrayList<User> searchGlobalUsers(String phrase, Integer user_id) {
		return (ArrayList<User>) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				phrase, user_id);
	}

	@Override
	public ArrayList<User> usersFromGroup(Integer conv_id, Integer user_id) {
		return (ArrayList<User>) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				conv_id, user_id);
	}

	@Override
	public ArrayList<Conversation> fetchConversationsForUser(Integer user_id) {
		return (ArrayList<Conversation>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public ArrayList<FileMessage> fetchFileConversationHistory(
			Integer conversationId, Integer user_id) {
		return (ArrayList<FileMessage>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), conversationId, user_id);
	}

	@Override
	public ArrayList<TextMessage> fetchTextConversationHistory(
			Integer conversationId, Integer user_id) {
		return (ArrayList<TextMessage>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), conversationId, user_id);
	}

	@Override
	public Boolean addLocalUser(Integer user_current, Integer user_to_add) {
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.LOCALADDRESSBOOK,
				QueryNotificationType.LOCALADDRESSBOOK), Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_current, user_to_add);
	}

	@Override
	public Boolean deleteUserFromLocalBook(Integer userID, Integer receiverID) {
		return (Boolean) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				userID, receiverID);
	}

	@Override
	public Boolean blockUserFromLocalBook(Integer user_id_by, Integer user_id_to) {
		return (Boolean) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id_by, user_id_to);
	}

	@Override
	public Boolean unblockUserFromLocalBook(Integer user_id_by,
			Integer user_id_to) {
		int conversationid = 0;
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.SINGLEUSER,
				QueryNotificationType.CONVERSATIONHISTORIES, user_id_to),
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id_by, user_id_to);
	}

	@Override
	public Boolean deleteUser(Integer user_id) {
		return (Boolean) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id);
	}

	/**
	 * @return the conn
	 */
	public Connection getConn() {
		return conn;
	}

	/**
	 * @param conn
	 *            the conn to set
	 */
	public void setConn(Connection conn) {
		this.conn = conn;
	}

	/**
	 * @return the databaseresult
	 */
	public Object getDatabaseresult() {
		return databaseresult;
	}

	/**
	 * @param databaseresult
	 *            the databaseresult to set
	 */
	public void setDatabaseresult(Object databaseresult) {
		this.databaseresult = databaseresult;
	}

	/**
	 * @return the gui
	 */
	public HomePage getGui() {
		return gui;
	}

	/**
	 * @param gui
	 *            the gui to set
	 */
	public void setGui(HomePage gui) {
		this.gui = gui;
	}

	/**
	 * @param user
	 *            the user to set
	 */
	public void setUser(User user) {
		this.user = user;
	}

	private GuiHandler() {
		super();
		// clientid is unknown yet
		conn = new Connection(new User(-10));
	}

	@Override
	public ArrayList<User> fetchBlockedUsers(Integer user_id) {
		return (ArrayList<User>) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id);
	}

	@Override
	public Boolean insertUserToGroup(Integer conv_id, Integer user_id) {
		return (Boolean) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				conv_id, user_id);
	}

	@Override
	public Boolean setUserStatusOffline(Integer userid) {
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.LOCALADDRESSBOOK,
				QueryNotificationType.CONVERSATIONHISTORIES), Thread
				.currentThread().getStackTrace()[1].getMethodName(), userid);
	}

	@Override
	public Boolean setUserStatusIdle(Integer userid) {
		return (Boolean) execute(new NotificationChangeScope(
				QueryNotificationScope.LOCALADDRESSBOOK,
				QueryNotificationType.CONVERSATIONHISTORIES), Thread
				.currentThread().getStackTrace()[1].getMethodName(), userid);
	}

	/**
	 * Method is called to start a file upload.
	 * 
	 * @param file
	 *            the file path of the file
	 * @param conversation_id
	 *            the conversation id, where the file shall be uploaded. (Ignore
	 *            for upload in repository)
	 * @param receiver_id
	 *            the receiver id (Ignore for upload in repository)
	 * @param type
	 *            true if the upload is a common repository upload, false if its
	 *            in a special conversation
	 */
	public void startFileUpload(String file, Integer conversation_id,
			Integer receiver_id, boolean type) {
		int id = insertFile(file, type);
		boolean success = false;
		if (!type) {
			try {
				success = se.bth.swatkats.letstalk.file.upload.Main.main(file,
						id);
			} catch (Exception e) {
				e.printStackTrace();
			}
			if (success) {
				FileMessage message = new FileMessage(receiver_id,
						conversation_id, file, id);
				conn.sendMessageObject(message);
			} else {
				System.err.print("File upload unsuccessful.");
			}
		} else {
			try {
				success = se.bth.swatkats.letstalk.file.repository.uploadMain
						.main(file, id);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * Method is called to start a file download.
	 * 
	 * @param path
	 *            The path, where to store the file
	 * @param file
	 *            The name of the file
	 * @param fileID
	 *            The ID of the file
	 * @param type
	 *            True, if its a common download from the repository, false if
	 *            its from a conversation
	 */
	public void startFileDownload(String path, String file, Integer fileID,
			boolean type) {
		boolean success = false;
		if (!type) {
			try {
				success = se.bth.swatkats.letstalk.file.download.Main.main(
						path, file, fileID);
			} catch (Exception e) {
				e.printStackTrace();
			}
			if (success) {
				System.out.println("success");
			} else {
				System.err.print("File download unsuccessful.");
			}
		} else {
			try {
				success = se.bth.swatkats.letstalk.file.repository.downloadMain
						.main(path, file, fileID);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

	}

	/**
	 * This method is called, when a File Message has been received.s
	 * 
	 * @param in
	 *            the FileMessage
	 */
	public void receiveFileMessage(FileMessage in) {
		gui.receiveFileMessage(in);
	}

	/**
	 * This method is called, when a change in the Address book has been
	 * detected.
	 */
	public void updateLocalAddressBook() {
		gui.updateContacts();
	}

	/**
	 * This method is called, when a change in the Conversation histories has
	 * been detected.
	 */
	public void updateConversationHistories() {
		gui.updateConversationHistories();
	}

	@Override
	public ArrayList<TopTextChats> fetchTopTextChatsForUserGroup(Integer user_id) {
		return (ArrayList<TopTextChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public ArrayList<TopTextChats> fetchTopTextChatsForUserOto(Integer user_id) {
		return (ArrayList<TopTextChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public ArrayList<TopFileChats> fetchTopFileChatsForUserOto(Integer user_id) {
		return (ArrayList<TopFileChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public ArrayList<TopFileChats> fetchTopFileChatsForUserGroup(Integer user_id) {
		return (ArrayList<TopFileChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public ArrayList<TopFileChats> fetchTopFileConversationsGroup() {
		return (ArrayList<TopFileChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName());
	}

	@Override
	public ArrayList<TopFileChats> fetchTopFileConversationsOto() {
		return (ArrayList<TopFileChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName());
	}

	@Override
	public ArrayList<TopTextChats> fetchTopTextConversationsOto() {
		return (ArrayList<TopTextChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName());
	}

	@Override
	public ArrayList<TopTextChats> fetchTopTextConversationsGroup() {
		return (ArrayList<TopTextChats>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName());
	}

	@Override
	public Integer insertFile(String filename, Boolean check) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				filename, check);
	}

	@Override
	public ArrayList<FileRepo> fetchFileRepo() {
		return (ArrayList<FileRepo>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName());
	}

	@Override
	public ArrayList<UserActivity> fetchUserActivity(Integer user_id) {
		return (ArrayList<UserActivity>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), user_id);
	}

	@Override
	public Integer getTotalMessagesInConversation(Integer conversation_id) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				conversation_id);
	}

	@Override
	public Integer getConversationIdBetweenUsers(Integer user_one,
			Integer user_two) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_one, user_two);
	}

	@Override
	public Integer messagesSentOnASpecificDay(String day) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(), day);
	}

	@Override
	public Hashtable<String, Integer> messagesPerDay(String timeStart,
			String timeEnd) {
		return (Hashtable<String, Integer>) execute(Thread.currentThread()
				.getStackTrace()[1].getMethodName(), timeStart, timeEnd);
	}

	@Override
	public Integer getTotalMessagesSentByUser(Integer user_id) {
		return (Integer) execute(
				Thread.currentThread().getStackTrace()[1].getMethodName(),
				user_id);
	}

}
