package se.bth.swatkats.letstalk.file.repository;
import java.io.File; 
import java.io.FileOutputStream;  
import java.io.ObjectInputStream;  
import java.io.ObjectOutputStream;  
import java.net.Socket;
import java.security.PublicKey;
import java.util.Observable;
import java.util.Observer;
import java.util.ArrayList;

import javax.crypto.SealedObject;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.connection.encryption.CryptModule;
import se.bth.swatkats.letstalk.connection.packet.internal.OpenConnectionMessage;
import se.bth.swatkats.letstalk.connection.packet.Packet;
/**
 * The filedownload class to handle File Download.
 * 
 * @author Jyoti
 *
 */ 
public class filedownload extends Observable {
	
	private static final int BUFFER_SIZE = 1024; 
	
	private Socket socket;
	
	private FileOutputStream fos = null;
	
	private String fileurl;
	
	private CryptModule crypt;
	
    private SealedObject message;
	
	private long FILE_SIZE,DOWNLOADED=0;
	
	private ArrayList<Observer> users=new ArrayList<Observer>();
	/**
	 * @return the upload progress in terms of percentage of file uploaded
	 */
	public long getValue()
    {
       return (DOWNLOADED*100)/FILE_SIZE;
    }
	/**
	 * Creates a new Connection on different port for file download. This
	 * method uses the default values from Constants.
	 *            
	 */
    public filedownload(String path,String fileurl,String filename) {  
		try { 
			    fos = new FileOutputStream(new File (path+filename));
			    this.fileurl=fileurl;
                socket = new Socket(Constants.HOST, Constants.REPOSITORYDOWNLOADPORT); 
        } catch (Exception e) {  
            e.printStackTrace();  
        }    
      }  
    /**
     * Reads from object input stream and saves it in a file
     */
	  public void saveFile() throws Exception
	  {	  
		    crypt=new CryptModule();
	        ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream());  
	           
	        byte [] buffer = new byte[BUFFER_SIZE];  
	        
	        try {
				PublicKey publicKey = crypt.initKeyExchange();
				OpenConnectionMessage m = new OpenConnectionMessage(publicKey);
				m.setSenderip(socket.getInetAddress().getHostAddress());
				oos.writeObject(m);
			} catch (Exception e) {
				System.err.print("Key exchange failed.");
				e.printStackTrace();
			}
	        ObjectInputStream ois = new ObjectInputStream(socket.getInputStream());
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
	  
	        // Write file path from where file is to be read.  
	        Object file ;  
	        oos.writeObject(crypt.encrypt(fileurl));  
	        //Read file size to determine download progress 
	        message = (SealedObject) ois.readObject();
	        FILE_SIZE=(long) crypt.decrypt(message);
	  
	        //Read and save file to the end.  
	        int size =0;
	        long remain=FILE_SIZE;
	        if(FILE_SIZE==0)
	        {
	        	this.DOWNLOADED=1;
	        	this.FILE_SIZE=1;
	            /*
	             * set the observable changed to notify the users(GUI) to update upload progress
	             */
	            setChanged();
	            notifyObservers();
	        }
	        while (DOWNLOADED < FILE_SIZE){  	  
	        	size=Math.min(1024,(int)remain);
	        	message = (SealedObject) ois.readObject();
            	buffer=(byte[]) crypt.decrypt(message);
            	remain=Math.max(0,remain-1024);
	  
	            //Write data to output file.  
	            fos.write(buffer, 0,Math.min(1024,(int)(remain))); 
	            this.DOWNLOADED=Math.min(DOWNLOADED+1024,FILE_SIZE);
	            setChanged();
	            notifyObservers();
	            
	        }   
	          
	        System.out.println("File transfer success");  
	        /*
	         * close file input stream, object input stream , object output stream
	         */ 
	        fos.close();  
	        ois.close();  
	        oos.close();  
	    }
  public static void throwException(String message) throws Exception {  
      throw new Exception(message);  
  }
}
 

