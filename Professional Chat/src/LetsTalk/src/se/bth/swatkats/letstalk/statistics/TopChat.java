package se.bth.swatkats.letstalk.statistics;

import java.io.Serializable;


public class TopChat implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 5870551810222808658L;
	private Integer conversationId, userOne, userTwo;
	private String groupName;
	public Integer getConversationId() {
		return conversationId;
	}
	public void setConversationId(Integer conversationId) {
		this.conversationId = conversationId;
	}
	public Integer getUserOne() {
		return userOne;
	}
	public void setUserOne(Integer userOne) {
		this.userOne = userOne;
	}
	public Integer getUserTwo() {
		return userTwo;
	}
	public void setUserTwo(Integer userTwo) {
		this.userTwo = userTwo;
	}
	public String getGroupName() {
		return groupName;
	}
	public void setGroupName(String groupName) {
		this.groupName = groupName;
	}
	public TopChat(Integer conversationId, Integer userOne, Integer userTwo,
			String groupName) {
		super();
		this.conversationId = conversationId;
		this.userOne = userOne;
		this.userTwo = userTwo;
		this.groupName = groupName;
	}
	

}
