package se.bth.swatkats.letstalk.file.repository;
/**
 * The main class to call File Download, add observers 
 * 
 * @author Jyoti
 *
 */ 
public class downloadMain extends Thread{
	private String name;
	private String path;
	
	private String fileurl;
	
	/*
	 * initialize the path and file name variables
	 */
	   public downloadMain(String path,String name,String url)
	   {
		   this.name=name;
		   this.path=path;
		   this.fileurl=url;
	   }
	   public void run(){
		  try {
			  filedownload c=new filedownload(path,fileurl,name);
			  downloadUser u = new downloadUser(c);
			  c.addObserver(u);
		      c.saveFile();
		  }catch(Exception e) {  
	            e.printStackTrace();  
	        }  
	   }
	   private static String getFileExtension(String fileName) {
	        if(fileName.lastIndexOf(".") != -1 && fileName.lastIndexOf(".") != 0)
	        return fileName.substring(fileName.lastIndexOf(".")+1);
	        else return "";
	    } 
	   public static boolean main(String path,String name,int id) throws Exception
	   {
	      new downloadMain(path,name,id+"."+getFileExtension(name)).start();
	      return true;
	   }


}
