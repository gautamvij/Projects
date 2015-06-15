package se.bth.swatkats.letstalk.connection;

import se.bth.swatkats.letstalk.gui.Conversation;
import se.bth.swatkats.letstalk.statistics.TopFileChats;
import se.bth.swatkats.letstalk.statistics.TopTextChats;
import se.bth.swatkats.letstalk.connection.packet.FileRepo;
import se.bth.swatkats.letstalk.connection.packet.UserActivity;
import se.bth.swatkats.letstalk.connection.packet.message.FileMessage;

import java.sql.Connection;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import se.bth.swatkats.letstalk.connection.packet.message.Message;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;
import se.bth.swatkats.letstalk.gui.Conversation;
import se.bth.swatkats.letstalk.user.User;

/**
 * 
 * @author Inanc, Jibraan, Gautam, JS
 *
 */
public interface IDatabase {

	
	/**
	 * Fetches the local address book of the user from the server.
	 * @param user_id
	 * @param phrase
	 * @return ArrayList with users with information
	 */
	public ArrayList<User> searchLocalUsers(Integer user_id, String phrase);

	/**
	 * 
	 * @param conversationId
	 * @param user_id
	 * @return The sorted text messages in the conversation as ArrayList
	 */
	public ArrayList<TextMessage> fetchTextConversationHistory(
			Integer conversationId, Integer user_id);

	/**
	 * Changes the password of the specified user in the database.
	 * 
	 * @param oldPass
	 * @param newPass
	 * @return
	 */
	public Integer changeUserPassword(Integer user_id, String username,
			String oldPass, String newPass);

	/**
	 * Sets the user status as available in the database
	 *
	 * @return true, if succeeded; false, otherwise
	 */
	public Boolean setUserStatusAvailable(Integer userid);

	/**
	 * Sets the user status as busy in the database
	 *
	 * @return
	 */
	public Boolean setUserStatusBusy(Integer userid);

	/**
	 * Adds a user to the local address book.
	 *
	 * @return true if success, false if fail
	 */
	public Boolean addLocalUser(Integer user_current, Integer user_to_add);

	/**
	 * Deletes a user from the local address book.
	 *
	 * @param userID
	 * @param receiverID
	 * @return true if success, false if fail
	 */
	public Boolean deleteUserFromLocalBook(Integer userID, Integer receiverID);

	/**
	 * Blocks a user from the local address book.
	 * @param user_id_by
	 * @param user_id_to
	 * @return true if success, false if fail
	 */
	public Boolean blockUserFromLocalBook(Integer user_id_by, Integer user_id_to);

	/**
	 * Unblocks a user from the local address book.
	 *
	 * @return true, if succeeded ; false, otherwise
	 */
	public Boolean unblockUserFromLocalBook(Integer user_id_by, Integer user_id_to);

	/**
	 * Deletes user from global address book.
	 * @return true, if successful; false if an exception is caught
	 */
	public Boolean deleteUser(Integer user_id);
	
	/**
	 * Gets blocked users by the user who has user_id
	 * @param user_id
	 * @return List of blocked users as ArrayList
	 */
	public ArrayList<User> fetchBlockedUsers(Integer user_id);
	
	/**
	 * Inserts user to the conversation
	 * @param conv_id id of the conversation
	 * @param user_id id of the user to be added
	 * @return true, if successful; false, otherwise
	 */
	public Boolean insertUserToGroup(Integer conv_id, Integer user_id );
	
	/**
	 * Creates user, inserts into users table
	 * @param username
	 * @param password
	 * @param email
	 * @param isAdmin
	 * @return 0, if an SQL Exception caught;
	 * 		-1 if username already exists;	
	 * 		user_id, if successful.
	 */
	public Integer createUser(String username, String password, String email,
			Boolean isAdmin);

