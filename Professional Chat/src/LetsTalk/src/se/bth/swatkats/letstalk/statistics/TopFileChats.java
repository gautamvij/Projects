package se.bth.swatkats.letstalk.statistics;

import java.io.Serializable;

public class TopFileChats extends TopChat implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1406435913073446665L;
	private Integer fileCount;

	public Integer getFileCount() {
		return fileCount;
	}

	public void setFileCount(Integer fileCount) {
		this.fileCount = fileCount;
	}

	public TopFileChats(Integer conversationId, Integer userOne, Integer userTwo,
			String groupName, Integer fileCount) {
		super(conversationId, userOne, userTwo, groupName);
		this.fileCount = fileCount;
		// TODO Auto-generated constructor stub
	}


}
