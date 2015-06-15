package se.bth.swatkats.letstalk.gui;

import java.awt.Toolkit;
import java.io.File;
import java.util.ArrayList;
import javax.swing.JFileChooser;
import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.connection.packet.FileRepo;
import se.bth.swatkats.letstalk.connection.packet.message.FileMessage;
import se.bth.swatkats.letstalk.user.User;

/**
 * This class provides the window which shows the user the files availables
 * to download from the repository.
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada
 */
public class FilesRepo extends javax.swing.JFrame {
    
    private ArrayList<FileRepo> files;
    UploadFile fileUpWin;
    DownloadFile fileDownWin;    
    /**
     * Creates new form FilesRepo.
     */
    public FilesRepo() {
        initComponents();
        myInitComponents();
    }
    
    /**
     * Provides modifications written by us.
     */
    private void myInitComponents(){
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));
        updateFileRepoList();
        if(GuiHandler.getInstance().getUser().getAdmin_flag() != 1){
            this.addFileBut.setVisible(false);
        }
    }
    
    /**
     * This method updates the repository list with available files.
     */
    private void updateFileRepoList(){
        filesList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = putFileNames();
            @Override
            public int getSize() { return strings.length; }
            @Override
            public Object getElementAt(int i) { return strings[i]; }
        });
    }
    
    /**
     * This mehtod gets the names of the available files.
     * 
     * @return String[] - contains the names of the available files.
     */
    private String[] putFileNames(){
        
        try{
            files = GuiHandler.getInstance().fetchFileRepo();
            System.out.println(files.size());
            String[] temp = new String[files.size()];
            int pos=0;
            for(FileRepo f: files){
                temp[pos++] = f.getFileId() + "| " + f.getFilename();
            }
            return temp;
        } catch(java.lang.NullPointerException ex){
            System.out.println("empty list of files in repo!");
            String[] temp = new String[1];
            temp[0] = "todo";
            return temp;
        }
    }
    
    /**
     * This method gets the ID of the file selected.
     * 
     * @return ID - ID of the file selected. 
     */
    private int getSelectedFileID(){
        String selectedFileID = "";
        try{
            selectedFileID = getClearFileId(filesList.getSelectedValue().toString());
        } catch(java.lang.NullPointerException ex){
            System.out.println("EXCEPTION: no file is selected on filesList.");
            return -100;
        }
        int id = Integer.parseInt(selectedFileID);
        return id;
    }
    
    /**
     * This method takes the neccesary part of the string.
     * 
     * @param dirty - String that want to be separated.
     * @return clear - The necessary part of the string.
     */
    private String getClearFileId(String dirty){
        String[] parts = dirty.split("|");
        String clear = parts[0];
        return clear;
    }
    
    /**
     * This method gets the name of the selected file.
     * 
     * @return selectedValue - Name of the selected file.
     */
    private String getSelectedFileName(){
        String selectedValue = getClearFileName(filesList.getSelectedValue().toString());
        return selectedValue;
    }
    
    /**
     * This method gets some parts of the string.
     * 
     * @param dirty - String that want to be separated.
     * @return clear - The neccesary parts of the string.
     */
    private String getClearFileName(String dirty){
        System.out.println("dirty: " + dirty);
        String[] parts = dirty.split("|");
        String clear= "";
        for(int i=2; i<parts.length; i++)
            clear += parts[i];
        
        return clear.trim();
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel2 = new javax.swing.JPanel();
        filesRepoIcon = new javax.swing.JLabel();
        jPanel1 = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        filesList = new javax.swing.JList();
        addFileBut = new javax.swing.JButton();
        closeBut = new javax.swing.JButton();
        fileRepoLabel = new javax.swing.JLabel();

        setResizable(false);

        jPanel2.setBackground(new java.awt.Color(247, 247, 247));

        filesRepoIcon.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/Change-time-file-windows.png"))); // NOI18N

        jPanel1.setBackground(new java.awt.Color(237, 237, 255));
        jPanel1.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        filesList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        filesList.addListSelectionListener(new javax.swing.event.ListSelectionListener() {
            public void valueChanged(javax.swing.event.ListSelectionEvent evt) {
                filesListValueChanged(evt);
            }
        });
        jScrollPane1.setViewportView(filesList);

        addFileBut.setText("Add File");
        addFileBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addFileButActionPerformed(evt);
            }
        });

        closeBut.setText("Close");
        closeBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                closeButActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(addFileBut, javax.swing.GroupLayout.PREFERRED_SIZE, 79, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(closeBut, javax.swing.GroupLayout.PREFERRED_SIZE, 79, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 101, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 156, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(addFileBut)
                    .addComponent(closeBut))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        fileRepoLabel.setFont(new java.awt.Font("Tahoma", 0, 18)); // NOI18N
        fileRepoLabel.setText("Files Repository");

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(23, 23, 23)
                        .addComponent(filesRepoIcon)
                        .addGap(29, 29, 29)
                        .addComponent(fileRepoLabel))
                    .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(6, 6, 6)
                        .addComponent(filesRepoIcon)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(fileRepoLabel)
                        .addGap(32, 32, 32)))
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
        );

        pack();
        setLocationRelativeTo(null);
    }// </editor-fold>//GEN-END:initComponents
    
    /**
     * When the user presses this button, he/she can add one file to the repository.
     * 
     * @param evt - event. 
     */
    private void addFileButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addFileButActionPerformed
        System.out.println("PERFORMED adding file to repo");
        
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setCurrentDirectory(new File(System.getProperty("user.home")));
        int result = fileChooser.showOpenDialog(fileChooser);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            GuiHandler.getInstance().getGui().fileUpWin = new UploadFile();
            GuiHandler.getInstance().getGui().fileUpWin.setVisible(true);
            System.out.println("selected file path: " + selectedFile.getAbsolutePath());
            GuiHandler.getInstance().startFileUpload(selectedFile.getAbsolutePath(), 0, 0, true); 
        }
        
        this.updateFileRepoList();   
    }//GEN-LAST:event_addFileButActionPerformed
    
    /**
     * This method downloads the selected file.
     * 
     * @param evt - event. 
     */
    private void filesListValueChanged(javax.swing.event.ListSelectionEvent evt) {//GEN-FIRST:event_filesListValueChanged
        if(!filesList.getValueIsAdjusting()){
            System.out.println("Files list value changed.");
            int fileID = getSelectedFileID();
            String filename = getSelectedFileName();
            System.out.println("Filename: " + filename + " id: " + fileID);
            
            String path;
            JFileChooser chooser = new JFileChooser(); 
            chooser.setCurrentDirectory(new java.io.File("."));
            chooser.setDialogTitle("Downloading file directory");
            chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

            // disable the "All files" option.
            chooser.setAcceptAllFileFilterUsed(false);

            if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) { 
              path = chooser.getSelectedFile().getAbsolutePath();
              path += "\\";
              }
            else {
              System.out.println("No Selection ");
              path = null;
            }
            
            GuiHandler.getInstance().getGui().fileDownWin = new DownloadFile();
            GuiHandler.getInstance().getGui().fileDownWin.setVisible(true);
                 
            System.out.println("path: " + path);
            System.out.println("filename: " + filename);
            System.out.println("fileID: " + fileID);
            
            GuiHandler.getInstance().startFileDownload(path, filename, fileID, true);
        }
    }//GEN-LAST:event_filesListValueChanged

    /**
     * When the user presses this button, the window is closed.
     * 
     * @param evt - event.
     */
    private void closeButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_closeButActionPerformed
        this.setVisible(false);
    }//GEN-LAST:event_closeButActionPerformed

    /**
     * Main method which starts the class.
     * 
     * @param args the command line arguments.
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(FilesRepo.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(FilesRepo.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(FilesRepo.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(FilesRepo.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new FilesRepo().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton addFileBut;
    private javax.swing.JButton closeBut;
    private javax.swing.JLabel fileRepoLabel;
    private javax.swing.JList filesList;
    private javax.swing.JLabel filesRepoIcon;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JScrollPane jScrollPane1;
    // End of variables declaration//GEN-END:variables
}
