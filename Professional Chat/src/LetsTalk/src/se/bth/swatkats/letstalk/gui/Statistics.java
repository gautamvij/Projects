package se.bth.swatkats.letstalk.gui;

import java.awt.Toolkit;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.Objects;
import java.util.concurrent.TimeUnit;
import javax.swing.JOptionPane;
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
 * This class provides the window which shows the user statistics and 
 * graphs in relation with his/her conversations.
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada.
 */
public class Statistics extends javax.swing.JFrame {
    private ArrayList<TopTextChats> localTopTextOtOChats;
    private ArrayList<TopTextChats> localTopTextGroupChats;
    private ArrayList<TopFileChats> localTopFileOtOChats; 
    private ArrayList<TopFileChats> localTopFileGroupChats;
    private ArrayList<TopChat> top10oTo;
    private ArrayList<TopChat> top10group;
    private ArrayList<TopChat> top10;
    
    private ArrayList<UserActivity> activity;

    /**
     * Creates new form Statistics
     */
    public Statistics() {
        initComponents();
        myInitComponents();
    }
    
    /**
     * Provides modifications written by us.
     */
    private void myInitComponents(){
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));
        fetchStatisticsResultsFromDatabase(); 
        setTable(top10); //provide the table to be displayed
        setUserActivity();
    }
    
    private void setUserActivity(){
        activity = GuiHandler.getInstance().fetchUserActivity(GuiHandler.getInstance().getUser().getId());
        userActivityTable.setModel(new javax.swing.table.DefaultTableModel(putActivityPerDay(activity),putUserActivityColumns()));
        this.userActivityTable.getColumnModel().getColumn(0).setPreferredWidth(100);
        this.userActivityTable.getColumnModel().getColumn(1).setPreferredWidth(30);
        
        userActivityTable.setRowSelectionAllowed(true);
        ListSelectionModel rowSelectionModel = userActivityTable.getSelectionModel();
        rowSelectionModel.addListSelectionListener(new ListSelectionListener() {

            @Override
            public void valueChanged(ListSelectionEvent lse) {
                int selectedRow = userActivityTable.getSelectedRow();
                String selectedData = (String) userActivityTable.getValueAt(selectedRow, 0); //get the conversation name
                printDayActivity(selectedData);
            }
        });
        
    }
    
    /**
     * Computes the time difference between two dates.
     * 
     * @param date1
     * @param date2
     * @param timeUnit
     * @return the time difference between dates
     */
    public static long getDateDiff(Date date1, Date date2, TimeUnit timeUnit) {
        long diffInMillies = date2.getTime() - date1.getTime();
        return timeUnit.convert(diffInMillies, TimeUnit.MILLISECONDS);
    }
    
    private long howManyMinutesInDay(String day){
        long hours=0;
        SimpleDateFormat dt = new SimpleDateFormat("EEE, MMM d, ''yy");
        for(UserActivity a : activity){
            if(dt.format(a.getCheckIn()).equals(day)){
                hours += getDateDiff(a.getCheckIn(), a.getCheckOut(), TimeUnit.MINUTES);
            }
        }
        return hours;
    }
    
    /**
     * Calculates how many times per day the user was active
     * @param act
     * @return 
     */
    private Object[][] putActivityPerDay(ArrayList<UserActivity> act){
        Object[][] temp = new Object[10][3];
        int i=0;
        
        SimpleDateFormat dt = new SimpleDateFormat("EEE, MMM d, ''yy");
        String previous = dt.format(act.get(0).getCheckIn()); //keep the previous date
        temp[i][0] = dt.format(act.get(0).getCheckIn());
        temp[i][1] =0;
        
        for(UserActivity a: act){
            if(dt.format(a.getCheckIn()).equals(previous)){
                temp[i][1] = (int) temp[i][1] + 1;
            } else {
                previous = dt.format(a.getCheckIn());
                i++;
                temp[i][1] = 1;
                temp[i][0] = dt.format(a.getCheckIn());
            }            
        }
                
        return temp;
    }
    
    private String[] putUserActivityColumns(){
        String[] temp = { "Date", "Sessions"};
        return temp;
    }
    
    private void fetchStatisticsResultsFromDatabase(){
        localTopTextOtOChats = GuiHandler.getInstance().fetchTopTextChatsForUserOto(GuiHandler.getInstance().getUser().getId());
        localTopTextGroupChats = GuiHandler.getInstance().fetchTopTextChatsForUserGroup(GuiHandler.getInstance().getUser().getId());
        localTopFileOtOChats = GuiHandler.getInstance().fetchTopFileChatsForUserOto(GuiHandler.getInstance().getUser().getId());
        localTopFileGroupChats = GuiHandler.getInstance().fetchTopFileChatsForUserGroup(GuiHandler.getInstance().getUser().getId());
                
        top10oTo = new ArrayList<>(); //stores top10 one-to-one conversations for user
        top10oTo.addAll(localTopTextOtOChats); 
        
        //adds the file count to the appropriate converstion message count
        for(TopFileChats c : localTopFileOtOChats){
            boolean found =false;
            for(TopChat t : top10oTo){
                if(Objects.equals(c.getConversationId(), t.getConversationId())){
                    ((TopTextChats) t).increaseTextCount(c.getFileCount());
                    found = true;
                    break;
                }
            }
            if(!found){
                top10oTo.add(c);
            }
        }       
        
        top10group = new ArrayList<>(); //stores top10 group conversations of user
        top10group.addAll(localTopTextGroupChats); 
        
        //adds the file count to the appropriate converstion message count
        for(TopFileChats c : localTopFileGroupChats){
            boolean found =false;
            for(TopChat t : top10group){
                if(Objects.equals(c.getConversationId(), t.getConversationId())){
                    ((TopTextChats) t).increaseTextCount(c.getFileCount());
                    found = true;
                    break;
                }
            }
            if(!found){
                top10group.add(c);
            }
        }      
                
        top10 = new ArrayList<>(); //stores the final combined top10 of conversations

        //firstly add the elements of two different top10 conversation types
        top10.addAll(top10oTo); 
        top10.addAll(top10group); 
                
        System.out.println("sorting..."); //sort based on message count
        Collections.sort(top10, new Comparator<TopChat>(){
            @Override
            public int compare(TopChat c1, TopChat c2) {
                Integer count1= getMessageCount(c1);
                Integer count2= getMessageCount(c2);
                return count2.compareTo(count1);
            }
        });
    }
    
    private void setTable(ArrayList<TopChat> top10){
        top10table.setModel(new javax.swing.table.DefaultTableModel(putElements(top10),putColumns()));
        
        this.top10table.getColumnModel().getColumn(0).setPreferredWidth(15);
        this.top10table.getColumnModel().getColumn(1).setPreferredWidth(130);
        this.top10table.getColumnModel().getColumn(2).setPreferredWidth(20);
        top10table.setRowSelectionAllowed(true);
        ListSelectionModel rowSelectionModel = top10table.getSelectionModel();
        rowSelectionModel.addListSelectionListener(new ListSelectionListener() {

            @Override
            public void valueChanged(ListSelectionEvent lse) {
                int selectedRow = top10table.getSelectedRow();
                String selectedData = (String) top10table.getValueAt(selectedRow, 1); //get the conversation name
                printInfoMessage(selectedData);
            }
        });
    }
    
    private void printDayActivity(String day){
        long minutes = howManyMinutesInDay(day);
        int hours = (int) minutes / 60; //since both are ints, you get an int
        int mins =  (int) minutes % 60;
        System.out.printf("%d:%02d", hours, minutes);
        showMessageDialog(null, "During " + day + " you have been online for a total of " + minutes + " minutes\n" 
                            + "or else " + hours + "." + mins + " hours");
    }
    
    private void printInfoMessage(String convName){
        boolean flag=false;   
        
        for(TopChat t : top10group){ //check if group conversation
                if (t.getGroupName().equals(convName)){
                    JOptionPane.showMessageDialog(null, "This group conversation with "
                            + t.getGroupName() + " cosists of:\n" 
                            + getTextCountForGroup(convName) + " text messages\n " 
                            + getFileCountForGroup(convName) + " file messages" );
                    flag = true;
                    break;
                }
            }
        
        if(!flag){
            int id=-1;
            for(User u : GuiHandler.getInstance().searchLocalUsers(GuiHandler.getInstance().getUser().getId(), "")){
                if(u.getUsername().equals(convName)){
                    id = u.getId();
                    break;
                }
            }
            
            for(TopChat t : top10oTo){ //one to one conversation
                if (id == t.getUserOne()){
                    JOptionPane.showMessageDialog(null, "This one-to-one conversation with "
                            + convName + " cosists of:\n" 
                            + getTextCountForOtO(id) + " text messages\n " 
                            + getFileCountForOtO(id) + " file messages" );
                    break;
                }
            }
        }
    }
    
    private int getTextCountForOtO(int userID){
        
        for(TopTextChats t : localTopTextOtOChats){
            if(t.getUserOne() == userID){
                return t.getTextCount();
            }
        }
        return 0;
    }
    
    private int getTextCountForGroup(String convName){
        
        for(TopTextChats t : localTopTextGroupChats){
            if(t.getGroupName().equals(convName)){
                return t.getTextCount();
            }
        }
        return 0;
    }
    
    private int getFileCountForOtO(int userID){
        for(TopFileChats t : localTopFileOtOChats){
            if(t.getUserOne() == userID){
                return t.getFileCount();
            }
        }
        return 0;
    }
    
    private int getFileCountForGroup(String convName){
        for(TopFileChats t : localTopFileGroupChats){
            if(t.getGroupName().equals(convName)){
                return t.getFileCount();
            }
        }
        return 0;
    }
    
    private Object[][] putElements(ArrayList<TopChat> top10){
        Object[][] temp = new Object[10][3];
        int count =0;
        int i=1;
        
        for(TopChat c: top10){
            
            temp[count][0] = i;
            
            if(c.getUserOne() == -10) //group chat
                temp[count][1] = c.getGroupName();
            else{ //one-to-one chat
                for(User u : GuiHandler.getInstance().searchLocalUsers(GuiHandler.getInstance().getUser().getId(), "")){
                    if(u.getId() == c.getUserOne()){
                        temp[count][1] = u.getUsername();
                        break;
                    }
                }
            }
            temp[count][2] = getMessageCount(c);
            count++; i++;
            
            if(count == 10){
                return temp;
            }
        }
        return temp;
    }
    
    private String[] putColumns(){
        String[] temp = { "No.", "Conversation Name", "Count"};
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
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel2 = new javax.swing.JPanel();
        jPanel1 = new javax.swing.JPanel();
        oldPasswordLabel = new javax.swing.JLabel();
        newPasswordLabel = new javax.swing.JLabel();
        cancelButton = new javax.swing.JButton();
        jLabel3 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        top10table = new javax.swing.JTable();
        jScrollPane3 = new javax.swing.JScrollPane();
        userActivityTable = new javax.swing.JTable();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jLabel1 = new javax.swing.JLabel();

        setResizable(false);

        jPanel2.setBackground(new java.awt.Color(247, 247, 247));

        jPanel1.setBackground(new java.awt.Color(237, 237, 255));
        jPanel1.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        oldPasswordLabel.setFont(new java.awt.Font("Tahoma", 1, 13)); // NOI18N
        oldPasswordLabel.setText("Top10 users");

        newPasswordLabel.setFont(new java.awt.Font("Tahoma", 1, 13)); // NOI18N
        newPasswordLabel.setText("User Activity");

        cancelButton.setText("Close");
        cancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                cancelButtonActionPerformed(evt);
            }
        });

        jLabel3.setFont(new java.awt.Font("Tahoma", 2, 13)); // NOI18N
        jLabel3.setText("Click on the conversation to see more info");

        top10table.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null},
                {null, null, null}
            },
            new String [] {
                "null", "null", "null"
            }
        ));
        jScrollPane2.setViewportView(top10table);
        if (top10table.getColumnModel().getColumnCount() > 0) {
            top10table.getColumnModel().getColumn(2).setHeaderValue("null");
        }

        userActivityTable.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null},
                {null, null},
                {null, null},
                {null, null},
                {null, null},
                {null, null},
                {null, null}
            },
            new String [] {
                "null", "null"
            }
        ));
        jScrollPane3.setViewportView(userActivityTable);

        jLabel4.setFont(new java.awt.Font("Tahoma", 2, 13)); // NOI18N
        jLabel4.setText("Click on the day to see more info on it");

        jLabel5.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/top-10.png"))); // NOI18N

        jLabel6.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/time.png"))); // NOI18N

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(jLabel6)
                                    .addComponent(newPasswordLabel)))
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(jPanel1Layout.createSequentialGroup()
                                        .addGap(23, 23, 23)
                                        .addComponent(oldPasswordLabel))
                                    .addGroup(jPanel1Layout.createSequentialGroup()
                                        .addContainerGap()
                                        .addComponent(jLabel5)))
                                .addGap(6, 6, 6)))
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGap(18, 18, 18)
                                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(jScrollPane3, javax.swing.GroupLayout.PREFERRED_SIZE, 269, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 269, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGap(28, 28, 28)
                                .addComponent(jLabel3, javax.swing.GroupLayout.PREFERRED_SIZE, 249, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addGap(39, 39, 39)
                                .addComponent(jLabel4, javax.swing.GroupLayout.PREFERRED_SIZE, 231, javax.swing.GroupLayout.PREFERRED_SIZE))))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(176, 176, 176)
                        .addComponent(cancelButton)))
                .addContainerGap(47, Short.MAX_VALUE))
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGap(29, 29, 29)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(oldPasswordLabel)
                    .addComponent(jLabel3))
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(9, 9, 9)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 189, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(47, 47, 47)
                        .addComponent(jLabel5)))
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(26, 26, 26)
                        .addComponent(newPasswordLabel)
                        .addGap(13, 13, 13))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jLabel4)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)))
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(37, 37, 37)
                        .addComponent(jLabel6))
                    .addComponent(jScrollPane3, javax.swing.GroupLayout.PREFERRED_SIZE, 141, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 29, Short.MAX_VALUE)
                .addComponent(cancelButton)
                .addContainerGap())
        );

        jLabel2.setFont(new java.awt.Font("Tahoma", 0, 18)); // NOI18N
        jLabel2.setText("Statistics");

        jLabel1.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/statistics.png"))); // NOI18N

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(112, 112, 112)
                        .addComponent(jLabel1)
                        .addGap(36, 36, 36)
                        .addComponent(jLabel2))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addComponent(jLabel1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                        .addComponent(jLabel2)
                        .addGap(26, 26, 26)))
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
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
     * When the user presses this button, the window is closed.
     * 
     * @param evt - event.
     */
    private void cancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_cancelButtonActionPerformed
        this.setVisible(false);
    }//GEN-LAST:event_cancelButtonActionPerformed

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
            java.util.logging.Logger.getLogger(Statistics.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Statistics.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Statistics.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Statistics.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Statistics().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton cancelButton;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JLabel newPasswordLabel;
    private javax.swing.JLabel oldPasswordLabel;
    private javax.swing.JTable top10table;
    private javax.swing.JTable userActivityTable;
    // End of variables declaration//GEN-END:variables
}
