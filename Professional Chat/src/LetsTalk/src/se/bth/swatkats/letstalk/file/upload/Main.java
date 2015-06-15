package se.bth.swatkats.letstalk.file.upload;
/**
 * The main class to call File Upload, add observers 
 * 
 * @author Jyoti
 *
 */ 
public class Main extends Thread{
	private String path;
	
	private int fileid;
	/*
	 * initialize the path and file id variables
	 */
	   public Main(String path,int fileid)
	   {
		   this.path=path;
		   this.fileid=fileid;
	   }
	   @Override
	   public void run(){
		  try {
			  fileupload c=new fileupload(path);
			  user u = new user(c);
			  c.addObserver(u);
		      c.sendFile(fileid);
		  }catch(Exception e) {  
	            e.printStackTrace();  
	        }  
	   }
	  public static boolean main(String path,int fileid) throws Exception
	   {
	      new Main(path,fileid).start();
	      return true;
	   }
}
