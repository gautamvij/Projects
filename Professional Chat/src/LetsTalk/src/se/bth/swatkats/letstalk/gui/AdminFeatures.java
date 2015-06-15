package se.bth.swatkats.letstalk.gui;

import java.awt.Toolkit;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Hashtable;
import java.util.Objects;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import static javax.swing.JOptionPane.showMessageDialog;
import javax.swing.ListSelectionModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.connection.packet.UserActivity;
import se.bth.swatkats.letstalk.statistics.TopChat;
import se.bth.swatkats.letstalk.statistics.TopFileChats;
import se.bth.swatkats.letstalk.statistics.TopTextChats;
import se.bth.swatkats.letstalk.user.User;

/**
 * This class provides the window which lets admin do certain operations
 * relative with users.
 * 
 * @author Sokratis and David Alarcon.
 */
public class AdminFeatures extends javax.swing.JFrame {

    //stores the global users of the application
    private ArrayList<User> globalUsers;
    
    //one to one
    private ArrayList<TopTextChats> textOtO;
    private ArrayList<TopFileChats> fileOtO;

    //group
    private ArrayList<TopTextChats> textGroup;
    private ArrayList<TopFileChats> fileGroup;
    
    private ArrayList<TopChat> oTo;
    private ArrayList<TopChat> group;
    private ArrayList<TopChat> all;

    
    /**
     * Creates new form AdminFeatures.
     */
    public AdminFeatures() {
        initComponents();
        myInitComponents();
    }
    
