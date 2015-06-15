package se.bth.swatkats.letstalk.file.upload;

import java.io.File;
import java.security.PublicKey;
import java.util.Observable;  
import java.io.FileInputStream;  
import java.io.ObjectInputStream;  
import java.io.ObjectOutputStream;  
import java.net.Socket;  
import java.util.Observer;
import java.util.ArrayList;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.encryption.CryptModule;
import se.bth.swatkats.letstalk.connection.packet.internal.OpenConnectionMessage;
import se.bth.swatkats.letstalk.connection.packet.Packet;

/**
 * The fileupload class to handle File Upload.
 * 
 * @author Jyoti
 *
 */ 
public class fileupload extends Observable{ 
	
	private static final int BUFFER_SIZE = 1024; 
	
	private long FILE_SIZE,UPLOADED=0;
	
	private Socket socket;
	
	private File file;
	
	private CryptModule crypt;
	
	private ArrayList<Observer> users=new ArrayList<Observer>();
	
	/**
	 * Creates a new Connection on different port for file upload. This
	 * method uses the default values from Constants.
	 * 
	 */
    public fileupload(String path) throws Exception {  
        this.file = new File(path); 
        this.socket = new Socket(Constants.HOST, Constants.REPOSITORYUPLOADPORT);
    }
    /**
	 * @return the upload progress in terms of percentage of file uploaded
	 */
    public long getValue()
    {
       return (UPLOADED*100)/FILE_SIZE;
    }
    /**
     * Reads the file and sends it to server
     * @param fileid 
     * 			unique file id 
     * @throws Exception
     */
    public void sendFile(int fileid)throws Exception{
        
    	ObjectInputStream ois = new ObjectInputStream(socket.getInputStream());  
        ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream()); 
        /*
         * Send the encryption keys to the server
         */
        crypt=new CryptModule();
        try {
			PublicKey publicKey = crypt.initKeyExchange();
			OpenConnectionMessage m = new OpenConnectionMessage(publicKey);
			m.setSenderip(socket.getInetAddress().getHostAddress());
			oos.writeObject(m);
		} catch (Exception e) {
			System.err.print("Key exchange failed.");
			e.printStackTrace();
		}
        
        try {
			Packet openmessage = (Packet) ois.readObject();
			if (openmessage instanceof OpenConnectionMessage) {
				crypt.retreiveKey(((OpenConnectionMessage) openmessage)
						.getKey());
			} else {
				System.err
						.print("Expecting OpenConnection Message first.\n");
			}
        }catch (Exception e) {
			System.err.print("Receiving object failed.\n");
			e.printStackTrace();
		}
        /*
         * write file id which is a unique identity of file on server and in database
         */
        oos.writeObject(crypt.encrypt(fileid));
        /*
         * determine file size and write file size to object output stream
         */
        this.FILE_SIZE=file.length();
        oos.writeObject(crypt.encrypt(FILE_SIZE));
        /*
         * write file extension to object output stream to preserve the file
         */
        oos.writeObject(crypt.encrypt(getFileExtension(file.getName())));
        
        FileInputStream fis = new FileInputStream(file);  
        byte [] buffer = new byte[BUFFER_SIZE];  
        if(FILE_SIZE==0)
        {
        	this.UPLOADED=1;
        	this.FILE_SIZE=1;
            /*
             * set the observable changed to notify the users(GUI) to update upload progress
             */
            setChanged();
            notifyObservers();
        }
        while (UPLOADED < FILE_SIZE) {
        	fis.read(buffer);
        	/*
        	 * write encrypted data to object output stream
        	 */
        	oos.writeObject(crypt.encrypt(buffer));
            oos.flush();
            /*
             * update the upload progress
             */
            this.UPLOADED=Math.min(UPLOADED+1024,FILE_SIZE);
            /*
             * set the observable changed to notify the users(GUI) to update upload progress
             */
            setChanged();
            notifyObservers();
        }  
        /*
         * close file input stream, object input stream , object output stream
         */
        fis.close();
        oos.close();  
        ois.close();       
} 
    /*
     * Extracts file extension based on regular expression
     * @return file extension of the file to be uploaded 
     */
    private static String getFileExtension(String fileName) {
        if(fileName.lastIndexOf(".") != -1 && fileName.lastIndexOf(".") != 0)
        return fileName.substring(fileName.lastIndexOf(".")+1);
        else return "";
    } 
}  
  
   
