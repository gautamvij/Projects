package se.bth.swatkats.letstalk.file.download;
/**
 * The user class to observe file download progress 
 * 
 * @author Jyoti
 *
 */ 
import java.util.Observer;
import java.util.Observable;
import se.bth.swatkats.letstalk.connection.GuiHandler;
public class user implements Observer {
	private int downloaded;
	private filedownload file;
	public user(filedownload file){
	      this.file = file;
	   }
@Override
	   public void update(Observable obs, Object obj){
		if (obs == file)
		{
		   this.downloaded= (int) file.getValue();
                   GuiHandler.getInstance().getGui().updateDownloadProgress(downloaded);
	   }
}
}