    /**
     * Provides modifications written by us.
     */
    private void myInitComponents(){
        
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));
        updateUsersToDelete();
        loadGlobalConversations();
    }
    
    /**
     * This method load all the active conversation in the system.
     */
    private void loadGlobalConversations(){
        //one to one
        textOtO = GuiHandler.getInstance().fetchTopTextConversationsOto();
        fileOtO = GuiHandler.getInstance().fetchTopFileConversationsOto();
        
        //group
        textGroup = GuiHandler.getInstance().fetchTopTextConversationsGroup();
        fileGroup = GuiHandler.getInstance().fetchTopFileConversationsGroup();
                
        //merge one to one
        oTo = new ArrayList<>();
        oTo.addAll(textOtO);
        
        for(TopFileChats c : fileOtO){
            boolean found =false;
            for(TopChat t : oTo){
                if(Objects.equals(c.getConversationId(), t.getConversationId())){
                    ((TopTextChats) t).increaseTextCount(c.getFileCount());
                    found = true;
                    break;
                }
            }
            if(!found){
                oTo.add(c);
            }
        }               
        
        //merge group
        group = new ArrayList<>();
        group.addAll(textGroup);
        
        for(TopFileChats c : fileGroup){
            boolean found =false;
            for(TopChat t : group){
                if(Objects.equals(c.getConversationId(), t.getConversationId())){
                    ((TopTextChats) t).increaseTextCount(c.getFileCount());
                    found = true;
                    break;
                }
            }
            if(!found){
                group.add(c);
            }
        }             
                
        //merge all
        all = new ArrayList<>();
        all.addAll(oTo);
        all.addAll(group);
        
        Collections.sort(all, new Comparator<TopChat>(){
            @Override
            public int compare(TopChat c1, TopChat c2) {
                Integer count1= getMessageCount(c1);
                Integer count2= getMessageCount(c2);
                return count2.compareTo(count1);
            }
        });
        
        callRecords.setModel(new javax.swing.table.DefaultTableModel(putElements(all),putColumns()));
        callRecords.setRowSelectionAllowed(true);
        this.callRecords.getColumnModel().getColumn(0).setPreferredWidth(15);
        this.callRecords.getColumnModel().getColumn(1).setPreferredWidth(75);
        this.callRecords.getColumnModel().getColumn(2).setPreferredWidth(75);
        this.callRecords.getColumnModel().getColumn(3).setPreferredWidth(15);
        ListSelectionModel rowSelectionModel = callRecords.getSelectionModel();
        rowSelectionModel.addListSelectionListener(new ListSelectionListener() {

            @Override
            public void valueChanged(ListSelectionEvent lse) { //open the conversation window with relevant info
                if (!lse.getValueIsAdjusting()){
                    int selectedRow = callRecords.getSelectedRow();
                    CallRecords cr = new CallRecords((int) callRecords.getValueAt(selectedRow, 0), 
                                                     (String) callRecords.getValueAt(selectedRow, 1),
                                                     (String) callRecords.getValueAt(selectedRow, 2));
                    cr.setVisible(true);
                }
            }
        });
    }
    
    private String getUsername(int id){
        ArrayList<User> users = new ArrayList<>();
        users.add(GuiHandler.getInstance().getUser());
        users.addAll(globalUsers);
        for(User u : users){
            if(u.getId() == id){
                return u.getUsername();
            }
        }
        return null;
    }
    
    private Object[][] putElements(ArrayList<TopChat> all){
        Object[][] temp = new Object[10][4];
        int count =0;
        
        for(TopChat c: all){
            temp[count][0] = c.getConversationId();
            
            if(c.getUserTwo()== -10){ //group chat
                temp[count][1] = c.getGroupName();
                temp[count][2] = "(Group Chat)";
            } else{ //one-to-one chat
                temp[count][1] = getUsername(c.getUserOne());
                temp[count][2] = getUsername(c.getUserTwo());
            }
            temp[count][3] = getMessageCount(c);
            count++;
            
            if(count == 10){
                return temp;
            }
        }
        return temp;
    }
    
    private String[] putColumns(){
        String[] temp = { "ConvID", "User One", "User Two" , "Count"};
        return temp;
    }
    
    /**
     * This method show the conversations' name.
     * @param all - All the conversations.
     * @return - String[] contains specific information of the conversations.
     */
    private String[] putConversations(ArrayList<TopChat> all){
        
        String[] temp = new String[all.size()];
        int count=0;
        int i=1;
        
        for(TopChat c: all){
            System.out.println(i + ". id:" +c.getConversationId() + " with user: " + c.getUserOne() + " or group: " + c.getGroupName() + " where he had: " + getMessageCount(c) + " messages exchanged.");
            
            if(c.getGroupName()!=null){ //group chat
                temp[count] = count + ". " + c.getGroupName() + " " + getMessageCount(c);
                count++;
            } else {//one-to-one chat
                for(User u : GuiHandler.getInstance().searchLocalUsers(GuiHandler.getInstance().getUser().getId(), "")){
                    if(u.getId() == c.getUserOne()){
                        temp[count] = count + ". " + u.getUsername() + " " + getMessageCount(c);
                        count++;
                    }
                }
            }
            
            if(count == 10){
                return temp;
            }
        }
        return temp;
    }
    
    /**
     * This method counts the messages/files existing into a conversation.
     * 
     * @param c - Set of messages or files.
     * @return count - Number of messages or files.
     */
    private Integer getMessageCount(TopChat c){
        Integer count=0;
        if(c instanceof TopTextChats){
            count = ((TopTextChats) c).getTextCount();
        }else{
            count = ((TopFileChats) c).getFileCount();
        }
        
        return count;
    }
    
    /**
     * This method updates the list users, with all the user of the system
     * in order to can select one of them for delete.
     */
    private void updateUsersToDelete(){
        selectUserToDelete.setModel(new javax.swing.DefaultComboBoxModel(putNames()));
    }

    /**
     * This method gets the users from the database.
     * 
     * @return temp - This String[] contains all the users of the system.
     */
    private String[] putNames(){
        globalUsers = GuiHandler.getInstance().searchGlobalUsers("",GuiHandler.getInstance().getUser().getId());
        String[] temp = new String[globalUsers.size()];
        int pos=0;
        for(User u: globalUsers){
            temp[pos++] = u.getUsername() + " - " + u.getEmail();
        }
        return temp;
    }
    
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jScrollPane1 = new javax.swing.JScrollPane();
        jTextArea1 = new javax.swing.JTextArea();
        jPanel2 = new javax.swing.JPanel();
        adminPanelIcon2 = new javax.swing.JLabel();
        jPanel1 = new javax.swing.JPanel();
        blockUserImg = new javax.swing.JLabel();
        addUserImg = new javax.swing.JLabel();
        performAddUserButton = new javax.swing.JButton();
        cancelButton = new javax.swing.JButton();
        deleteUserImg = new javax.swing.JLabel();
        selectUserToDelete = new javax.swing.JComboBox();
        performDeleteUserButton1 = new javax.swing.JButton();
        graphsImg = new javax.swing.JLabel();
        viewGraphsBut = new javax.swing.JButton();
        usernameLabel = new javax.swing.JLabel();
        emailLabel = new javax.swing.JLabel();
        passLabel = new javax.swing.JLabel();
        adminPropertiesInput = new javax.swing.JCheckBox();
        passInput = new javax.swing.JPasswordField();
        usernameInput = new javax.swing.JTextField();
        emailInput = new javax.swing.JTextField();
        jScrollPane2 = new javax.swing.JScrollPane();
        callRecords = new javax.swing.JTable();
        jLabel3 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        blockUnblockUserLabel = new javax.swing.JLabel();

        jTextArea1.setColumns(20);
        jTextArea1.setRows(5);
        jScrollPane1.setViewportView(jTextArea1);

        setResizable(false);

        jPanel2.setBackground(new java.awt.Color(247, 247, 247));

        adminPanelIcon2.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/adminPanel.png"))); // NOI18N

        jPanel1.setBackground(new java.awt.Color(237, 237, 255));
        jPanel1.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        blockUserImg.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/call_recorder_icon.png"))); // NOI18N
        blockUserImg.setText("Call records");

        addUserImg.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/addUser.png"))); // NOI18N
        addUserImg.setText("Add user");

        performAddUserButton.setText("Add");
        performAddUserButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                performAddUserButtonActionPerformed(evt);
            }
        });

        cancelButton.setText("Close");
        cancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                cancelButtonActionPerformed(evt);
            }
        });

        deleteUserImg.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/deleteUser.png"))); // NOI18N
        deleteUserImg.setText("Delete user");

        performDeleteUserButton1.setText("Delete");
        performDeleteUserButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                performDeleteUserButton1ActionPerformed(evt);
            }
        });

        graphsImg.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/barChart.png"))); // NOI18N
        graphsImg.setText("Graphs");

        viewGraphsBut.setText("View relevant graphs on LetsTalk usage");
        viewGraphsBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                viewGraphsButActionPerformed(evt);
            }
        });

        usernameLabel.setText("Username:");

        emailLabel.setText("Email:");

        passLabel.setText("Pass:");

        adminPropertiesInput.setBackground(new java.awt.Color(237, 237, 255));
        adminPropertiesInput.setLabel("Admin Properties");
        adminPropertiesInput.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                adminPropertiesInputActionPerformed(evt);
            }
        });

        callRecords.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "null", "null", "Title 3", "Title 4"
            }
        ));
        jScrollPane2.setViewportView(callRecords);

        jLabel3.setFont(new java.awt.Font("Tahoma", 2, 13)); // NOI18N
        jLabel3.setText("Click on the conversation to see more info");

        jLabel5.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/top-10.png"))); // NOI18N

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                .addComponent(blockUserImg)
                                .addGap(44, 44, 44)
                                .addComponent(jLabel3, javax.swing.GroupLayout.PREFERRED_SIZE, 249, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(40, 40, 40))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                .addComponent(jLabel5)
                                .addGap(36, 36, 36)
                                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 325, javax.swing.GroupLayout.PREFERRED_SIZE))))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addComponent(addUserImg)
                                .addGap(17, 17, 17)
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                            .addComponent(passLabel, javax.swing.GroupLayout.Alignment.TRAILING)
                                            .addComponent(emailLabel, javax.swing.GroupLayout.Alignment.TRAILING))
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                            .addComponent(passInput, javax.swing.GroupLayout.DEFAULT_SIZE, 228, Short.MAX_VALUE)
                                            .addComponent(emailInput)))
                                    .addGroup(jPanel1Layout.createSequentialGroup()
                                        .addGap(25, 25, 25)
                                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                            .addGroup(jPanel1Layout.createSequentialGroup()
                                                .addComponent(adminPropertiesInput)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                                .addComponent(performAddUserButton, javax.swing.GroupLayout.PREFERRED_SIZE, 79, javax.swing.GroupLayout.PREFERRED_SIZE))
                                            .addGroup(jPanel1Layout.createSequentialGroup()
                                                .addComponent(usernameLabel)
                                                .addGap(17, 17, 17)
                                                .addComponent(usernameInput, javax.swing.GroupLayout.PREFERRED_SIZE, 228, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addGap(0, 0, Short.MAX_VALUE))))))
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(jPanel1Layout.createSequentialGroup()
                                        .addComponent(deleteUserImg)
                                        .addGap(28, 28, 28)
                                        .addComponent(selectUserToDelete, javax.swing.GroupLayout.PREFERRED_SIZE, 211, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addGap(18, 18, 18)
                                        .addComponent(performDeleteUserButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 79, javax.swing.GroupLayout.PREFERRED_SIZE))
                                    .addComponent(graphsImg))
                                .addGap(0, 0, Short.MAX_VALUE))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                .addGap(0, 0, Short.MAX_VALUE)
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(cancelButton, javax.swing.GroupLayout.PREFERRED_SIZE, 132, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(viewGraphsBut, javax.swing.GroupLayout.PREFERRED_SIZE, 325, javax.swing.GroupLayout.PREFERRED_SIZE))))))
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(47, 47, 47)
                        .addComponent(addUserImg)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(21, 21, 21)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(usernameLabel, javax.swing.GroupLayout.PREFERRED_SIZE, 27, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(usernameInput, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(passInput)
                            .addComponent(passLabel))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(emailLabel, javax.swing.GroupLayout.PREFERRED_SIZE, 21, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(emailInput, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(21, 21, 21)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(performAddUserButton)
                            .addComponent(adminPropertiesInput))
                        .addGap(26, 26, 26)))
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(22, 22, 22)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(selectUserToDelete, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(performDeleteUserButton1)))
                    .addComponent(deleteUserImg))
                .addGap(41, 41, 41)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(blockUserImg)
                    .addComponent(jLabel3))
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(2, 2, 2)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 189, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(47, 47, 47)
                        .addComponent(jLabel5)))
                .addGap(18, 18, 18)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(viewGraphsBut)
                    .addComponent(graphsImg))
                .addGap(18, 18, 18)
                .addComponent(cancelButton)
                .addContainerGap())
        );

        blockUnblockUserLabel.setFont(new java.awt.Font("Tahoma", 0, 18)); // NOI18N
        blockUnblockUserLabel.setText("Admin Panel");

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGap(121, 121, 121)
                .addComponent(adminPanelIcon2)
                .addGap(38, 38, 38)
                .addComponent(blockUnblockUserLabel)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(adminPanelIcon2))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(28, 28, 28)
                        .addComponent(blockUnblockUserLabel)))
                .addGap(18, 18, 18)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );

        pack();
        setLocationRelativeTo(null);
    }// </editor-fold>//GEN-END:initComponents

    /**
     * When the admin presses this button, a new window with statistical graphs 
     * are showed.
     * 
     * @param evt - event.
     */
    private void viewGraphsButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_viewGraphsButActionPerformed
        // TODO add your handling code here:
        Graphs graphsWin = new Graphs();
    	graphsWin.setVisible(true);
    }//GEN-LAST:event_viewGraphsButActionPerformed

    /**
     * When the admin presses this button, the window is closed.
     * 
     * @param evt - event.
     */
    private void cancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_cancelButtonActionPerformed
        this.setVisible(false);
    }//GEN-LAST:event_cancelButtonActionPerformed

   
    /**
     * When the admin select the check button, it will be marked.
     * 
     * @param evt - event.
     */
    private void adminPropertiesInputActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_adminPropertiesInputActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_adminPropertiesInputActionPerformed
    
    /**
     * When the admin presess this button, the action (delete user) is 
     * performed.
     * 
     * @param evt - event.
     */
    private void performDeleteUserButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_performDeleteUserButton1ActionPerformed
        String selectedUserName = this.selectUserToDelete.getSelectedItem().toString();
        System.out.println("user to delete: "+ selectedUserName);
        globalUsers = GuiHandler.getInstance().searchGlobalUsers("",GuiHandler.getInstance().getUser().getId());
        //System.out.println("start the for each loop to find the guy to delete");
        for(User u: globalUsers){
            if(selectedUserName.equals(u.getUsername() +" - " + u.getEmail())){
                System.out.println("found user to be deleted. Time to call the function (and pray) ----id:" + u.getId());
                GuiHandler.getInstance().deleteUser(u.getId());
                break;
            }
        }
    }//GEN-LAST:event_performDeleteUserButton1ActionPerformed
    
    /**
     * This method checks if the email has the correct format.
     * 
     * @param email - Direction to check.
     * @return - True if it has correct format, false if not.
     */
    public static boolean isValidEmailAddress(String email) {
        boolean result = true;
        try {
           InternetAddress emailAddr = new InternetAddress(email);
           emailAddr.validate();
        } catch (AddressException ex) {
           result = false;
        }
        return result;
     }
    
    /**
     * When the admin presses this button, the action (add user) is 
     * performed.
     * 
     * @param evt - event.
     */
    private void performAddUserButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_performAddUserButtonActionPerformed
       
        if(usernameInput.getText().equals("")){
            showMessageDialog(null,"Please insert username!");
        } else if (passInput.getText().equals("")){
            showMessageDialog(null,"Please insert password!");
        } else if (emailInput.getText().equals("")){
            showMessageDialog(null,"Please insert email!");
        } else if (!isValidEmailAddress(emailInput.getText())){
            showMessageDialog(null,"Please insert a valid email!");
        } else {
            GuiHandler.getInstance().createUser(usernameInput.getText(), passInput.getText(), emailInput.getText(), adminPropertiesInput.isSelected());
            showMessageDialog(null,"User " + usernameInput.getText() + " was successfully created!");
            updateUsersToDelete();
            
            usernameInput.setText("");
            passInput.setText("");
            emailInput.setText("");
            adminPropertiesInput.setSelected(false);
        }
    }//GEN-LAST:event_performAddUserButtonActionPerformed

    
    private int getTextCountForOtO(int userID){
        
        for(TopTextChats t : textOtO){
            if(t.getUserOne() == userID){
                return t.getTextCount();
            }
        }
        return 0;
    }
    
    private int getTextCountForGroup(String convName){
        
        for(TopTextChats t : textGroup){
            if(t.getGroupName().equals(convName)){
                return t.getTextCount();
            }
        }
        return 0;
    }
    
    private int getFileCountForOtO(int userID){
        for(TopFileChats t : fileOtO){
            if(t.getUserOne() == userID){
                return t.getFileCount();
            }
        }
        return 0;
    }
    
    private int getFileCountForGroup(String convName){
        for(TopFileChats t : fileGroup){
            if(t.getGroupName().equals(convName)){
                return t.getFileCount();
            }
        }
        return 0;
    }
    
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
            java.util.logging.Logger.getLogger(AdminFeatures.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(AdminFeatures.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(AdminFeatures.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(AdminFeatures.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new AdminFeatures().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel addUserImg;
    private javax.swing.JLabel adminPanelIcon2;
    private javax.swing.JCheckBox adminPropertiesInput;
    private javax.swing.JLabel blockUnblockUserLabel;
    private javax.swing.JLabel blockUserImg;
    private javax.swing.JTable callRecords;
    private javax.swing.JButton cancelButton;
    private javax.swing.JLabel deleteUserImg;
    private javax.swing.JTextField emailInput;
    private javax.swing.JLabel emailLabel;
    private javax.swing.JLabel graphsImg;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTextArea jTextArea1;
    private javax.swing.JPasswordField passInput;
    private javax.swing.JLabel passLabel;
    private javax.swing.JButton performAddUserButton;
    private javax.swing.JButton performDeleteUserButton1;
    private javax.swing.JComboBox selectUserToDelete;
    private javax.swing.JTextField usernameInput;
    private javax.swing.JLabel usernameLabel;
    private javax.swing.JButton viewGraphsBut;
    // End of variables declaration//GEN-END:variables
}
