package se.bth.swatkats.letstalk.statistics;

import java.io.Serializable;

public class TopTextChats extends TopChat implements Serializable {
	/**
	 * 
	 */
	private static final long serialVersionUID = -6887408348307139747L;
	private Integer textCount;

	public Integer getTextCount() {
		return textCount;
	}

	public void setTextCount(Integer textCount) {
		this.textCount = textCount;
	}

        public void increaseTextCount(Integer more){
                this.textCount = textCount + more;
        }
	public TopTextChats(Integer conversationId, Integer userOne, Integer userTwo,
			String groupName, Integer textCount) {
		super(conversationId, userOne, userTwo, groupName);
		this.textCount = textCount;
	}

	

}