	/**
	 * Creates conversation between users, inserts into converstaions table
	 * @param user_one
	 * @param user_two
	 * @param chat_type 0 for group conversations, 1 for one-to-one conversations
	 * @param g_name
	 * @return conversation_id, if successful; -1 if an error is caught
	 */
	public Integer createConversation(Integer user_one, Integer user_two, Integer chat_type, String g_name);

	/**
	 * Searches users from global address book
	 * @param phrase Phrase to be searched
	 * @param user_id
	 * @return Results as ResultSet
	 */
	public ArrayList<User> searchGlobalUsers(String phrase, Integer user_id);

	/**
	 * Gets conversations for user
	 * @param user_id
	 * @return Conversations in an ArrayList
	 */
	public ArrayList<Conversation> fetchConversationsForUser(Integer user_id);

	/**
	 * 
	 * @param conversationId
	 * @param user_id
	 * @return The sorted text messages in the conversation as ArrayList
	 */
	public ArrayList<FileMessage> fetchFileConversationHistory(
			Integer conversationId, Integer user_id);

	/**
	 * Sets the user status as offline in the database
	 * @param userid
	 * @return true, if succeeded; false, otherwise
	 */
	public Boolean setUserStatusOffline(Integer userid);

	/**
	 * Sets the user status as idle in the database
	 * @param userid
	 * @return true, if succeeded; false, otherwise
	 */
	public Boolean setUserStatusIdle(Integer userid);

	public ArrayList<User> usersFromGroup(Integer conv_id, Integer user_id);

	public ArrayList<TopTextChats> fetchTopTextChatsForUserGroup(Integer user_id);

	public ArrayList<TopTextChats> fetchTopTextChatsForUserOto(Integer user_id);

	public ArrayList<TopFileChats> fetchTopFileChatsForUserOto(Integer user_id);

	public ArrayList<TopFileChats> fetchTopFileChatsForUserGroup(Integer user_id);

	public ArrayList<TopFileChats> fetchTopFileConversationsGroup();

	public ArrayList<TopFileChats> fetchTopFileConversationsOto();

	public ArrayList<TopTextChats> fetchTopTextConversationsOto();

	public ArrayList<TopTextChats> fetchTopTextConversationsGroup();

	public Integer insertFile(String filename, Boolean check);

	public ArrayList<FileRepo> fetchFileRepo();

	public ArrayList<UserActivity> fetchUserActivity(Integer user_id);

	/**
	 * Gets total number of messages in a conversation.
	 * @param conversation_id the conversation which message number will be calculated.
	 * @return Message count(greater or equal to 0) if succeeded; -1 if an error occurred.
	 */
	public Integer getTotalMessagesInConversation(Integer conversation_id);
	
	/**
	 * Gets the one-to-one conversation ID between two users.
	 * @param user_one
	 * @param user_two
	 * @return conv_id,if successful; 0, if no conversation found; -1,if an error occurred.
	 */
	public Integer getConversationIdBetweenUsers(Integer user_one, Integer user_two);
	
	/**
	 * Gets user message sending activity in a specific day.
	 * @param day in format of "YYYY-MM-DD"
	 * @return count of messages sent on a day, if successful; -1 if an error occured.
	 */
	public Integer messagesSentOnASpecificDay(String day);
	
	/**
	 * Gets statistics of messages sent in the time interval for graphs.
	 * @param timeStart in format of "YYYY-MM-DD"
	 * @param timeEnd in format of "YYYY-MM-DD"
	 * @return messages/day if the interval is less than 2 months; messages/weeks if 2 months is less than the interval 10 months ; messages/months if 10 months is less than the interval 5 years ; message/years otherwise 
	 */
	public Hashtable<String, Integer> messagesPerDay(String timeStart, String timeEnd);
	
	/**
	 * Gets all time message count of the user
	 * @param user_id the user's id
	 * @return count of total messages sent
	 */
	public Integer getTotalMessagesSentByUser(Integer user_id);

}
