package se.bth.swatkats.letstalk.junit;

import static org.junit.Assert.*;

import java.io.File;

import org.junit.Test;

import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.connection.packet.LoginMessage;
import se.bth.swatkats.letstalk.gui.HomePage;
import se.bth.swatkats.letstalk.gui.Login;

public class FileUploadTest {

	@Test
	public void test() {
		fail("Not yyet implemented.");
		GuiHandler.getInstance().login("g", "g_p");

		new HomePage().setVisible(true);
		
		File folder = new File("repo");
		File[] listOfFiles = folder.listFiles();

		for (int i = 0; i < listOfFiles.length; i++) {
			if (listOfFiles[i].isFile()) {
				System.out.println("File " + listOfFiles[i].getName());
				GuiHandler.getInstance().startFileUpload(
						listOfFiles[i].getAbsolutePath(), 0, 0, true);
			} else if (listOfFiles[i].isDirectory()) {
				System.out.println("Found a directory.");
			}
		}

	}

}
