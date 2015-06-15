package se.bth.swatkats.letstalk.file.repository;
/**
 * The user class to observe file download progress 
 * 
 * @author Jyoti
 *
 */ 
import java.util.Observer;
import java.util.Observable;
public class user implements Observer {
	private long downloaded;
	private filedownload file;
	public user(filedownload file){
	      this.file = file;
	   }
@Override
	   public void update(Observable obs, Object obj){
		if (obs == file)
		{
		   this.downloaded=file.getValue();
	   }
}
}
