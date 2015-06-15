package se.bth.swatkats.letstalk.connection.packet;

import java.io.Serializable;

public class FileRepo implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -5622163894604086161L;
	private int fileId;
	private String filename;
	public FileRepo(int fileId, String filename) {
		super();
		this.fileId = fileId;
		this.filename = filename;
	}
	public int getFileId() {
		return fileId;
	}
	public void setFileId(int fileId) {
		this.fileId = fileId;
	}
	public String getFilename() {
		return filename;
	}
	public void setFilename(String filename) {
		this.filename = filename;
	}
	

}
