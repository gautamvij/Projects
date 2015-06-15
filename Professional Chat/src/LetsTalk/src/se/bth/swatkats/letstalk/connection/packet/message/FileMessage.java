package se.bth.swatkats.letstalk.connection.packet.message;

import java.sql.Timestamp;

/**
 * File Message, usually an upload, that is available for download.
 * 
 * @author JS
 *
 */
public class FileMessage extends Message {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6211493495565200646L;

	private String filename;

	private int fileid;

	/**
	 * @return the filename
	 */
	public String getFilename() {
		return filename;
	}

	/**
	 * @param filename
	 *            the filename to set
	 */
	public void setFilename(String filename) {
		this.filename = filename;
	}

	/**
	 * @return the file_id
	 */
	public int getFileid() {
		return fileid;
	}

	/**
	 * @param file_id
	 *            the file_id to set
	 */
	public void setFileid(int file_id) {
		this.fileid = file_id;
	}

	public FileMessage(int receiver, int convid, String filename, int file_id) {
		super(receiver, convid);
		this.filename = filename;
		this.fileid = file_id;
	}

	public FileMessage(String filename, String username, int file_id,
			int senderid, Timestamp time, int receiver, int convid,
			String senderip) {
		super(senderid, username, time, receiver, convid, senderip);
		this.filename = filename;
		this.fileid = file_id;
	}

}
