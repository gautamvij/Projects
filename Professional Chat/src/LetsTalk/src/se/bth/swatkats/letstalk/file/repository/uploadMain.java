package se.bth.swatkats.letstalk.file.repository;
/**
 * The main class to call File Upload, add observers 
 * 
 * @author Jyoti
 *
 */ 
public class uploadMain extends Thread{
	private String path;
	
	private int fileid;
	/*
	 * initialize the path and file id variables
	 */
	   public uploadMain(String path,int fileid)
	   {
		   this.path=path;
		   this.fileid=fileid;
	   }
	   @Override
	   public void run(){
		  try {
			  fileupload c=new fileupload(path);
			  uploadUser u = new uploadUser(c);
			  c.addObserver(u);
		      c.sendFile(fileid);
		  }catch(Exception e) {  
	            e.printStackTrace();  
	        }  
	   }
	  public static boolean main(String path,int fileid) throws Exception
	   {
	      new uploadMain(path,fileid).start();
	      return true;
	   }
}
