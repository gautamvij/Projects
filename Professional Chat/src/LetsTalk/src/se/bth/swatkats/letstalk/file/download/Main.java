package se.bth.swatkats.letstalk.file.download;
/**
 * The main class to call File Download, add observers 
 * 
 * @author Jyoti
 *
 */ 
public class Main extends Thread{
	private String name;
	private String path;
	
	private String fileurl;
	
	/*
	 * initialize the path and file name variables
	 */
	   public Main(String path,String name,String url)
	   {
		   this.name=name;
		   this.path=path;
		   this.fileurl=url;
	   }
	   public void run(){
		  try {
			  filedownload c=new filedownload(path,fileurl,name);
			  user u = new user(c);
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
	      new Main(path,name,id+"."+getFileExtension(name)).start();
	      return true;
	   }


}
