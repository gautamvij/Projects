package se.bth.swatkats.letstalk.gui;

import java.awt.Toolkit;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.user.User;

/**
 * This class provides the window which lets user to add other user to the 
 * group conversation
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada.
 */
public class AddUserToGroupChat extends javax.swing.JFrame {
    private ArrayList<User> globalUsers;
    
    /**
     * Creates new form AddUserToGroupChat
     */
    public AddUserToGroupChat() {
        initComponents();
        myInitComponents();
    }

    /**
     * Provides modifications written by us.
     */
    private void myInitComponents(){
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));
        selectUserToAdd.setModel(new javax.swing.DefaultComboBoxModel(putNames()));
        
        this.addWindowListener(new WindowAdapter(){
            @Override
            public void windowClosing(WindowEvent event){
                GuiHandler.getInstance().getGui().updateContacts();
                setVisible(false);
            }
        });
        
        updateCurrentGroupChatUsers();
    }
    
    /**
     * This method updates the current group chat.
     */
    private void updateCurrentGroupChatUsers(){
        System.out.println("---update current group chat users---");
        usersInChatList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = insertCurrentGroupChatUsers();
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        }); 
    }
    
    /**
     * This method returns users in the current group chat.
     * 
     * @return temp - This String[] contains all the users in the current group chat.
     */
    private String[] insertCurrentGroupChatUsers(){
        ArrayList<User> groupUsers = new ArrayList<>();
        int convID = GuiHandler.getInstance().getGui().getSelectedConversationID();
        //String convName = GuiHandler.getInstance().getGui().getSelectedConversationName();
        groupUsers = GuiHandler.getInstance().usersFromGroup(convID, GuiHandler.getInstance().getUser().getId());
        
        System.out.println("current users in group chat size: " + groupUsers.size());
        String[] temp = new String[groupUsers.size()+1];
        int pos=0;
        temp[pos++]= GuiHandler.getInstance().getUser().getUsername() + " - " + GuiHandler.getInstance().getUser().getEmail();
        for(User u : groupUsers){
            temp[pos++] = u.getUsername() + " - " + u.getEmail();
        }
        return temp;
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

        jPanel1 = new javax.swing.JPanel();
        addDeleteUserIcon = new javax.swing.JLabel();
        addDeleteUserLabel = new javax.swing.JLabel();
        addDeleteUserPanel = new javax.swing.JPanel();
        oldPasswordLabel = new javax.swing.JLabel();
        cancelButton = new javax.swing.JButton();
        performAddUserButton = new javax.swing.JButton();
        acceptButton = new javax.swing.JButton();
        selectUserToAdd = new javax.swing.JComboBox();
        jPanel2 = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        usersInChatList = new javax.swing.JList();

        setResizable(false);

        jPanel1.setBackground(new java.awt.Color(247, 247, 247));

        addDeleteUserIcon.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/usertype.png"))); // NOI18N

        addDeleteUserLabel.setFont(new java.awt.Font("Tahoma", 0, 18)); // NOI18N
        addDeleteUserLabel.setText("Add User to Group");

        addDeleteUserPanel.setBackground(new java.awt.Color(237, 237, 255));
        addDeleteUserPanel.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        oldPasswordLabel.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/addUser.png"))); // NOI18N
        oldPasswordLabel.setText("add user");

        cancelButton.setText("Cancel");
        cancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                cancelButtonActionPerformed(evt);
            }
        });

        performAddUserButton.setText("Perform");
        performAddUserButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                performAddUserButtonActionPerformed(evt);
            }
        });

        acceptButton.setText("Okay");
        acceptButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                acceptButtonActionPerformed(evt);
            }
        });

        jPanel2.setBackground(new java.awt.Color(237, 237, 255));
        jPanel2.setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Current Users in Group", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP));

        usersInChatList.setFocusable(false);
        usersInChatList.setPreferredSize(new java.awt.Dimension(260, 100));
        usersInChatList.setVisibleRowCount(5);
        jScrollPane2.setViewportView(usersInChatList);

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );

        javax.swing.GroupLayout addDeleteUserPanelLayout = new javax.swing.GroupLayout(addDeleteUserPanel);
        addDeleteUserPanel.setLayout(addDeleteUserPanelLayout);
        addDeleteUserPanelLayout.setHorizontalGroup(
            addDeleteUserPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(addDeleteUserPanelLayout.createSequentialGroup()
                .addGroup(addDeleteUserPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(addDeleteUserPanelLayout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(oldPasswordLabel)
                        .addGap(11, 11, 11)
                        .addComponent(selectUserToAdd, javax.swing.GroupLayout.PREFERRED_SIZE, 188, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(performAddUserButton))
                    .addGroup(addDeleteUserPanelLayout.createSequentialGroup()
                        .addGap(108, 108, 108)
                        .addComponent(acceptButton)
                        .addGap(31, 31, 31)
                        .addComponent(cancelButton))
                    .addGroup(addDeleteUserPanelLayout.createSequentialGroup()
                        .addGap(46, 46, 46)
                        .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        addDeleteUserPanelLayout.setVerticalGroup(
            addDeleteUserPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(addDeleteUserPanelLayout.createSequentialGroup()
                .addGap(30, 30, 30)
                .addGroup(addDeleteUserPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(oldPasswordLabel)
                    .addComponent(performAddUserButton)
                    .addComponent(selectUserToAdd, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 8, Short.MAX_VALUE)
                .addGroup(addDeleteUserPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(acceptButton)
                    .addComponent(cancelButton))
                .addContainerGap())
        );

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGap(49, 49, 49)
                .addComponent(addDeleteUserIcon)
                .addGap(51, 51, 51)
                .addComponent(addDeleteUserLabel)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(addDeleteUserPanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(addDeleteUserIcon)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                        .addComponent(addDeleteUserLabel)
                        .addGap(37, 37, 37)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(addDeleteUserPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(129, 129, 129))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(0, 0, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, 388, Short.MAX_VALUE)
        );

        pack();
        setLocationRelativeTo(null);
    }// </editor-fold>//GEN-END:initComponents
    
    /**
     * When the user presess this button, the action is performed (update 
     * the group chat).
     * 
     * @param evt - event.
     */
    private void acceptButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_acceptButtonActionPerformed
        // TODO add your handling code here:
        this.setVisible(false);
    }//GEN-LAST:event_acceptButtonActionPerformed
    
    /**
     * When the user presses this button, the action (add user to the group chat) is 
     * performed.
     * 
     * @param evt - event.
     */
    private void performAddUserButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_performAddUserButtonActionPerformed
        //showMessageDialog(null,selectUserToAdd.getSelectedItem().toString());
        System.out.println("PERFORMED adding user to group");
        String selectedUserName = selectUserToAdd.getSelectedItem().toString();
        for(User u : globalUsers){
            if (selectedUserName.equals(u.getUsername() + " - " +u.getEmail())){
                System.out.println("found it man! It is " + u.getUsername());
                GuiHandler.getInstance().insertUserToGroup(GuiHandler.getInstance().getGui().getSelectedConversationID(), u.getId());
                System.out.println("inserted to database for convID: " + GuiHandler.getInstance().getGui().getSelectedConversationID());
                break;
            }
        }
        this.updateCurrentGroupChatUsers();
    }//GEN-LAST:event_performAddUserButtonActionPerformed

    /**
     * When the user presses this button, the window is closed.
     * 
     * @param evt - event.
     */
    private void cancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_cancelButtonActionPerformed
        this.setVisible(false);
    }//GEN-LAST:event_cancelButtonActionPerformed

    /**
     * @param args the command line arguments
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
            java.util.logging.Logger.getLogger(AddUserToGroupChat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(AddUserToGroupChat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(AddUserToGroupChat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(AddUserToGroupChat.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new AddUserToGroupChat().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton acceptButton;
    private javax.swing.JLabel addDeleteUserIcon;
    private javax.swing.JLabel addDeleteUserLabel;
    private javax.swing.JPanel addDeleteUserPanel;
    private javax.swing.JButton cancelButton;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JLabel oldPasswordLabel;
    private javax.swing.JButton performAddUserButton;
    private javax.swing.JComboBox selectUserToAdd;
    private javax.swing.JList usersInChatList;
    // End of variables declaration//GEN-END:variables
}
