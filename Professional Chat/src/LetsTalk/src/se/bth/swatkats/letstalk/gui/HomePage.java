package se.bth.swatkats.letstalk.gui;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.sql.Timestamp;
import java.util.ArrayList;
import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import static javax.swing.JOptionPane.showMessageDialog;
import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.connection.packet.message.FileMessage;
import se.bth.swatkats.letstalk.connection.packet.message.Message;
import se.bth.swatkats.letstalk.connection.packet.message.TextMessage;
import se.bth.swatkats.letstalk.statistics.TopFileChats;
import se.bth.swatkats.letstalk.statistics.TopTextChats;
import se.bth.swatkats.letstalk.user.User;

/**
 * This class provides the window which has all the functionalities that can be used by the user.
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada.
 */
public class HomePage extends javax.swing.JFrame {
    
    private User user; //current user
    
    private ArrayList<User> contacts; //users in local address book
    private ArrayList<Conversation> conversations; //conv_id, name, timestamp_of_last_message
    private String selectedConversationName;
    
    UploadFile fileUpWin;
    DownloadFile fileDownWin;

    /**
     * Creates new form HomePage.
     */
    public HomePage() {       
        initComponents(); 
        myInitComponents();
    }
    
    /**
     * Provides modifications written by us.
     */
    private void myInitComponents(){
        //set the favicon --> logo of app at top-left of window
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));
        
        // link to the gui handler
        user = GuiHandler.getInstance().getUser();
        GuiHandler.getInstance().setGui(this);
        
        setTitle("LetsTalk - " + user.getUsername());
        
        //initialize variables
        contacts = new ArrayList<>();
        conversations = new ArrayList<>();
        
        setInactivityFunctions();
        setCloseWindowFunction();
        
        updateContacts();
        updateConversations();
        
        //Hides the Admin Features menu if the user is not an admin
        if(user.getAdmin_flag()!=1){
            adminFeaturesMenu.setVisible(false);
        }
        
        addUserToConversationBut.setEnabled(false);
        
        //Current user of the application
        System.out.println("========AUTHENTICATED USER=========");
        System.out.println("username: "+ user.getUsername());
        System.out.println("id: "+user.getId());
        System.out.println("email: "+user.getEmail());
        System.out.println("status: "+user.getStatus());
        System.out.println("admin flag: "+user.getAdmin_flag());
        System.out.println("====================================");
    }
    
    /**
     * This methods detects user inactivity in the program.
     */
    private void setInactivityFunctions(){
        
        
        Action idle = new AbstractAction()
        {
            @Override
            public void actionPerformed(ActionEvent e)
            {
                GuiHandler.getInstance().setUserStatusIdle(user.getId());
                user.setStatus(2);
                GuiHandler.getInstance().getUser().setStatus(2);
                Object[] possibleValues = { "Available", "Busy"};
                Object selectedValue = JOptionPane.showInputDialog(null,
                "Your status has been set to idle because of long time of inactivity.\n Choose your new status.\n", "Choose status",
                JOptionPane.INFORMATION_MESSAGE, null,
                possibleValues, possibleValues[0]);
                try{
                    if(selectedValue.equals("Available")){
                        user.setStatus(0);
                        GuiHandler.getInstance().getUser().setStatus(0);
                        GuiHandler.getInstance().setUserStatusAvailable(user.getId());
                    } else {
                        user.setStatus(1);
                        GuiHandler.getInstance().getUser().setStatus(1);
                        GuiHandler.getInstance().setUserStatusBusy(user.getId());
                    }
                } catch (java.lang.NullPointerException ex){
                    //cancel pressed - set to Busy
                    user.setStatus(1);
                    GuiHandler.getInstance().getUser().setStatus(1);
                    GuiHandler.getInstance().setUserStatusAvailable(user.getId());
                }
            }
        };
        
        InactivityListener listener = new InactivityListener(this, idle, 1); //if inactive for 10 minutes --> set status to Idle
        listener.start();
    }
    
    /**
     * This method sets what happens upon closure of main homepage window.
     */
    private void setCloseWindowFunction(){
        this.addWindowListener(new WindowAdapter(){
            @Override
            public void windowClosing(WindowEvent event){
                exitProcedure();
            }
        });
    }
    
    /**
     * This method notify to the conversation that it has received a new message.
     * 
     * @param convID - Conversation ID which has received a message.
     */
    public void notifyConversationReceivedMessage(int convID){
        //fetching all conversations for our current user from the database
        conversations = GuiHandler.getInstance().fetchConversationsForUser(user.getId());
        
        String temp = "";
        for(Conversation conv: conversations){
            if(conv.getId() == convID)
                temp = conv.getName();
        }
        
        final String name = temp;
        
        //adds conversations to the conversation list of current user.
        conversationsList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = putNamesWithNotifier(name);
            @Override
            public int getSize() { return strings.length; }
            @Override
            public Object getElementAt(int i) { return strings[i]; }
       });
    }
    
     /**
     * Inserts into the left list, the conversations.
     * 
     * @return the conversations strings (conversations names).
     */
    private String[] putNamesWithNotifier(String name) {
        
        String[] temp = new String[conversations.size()];
        int pos=0;
        for(Conversation conv: conversations){ // for each of user's conversations
            
            boolean group=true;
            
            for(User u : contacts){ //find the status of the other user and print it next to his name
                if(conv.getName().equals(u.getUsername())){
                    group = false;
                    switch(u.getStatus()){
                        case 0: 
                            temp[pos] = conv.getName() + " (Available)";
                            break;
                        case 1: 
                            temp[pos] = conv.getName() + " (Busy)";
                            break;
                        case 2: 
                            temp[pos] = conv.getName() + " (Idle)";
                            break;
                        case 3: 
                            temp[pos] = conv.getName() + " (Offline)";
                            break;
                        default:
                            temp[pos] = conv.getName() + " (Not Defined)";
                    }
                    break;
                }
            }
            
            if (group){
                temp[pos] = conv.getName() + " (Group Chat)";
            }
            
            if(conv.getName().equals(name)){
                temp[pos] += " [N]";
            }
            
            pos++;
        }
        return temp;
    }
    
    /**
     * This method updates the conversation histories.
     */
    public void updateConversationHistories() {
        updateContacts();
        try {
            selectedConversationName = this.conversationsList.getSelectedValue().toString();        
        } catch (java.lang.NullPointerException ex){
            System.out.println("Exception: No conversation is selected!");
        }
        updateConversations();
        for(Conversation conv : conversations){
            loadMessageHistory(GuiHandler.getInstance().fetchTextConversationHistory(conv.getId(), user.getId()), GuiHandler.getInstance().fetchFileConversationHistory(conv.getId(), user.getId())); 
        }
        conversationsList.setSelectedValue(selectedConversationName, true);
    }
    
    /**
     * This method updates the conversations.
     */
    public void updateConversations(){
        
        //fetching all conversations for our current user from the database
        conversations = GuiHandler.getInstance().fetchConversationsForUser(user.getId());
        
        boolean flag = true;
        try{
            selectedConversationName = conversationsList.getSelectedValue().toString();
        } catch(java.lang.NullPointerException ex){
            flag = false;            
        }
        
        //adds conversations to the conversation list of current user.
        conversationsList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = putNames();
            @Override
            public int getSize() { return strings.length; }
            @Override
            public Object getElementAt(int i) { return strings[i]; }
       });
        
        if(flag)
            conversationsList.setSelectedValue(selectedConversationName, true);
    }
    
    /**
     * This method updates the contacts.
     */
    public void updateContacts(){
        //fetching all contacts (people in local address book) for our current user from database
        contacts = GuiHandler.getInstance().searchLocalUsers(user.getId(), "");
//        System.out.println("just got them:==============================");
//        for(User u : contacts){
//            System.out.println(u.getUsername() + " " + u.getId() + " " + u.getEmail());
//        }
        
        //insert the contacts in local address book of current user.		
        localAddressBookList.setModel(new javax.swing.AbstractListModel() {		
            String[] strings = insertContacts();		
            @Override		
            public int getSize() { return strings.length; }		
            @Override		
            public Object getElementAt(int i) { return strings[i]; }		
        });          
    }

    /**
     * Inserts into the local address book the names of user's contacts.
     * 
     * @return temp - the local address book strings (usernames).
     */
    private String[] insertContacts() {
//        System.out.println("===> insert contacts ====> " + contacts.size());
        String[] temp = new String[contacts.size()];
        int pos=0;
        for(User contact: contacts){
            temp[pos++] = contact.getUsername();
        }
        return temp;
    }
    
    /**
     * Inserts into the left list, the conversations.
     * 
     * @return temp - the conversations strings (conversations names).
     */
    private String[] putNames() {
//        System.out.println("====> insert conversations ====> " + conversations.size());
        String[] temp = new String[conversations.size()];
        int pos=0;
        for(Conversation conv: conversations){ // for each of user's conversations
            
            boolean group=true;
//            System.out.println(conv.getName() + " - " + conv.getId());
            
            for(User u : contacts){ //find the status of the other user and print it next to his name
                if(conv.getName().equals(u.getUsername())){
//                    System.out.println(conv.getName() + " " + u.getUsername() + " " + u.getStatus());
                    group = false;
                    switch(u.getStatus()){
                        case 0: 
                            temp[pos++] = conv.getName() + " (Available)";
                            break;
                        case 1: 
                            temp[pos++] = conv.getName() + " (Busy)";
                            break;
                        case 2: 
                            temp[pos++] = conv.getName() + " (Idle)";
                            break;
                        case 3: 
                            temp[pos++] = conv.getName() + " (Offline)";
                            break;
                        default:
                            temp[pos++] = conv.getName() + " (Not Defined)";
                    }
                    break;
                }
            }
            
            if (group){
                temp[pos++] = conv.getName() + " (Group Chat)";
            }
        }
        return temp;
    }
    
    /**
     * Called when user exits our application.
     * It aborts the connection and then close the window.
     */
    private void exitProcedure(){
        setVisible(false); //you can't see me!
        dispose(); //Destroy the JFrame object
        GuiHandler.getInstance().closeConnection(); //closes connection with server.
        System.exit(1); //terminates the program.
    }
    
    /**
     * Manages the received messages. If it is a normal message is showed
     * in the screen, if not... [WE WILL SEE]
     * 
     * @param m - received message. 
     */
    public void receivedMessage(Message m){
//        System.out.println("user " + user.getUsername() + " have received a message by "+ m.getUsername() + " in conversation " + m.getConversationid());
        //updateContacts();
        //updateConversations();
        if(m.getConversationid() == this.getSelectedConversationID())
            loadMessageHistory(GuiHandler.getInstance().fetchTextConversationHistory(m.getConversationid(), user.getId()), GuiHandler.getInstance().fetchFileConversationHistory(m.getConversationid(), user.getId())); 
        else{
            //notify that this conversation has a new message!!!
            notifyConversationReceivedMessage(m.getConversationid());
        }   
    }
    
    /**
     * This method notifies that a new file message is been received.
     * 
     * @param in - File message received.
     */
    public void receiveFileMessage(FileMessage in) {
//        System.out.println("user " + user.getUsername() + " have received a file message by "+ in.getUsername() + " in conversation " + in.getConversationid());
        //updateContacts();
        //updateConversations();
        
        if(in.getConversationid() == this.getSelectedConversationID())
            loadMessageHistory(GuiHandler.getInstance().fetchTextConversationHistory(in.getConversationid(), user.getId()), GuiHandler.getInstance().fetchFileConversationHistory(in.getConversationid(), user.getId())); 
        else{
            //notify that this conversation has a new message!!!
            notifyConversationReceivedMessage(in.getConversationid());
        }     
    }   
    
   /**
     * Every time user selects another conversation, the new message history
     * is loaded.
     * 
     * @param e - event.
     * */
    private void conversationsListValueChanged(javax.swing.event.ListSelectionEvent e){
        if(!conversationsList.getValueIsAdjusting()){
//            System.out.println("Conversations list value changed.");
            String value = "";

            try{
                value = conversationsList.getSelectedValue().toString();
            } catch(java.lang.NullPointerException ex){
                System.out.println("Exception!! No conversation was selected");
                return;
            }

            if(value.endsWith("[N]")){
                int where = conversationsList.getSelectedIndex();
                updateConversations();
                conversationsList.setSelectedIndex(where);
            }

            int convID = getSelectedConversationID();
            ArrayList<User> globalUsers = GuiHandler.getInstance().searchGlobalUsers("", user.getId());
//            System.out.println("Search the conversations names");
            for(Conversation conv : conversations){
                if(conv.getId() == convID){
//                    System.out.println("found! conName: " + conv.getName() + " convID: " + conv.getId());
                    boolean flag = true;
                    for(User u : globalUsers){
                        if (u.getUsername().equals(conv.getName()))
                            flag = false;
                    }
                    addUserToConversationBut.setEnabled(flag);
                }
            }
            ArrayList<TextMessage> textMessages = GuiHandler.getInstance().fetchTextConversationHistory(convID, user.getId());
            ArrayList<FileMessage> fileMessages = GuiHandler.getInstance().fetchFileConversationHistory(convID, user.getId());
            loadMessageHistory(textMessages, fileMessages);
        }
    }
    
    /**
     * This method loads the messages & files history.
     * 
     * @param textMessages - All the messages which belong to the conversation.
     * @param fileMessages - All the files which belong to the conversation.
     */
    private void loadMessageHistory(ArrayList<TextMessage> textMessages, ArrayList<FileMessage> fileMessages){
//        System.out.println("... loading history ...");
        messageHistoryTextArea.setText("");
        
//        System.out.println("******* Printing what Text Messages came!! **********");
//        System.out.println("**** number of text messages: "+textMessages.size());
//        System.out.println("**** number of file messages: "+fileMessages.size());
        
        Timestamp previous = new Timestamp(24,5,20,11,5,20,1000);
        String prev = new java.text.SimpleDateFormat("dd").format(previous);
        
        for(TextMessage m : textMessages){
            Timestamp current = ((TextMessage) m).getTimestamp();
            String cur = new java.text.SimpleDateFormat("dd").format(current);
            if(!prev.equals(cur)){
                String date = new java.text.SimpleDateFormat("EEE, MMM d, ''yy").format(current);
                messageHistoryTextArea.append("~~~~~~~~~~~~~~~~~~~~~~   " + date + "   ~~~~~~~~~~~~~~~~~~~~~~" + System.getProperty("line.separator"));
            }
            prev = cur;
            String date = new java.text.SimpleDateFormat("h:mm a").format(current);

            messageHistoryTextArea.append(date + " - " + ((TextMessage) m).getUsername() + ": " + ((TextMessage) m).getText() + System.getProperty("line.separator") );
        }
        
        filesList.setModel(new javax.swing.AbstractListModel() {
            String[] strings = putFiles(fileMessages);
            @Override
            public int getSize() { return strings.length; }
            @Override
            public Object getElementAt(int i) { return strings[i]; }
        });
    }
    
    /**
     * This method returns a list with files' names.
     * 
     * @param files - List of files.
     * @return temp - String[] which contains the files' names.
     */
    public String[] putFiles(ArrayList<FileMessage> files){
//        System.out.println("=== insert files ==== ");
        String[] temp = new String[files.size()];
        int pos=0;
        for(FileMessage m: files){
            temp[pos++] = m.getFileid() + "| " + m.getFilename();
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

        jCheckBoxMenuItem1 = new javax.swing.JCheckBoxMenuItem();
        jMenu1 = new javax.swing.JMenu();
        userStatus = new javax.swing.ButtonGroup();
        sendMessagePanel = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        sendMessageTextPane = new javax.swing.JTextPane();
        attachFile = new javax.swing.JButton();
        sendTextBut = new javax.swing.JButton();
        conversationsPanel = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        conversationsList = new javax.swing.JList();
        logo = new javax.swing.JLabel();
        localAddresBookScrollPane = new javax.swing.JScrollPane();
        localAddressBookList = new javax.swing.JList();
        newConversationButton = new javax.swing.JButton();
        jPanel1 = new javax.swing.JPanel();
        jScrollPane3 = new javax.swing.JScrollPane();
        filesList = new javax.swing.JList();
        jScrollPane4 = new javax.swing.JScrollPane();
        messageHistoryTextArea = new javax.swing.JTextArea();
        addUserToConversationBut = new javax.swing.JButton();
        menuBar = new javax.swing.JMenuBar();
        settingsMenu = new javax.swing.JMenu();
        changePasswordMenu = new javax.swing.JMenuItem();
        statusMenu = new javax.swing.JMenu();
        statusAvailableSubMenu = new javax.swing.JRadioButtonMenuItem();
        statusBusySubMenu = new javax.swing.JRadioButtonMenuItem();
        addressBookMenu = new javax.swing.JMenu();
        addDeleteUserSubMenu = new javax.swing.JMenuItem();
        blockUnblockUserSubMenu = new javax.swing.JMenuItem();
        adminFeaturesMenu = new javax.swing.JMenu();
        adminPanelSubMenu = new javax.swing.JMenuItem();
        statisticsMenu = new javax.swing.JMenu();
        checkStatsSubMenu = new javax.swing.JMenuItem();
        materialRepoMenu = new javax.swing.JMenu();
        filesDatabaseSubMenu = new javax.swing.JMenuItem();
        helpMenu = new javax.swing.JMenu();
        aboutSubMenu = new javax.swing.JMenuItem();

        jCheckBoxMenuItem1.setSelected(true);
        jCheckBoxMenuItem1.setText("jCheckBoxMenuItem1");

        jMenu1.setText("jMenu1");

        setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
        setTitle("Lets Talk");
        setBackground(new java.awt.Color(247, 247, 247));
        setCursor(new java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR));
        setResizable(false);

        sendMessagePanel.setBorder(javax.swing.BorderFactory.createTitledBorder("Send a message"));

        sendMessageTextPane.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                sendMessageTextPaneKeyPressed(evt);
            }
            public void keyReleased(java.awt.event.KeyEvent evt) {
                sendMessageTextPaneKeyReleased(evt);
            }
            public void keyTyped(java.awt.event.KeyEvent evt) {
                sendMessageTextPaneKeyTyped(evt);
            }
        });
        jScrollPane2.setViewportView(sendMessageTextPane);

        attachFile.setText("Attach File");
        attachFile.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                attachFileActionPerformed(evt);
            }
        });

        sendTextBut.setText("Send Text");
        sendTextBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sendTextButActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout sendMessagePanelLayout = new javax.swing.GroupLayout(sendMessagePanel);
        sendMessagePanel.setLayout(sendMessagePanelLayout);
        sendMessagePanelLayout.setHorizontalGroup(
            sendMessagePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, sendMessagePanelLayout.createSequentialGroup()
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 723, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(sendMessagePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(attachFile, javax.swing.GroupLayout.DEFAULT_SIZE, 166, Short.MAX_VALUE)
                    .addComponent(sendTextBut, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addGap(2, 2, 2))
        );
        sendMessagePanelLayout.setVerticalGroup(
            sendMessagePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(sendMessagePanelLayout.createSequentialGroup()
                .addComponent(attachFile, javax.swing.GroupLayout.PREFERRED_SIZE, 72, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(sendTextBut, javax.swing.GroupLayout.PREFERRED_SIZE, 72, javax.swing.GroupLayout.PREFERRED_SIZE))
            .addComponent(jScrollPane2, javax.swing.GroupLayout.Alignment.TRAILING)
        );

        conversationsPanel.setBorder(javax.swing.BorderFactory.createTitledBorder("Conversations"));
        conversationsPanel.setName(""); // NOI18N
        conversationsPanel.setOpaque(false);

        conversationsList.addListSelectionListener(new javax.swing.event.ListSelectionListener() {
            public void valueChanged(javax.swing.event.ListSelectionEvent evt) {
                conversationsListValueChanged(evt);
            }
        });
        jScrollPane1.setViewportView(conversationsList);

        javax.swing.GroupLayout conversationsPanelLayout = new javax.swing.GroupLayout(conversationsPanel);
        conversationsPanel.setLayout(conversationsPanelLayout);
        conversationsPanelLayout.setHorizontalGroup(
            conversationsPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(conversationsPanelLayout.createSequentialGroup()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 224, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(0, 0, Short.MAX_VALUE))
        );
        conversationsPanelLayout.setVerticalGroup(
            conversationsPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 467, javax.swing.GroupLayout.PREFERRED_SIZE)
        );

        logo.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/logoSmall.png"))); // NOI18N
        logo.setPreferredSize(new java.awt.Dimension(500, 256));
        logo.setRequestFocusEnabled(false);

        localAddresBookScrollPane.setBorder(javax.swing.BorderFactory.createTitledBorder("Local Address Book"));
        localAddresBookScrollPane.setToolTipText("");

        localAddresBookScrollPane.setViewportView(localAddressBookList);

        newConversationButton.setText("New conversation");
        newConversationButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                newConversationButtonActionPerformed(evt);
            }
        });

        jPanel1.setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Messages & Files", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP));

        filesList.addListSelectionListener(new javax.swing.event.ListSelectionListener() {
            public void valueChanged(javax.swing.event.ListSelectionEvent evt) {
                filesListValueChanged(evt);
            }
        });
        jScrollPane3.setViewportView(filesList);

        messageHistoryTextArea.setEditable(false);
        messageHistoryTextArea.setColumns(20);
        messageHistoryTextArea.setRows(5);
        jScrollPane4.setViewportView(messageHistoryTextArea);

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addComponent(jScrollPane4)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane3, javax.swing.GroupLayout.PREFERRED_SIZE, 139, javax.swing.GroupLayout.PREFERRED_SIZE))
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane4)
            .addComponent(jScrollPane3, javax.swing.GroupLayout.DEFAULT_SIZE, 388, Short.MAX_VALUE)
        );

        addUserToConversationBut.setFont(new java.awt.Font("Tahoma", 0, 14)); // NOI18N
        addUserToConversationBut.setText("...");
        addUserToConversationBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addUserToConversationButActionPerformed(evt);
            }
        });

        menuBar.setBorder(javax.swing.BorderFactory.createCompoundBorder());
        menuBar.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        settingsMenu.setText("Settings");
        settingsMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        changePasswordMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        changePasswordMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/changePass.png"))); // NOI18N
        changePasswordMenu.setText("Change Password");
        changePasswordMenu.setAutoscrolls(true);
        changePasswordMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                changePasswordMenuActionPerformed(evt);
            }
        });
        settingsMenu.add(changePasswordMenu);

        menuBar.add(settingsMenu);

        statusMenu.setBorder(javax.swing.BorderFactory.createCompoundBorder());
        statusMenu.setText("Status");
        statusMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        statusAvailableSubMenu.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_A, java.awt.event.InputEvent.CTRL_MASK));
        userStatus.add(statusAvailableSubMenu);
        statusAvailableSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        statusAvailableSubMenu.setSelected(true);
        statusAvailableSubMenu.setText("Available");
        statusAvailableSubMenu.setCursor(new java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR));
        statusAvailableSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/green.png"))); // NOI18N
        statusAvailableSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                statusAvailableSubMenuActionPerformed(evt);
            }
        });
        statusMenu.add(statusAvailableSubMenu);

        statusBusySubMenu.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_B, java.awt.event.InputEvent.CTRL_MASK));
        userStatus.add(statusBusySubMenu);
        statusBusySubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        statusBusySubMenu.setText("Busy");
        statusBusySubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/red.png"))); // NOI18N
        statusBusySubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                statusBusySubMenuActionPerformed(evt);
            }
        });
        statusMenu.add(statusBusySubMenu);

        menuBar.add(statusMenu);

        addressBookMenu.setText("Address Book");
        addressBookMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        addDeleteUserSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        addDeleteUserSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/manageUser.png"))); // NOI18N
        addDeleteUserSubMenu.setText("Add/Delete User");
        addDeleteUserSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addDeleteUserSubMenuActionPerformed(evt);
            }
        });
        addressBookMenu.add(addDeleteUserSubMenu);

        blockUnblockUserSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        blockUnblockUserSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/blockUnblock.png"))); // NOI18N
        blockUnblockUserSubMenu.setText("Block/Unblock User");
        blockUnblockUserSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                blockUnblockUserSubMenuActionPerformed(evt);
            }
        });
        addressBookMenu.add(blockUnblockUserSubMenu);

        menuBar.add(addressBookMenu);

        adminFeaturesMenu.setText("Admin Features");
        adminFeaturesMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        adminPanelSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        adminPanelSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/user_admin.png"))); // NOI18N
        adminPanelSubMenu.setText("Open admin panel");
        adminPanelSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                adminPanelSubMenuActionPerformed(evt);
            }
        });
        adminFeaturesMenu.add(adminPanelSubMenu);

        menuBar.add(adminFeaturesMenu);

        statisticsMenu.setText("Statistics");
        statisticsMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        checkStatsSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        checkStatsSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/stats.png"))); // NOI18N
        checkStatsSubMenu.setText("Check your stats");
        checkStatsSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkStatsSubMenuActionPerformed(evt);
            }
        });
        statisticsMenu.add(checkStatsSubMenu);

        menuBar.add(statisticsMenu);

        materialRepoMenu.setText("Material Repository");
        materialRepoMenu.setFocusable(false);
        materialRepoMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        filesDatabaseSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        filesDatabaseSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/files.png"))); // NOI18N
        filesDatabaseSubMenu.setText("Open files database");
        filesDatabaseSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                filesDatabaseSubMenuActionPerformed(evt);
            }
        });
        materialRepoMenu.add(filesDatabaseSubMenu);

        menuBar.add(materialRepoMenu);

        helpMenu.setBorder(javax.swing.BorderFactory.createCompoundBorder());
        helpMenu.setText("Help");
        helpMenu.setFont(new java.awt.Font("Segoe UI", 0, 18)); // NOI18N

        aboutSubMenu.setFont(new java.awt.Font("Segoe UI", 0, 16)); // NOI18N
        aboutSubMenu.setIcon(new javax.swing.ImageIcon(getClass().getResource("/se/bth/swatkats/letstalk/gui/img/information.png"))); // NOI18N
        aboutSubMenu.setText("About");
        aboutSubMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                aboutSubMenuActionPerformed(evt);
            }
        });
        helpMenu.add(aboutSubMenu);

        menuBar.add(helpMenu);

        setJMenuBar(menuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(logo, javax.swing.GroupLayout.PREFERRED_SIZE, 241, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(conversationsPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(sendMessagePanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                .addComponent(addUserToConversationBut, javax.swing.GroupLayout.PREFERRED_SIZE, 24, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(newConversationButton, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                            .addComponent(localAddresBookScrollPane, javax.swing.GroupLayout.PREFERRED_SIZE, 173, javax.swing.GroupLayout.PREFERRED_SIZE))))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(logo, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(conversationsPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                                    .addComponent(newConversationButton)
                                    .addComponent(addUserToConversationBut, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(localAddresBookScrollPane, javax.swing.GroupLayout.PREFERRED_SIZE, 383, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(11, 11, 11)
                        .addComponent(sendMessagePanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addGap(31, 31, 31))
        );

        setSize(new java.awt.Dimension(1203, 691));
        setLocationRelativeTo(null);
    }// </editor-fold>//GEN-END:initComponents

    /**
     * When user presses the Attach File button, is opened a new window where
     * the user can choose the file that he wants to send and send it.
     * 
     * @param evt - event.
     */
    private void attachFileActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_attachFileActionPerformed
        
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setCurrentDirectory(new File(System.getProperty("user.home")));
        int result = fileChooser.showOpenDialog(fileChooser);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            int receiverID = getSelectedReceiverID();
            int convID =getSelectedConversationID();
            fileUpWin = new UploadFile();
            fileUpWin.setVisible(true);
            GuiHandler.getInstance().startFileUpload(selectedFile.getAbsolutePath(), convID, receiverID, false); 
            sendMessageTextPane.setText(""); //clears the sendTextArea 
            loadMessageHistory(GuiHandler.getInstance().fetchTextConversationHistory(convID, user.getId()), GuiHandler.getInstance().fetchFileConversationHistory(convID, user.getId())); 
        }
    }//GEN-LAST:event_attachFileActionPerformed

    /**
     * This method uploads the progress bar.
     * 
     * @param value - Percent of the file uploaded.
     */
    public void updateUploadProgress(int value){
         fileUpWin.setProgressValue(value);
         if(value == 100){
             fileUpWin.fileUploaded();
         }
    }
    
    public void updateDownloadProgress(int value){
         fileDownWin.setProgressValue(value);
         if(value == 100){
             fileDownWin.fileDownloaded();
         }
    }
    
    /**
     * When user presses the send button, it sends the text to the user specified 
     * in the conversation and cleans the send text area.
     * 
     * @param evt - event.
     */
    private void sendTextButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendTextButActionPerformed
//        System.out.println("+++++ Send Text +++++");
        
        if(!sendMessageTextPane.getText().isEmpty()){
            int receiverID = getSelectedReceiverID();
            int convID =getSelectedConversationID();

            if(receiverID != -50){

                if (receiverID == -10){ //group chat
                    ArrayList<User> groupUsers = GuiHandler.getInstance().usersFromGroup(convID, user.getId());
//                    System.out.println("group chat has " + groupUsers.size() + " users");
//                    for(User u : groupUsers){
//                        System.out.println(u.getUsername() + " is in the group");
//                        System.out.println("Ready to send text message: "+ sendMessageTextPane.getText());
//                        System.out.println("==> ConvID: " + convID);
//                        System.out.println("==> ReceiverID: "+ u.getId());
//                    }
                    GuiHandler.getInstance().sendMessage(-10, convID,sendMessageTextPane.getText());
                } else { //one-to-one chat
//                    System.out.println("Ready to send text message: "+ sendMessageTextPane.getText());
//                    System.out.println("==> ConvID: " + convID);
//                    System.out.println("==> ReceiverID: "+ receiverID);
                    GuiHandler.getInstance().sendMessage(receiverID, convID,sendMessageTextPane.getText());
                }

                sendMessageTextPane.setText(""); //clears the sendTextArea 
                loadMessageHistory(GuiHandler.getInstance().fetchTextConversationHistory(convID, user.getId()), GuiHandler.getInstance().fetchFileConversationHistory(convID, user.getId())); 

            } else {
                showMessageDialog(null,"Please select a conversation!");
            }
        } else {
            showMessageDialog(null, "Please write a message!");
        }
    }//GEN-LAST:event_sendTextButActionPerformed
   
    /**
     * When user presses this option, his/her status is changed to available.
     * 
     * @param evt - event.
     */
    private void statusAvailableSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_statusAvailableSubMenuActionPerformed
        GuiHandler.getInstance().setUserStatusAvailable(user.getId());
        user.setStatus(0);
    }//GEN-LAST:event_statusAvailableSubMenuActionPerformed
    
    /**
     * When user presses this option, his/her status is changed to busy.
     * 
     * @param evt - event.
     */
    private void statusBusySubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_statusBusySubMenuActionPerformed
        GuiHandler.getInstance().setUserStatusBusy(user.getId());
        user.setStatus(1);
    }//GEN-LAST:event_statusBusySubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for change password.
     * 
     * @param evt - event.
     */
    private void changePasswordMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_changePasswordMenuActionPerformed
        ChangePassword changePass = new ChangePassword();
        changePass.setVisible(true);
    }//GEN-LAST:event_changePasswordMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for add/delete users.
     * 
     * @param evt - event.
     */
    private void addDeleteUserSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addDeleteUserSubMenuActionPerformed
        
        AddDeleteUser addDeleteWin = new AddDeleteUser();
        addDeleteWin.setVisible(true);
        

    }//GEN-LAST:event_addDeleteUserSubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for block/unblock users.
     * 
     * @param evt - event.
     */
    private void blockUnblockUserSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_blockUnblockUserSubMenuActionPerformed
        BlockUnblockUser blockUnblock = new BlockUnblockUser();
        blockUnblock.setVisible(true);
        blockUnblock.addWindowListener(new WindowAdapter(){
            @Override
            public void windowClosing(WindowEvent event){
                updateContacts();
            }
        });
        
    }//GEN-LAST:event_blockUnblockUserSubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for see the file repository.
     * 
     * @param evt - event. 
     */
    private void filesDatabaseSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_filesDatabaseSubMenuActionPerformed
        FilesRepo filesWin = new FilesRepo();
        filesWin.setVisible(true);
    }//GEN-LAST:event_filesDatabaseSubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for see details about the program.
     * 
     * @param evt - event. 
     */
    private void aboutSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_aboutSubMenuActionPerformed
    	// open window for see details about the program
    	About aboutWin = new About();
    	aboutWin.setVisible(true);
    }//GEN-LAST:event_aboutSubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for change admin features.
     * 
     * @param evt - event.
     */
    private void adminPanelSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_adminPanelSubMenuActionPerformed
    	AdminFeatures adminP = new AdminFeatures();
    	adminP.setVisible(true);
        
        adminP.addWindowListener(new WindowAdapter(){
            @Override
            public void windowClosing(WindowEvent event){
                updateContacts();
            }
        });
    }//GEN-LAST:event_adminPanelSubMenuActionPerformed
    
    /**
     * When user presses this option, a new window is displayed for see the resources' statistics.
     * 
     * @param evt - e.
     */
    private void checkStatsSubMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkStatsSubMenuActionPerformed
        Statistics statsWin = new Statistics();
        statsWin.setVisible(true);
    }//GEN-LAST:event_checkStatsSubMenuActionPerformed

    /**
     * When the user presses the file, it starts to download.
     * 
     * @param evt - event.
     */
    private void filesListValueChanged(javax.swing.event.ListSelectionEvent evt) {//GEN-FIRST:event_filesListValueChanged
        if(!filesList.getValueIsAdjusting()){
//            System.out.println("Files list value changed.");
            int fileID = getSelectedFileID();
            String filename = getSelectedFileName();
            
            //choose where to store
            String path;
            JFileChooser chooser = new JFileChooser(); 
            chooser.setCurrentDirectory(new java.io.File("."));
            chooser.setDialogTitle("Downloading file directory");
            chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
            chooser.setAcceptAllFileFilterUsed(false);

            if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) { 
                path = chooser.getSelectedFile().getAbsolutePath();
                path += "\\";
            } else {
                System.out.println("No Selection ");
                path = null;
            }
                 
//            System.out.println("path: " + path);
//            System.out.println("filename: " + filename);
//            System.out.println("fileID: " + fileID);
            GuiHandler.getInstance().startFileDownload(path, filename, fileID, false);
        }
    }//GEN-LAST:event_filesListValueChanged

    /**
     * When the user presses this button, a new window is displayed in order to add
     * new users to the group chat.
     * 
     * @param evt - event. 
     */
    private void addUserToConversationButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addUserToConversationButActionPerformed
        AddUserToGroupChat win = new AddUserToGroupChat();
        win.setVisible(true);
    }//GEN-LAST:event_addUserToConversationButActionPerformed

    private void sendMessageTextPaneKeyReleased(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_sendMessageTextPaneKeyReleased
        if (evt.getKeyCode()==KeyEvent.VK_ENTER)    
            this.sendMessageTextPane.setText("");
    }//GEN-LAST:event_sendMessageTextPaneKeyReleased

    private void sendMessageTextPaneKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_sendMessageTextPaneKeyPressed
        if (evt.getKeyCode()==KeyEvent.VK_ENTER){
            this.sendTextBut.doClick();
            this.sendMessageTextPane.setText("");
        }
    }//GEN-LAST:event_sendMessageTextPaneKeyPressed

    private void sendMessageTextPaneKeyTyped(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_sendMessageTextPaneKeyTyped

    }//GEN-LAST:event_sendMessageTextPaneKeyTyped
    
    /**
     * When user presses this option, a new window is displayed for create a new conversation.
     * 
     * @param evt - event.
     */
    private void newConversationButtonActionPerformed(java.awt.event.ActionEvent evt){
        NewConversation newCnvWin = new NewConversation();
        newCnvWin.setVisible(true);
    }
    
    /**
     * This method returns the conversation iD of the conversation that is selected.
     * 
     * @return convID - Conversation ID.
     */
    public int getSelectedConversationID(){
        int convID =-100;
        String selectedValue = null;
        try {
            selectedValue = getClearSelectedValue(conversationsList.getSelectedValue().toString());
        } catch(java.lang.NullPointerException ex){
            System.out.println("EXCEPTION: No conversation is selected in conversationsList.");
            return -100;
        }

        for (Conversation  conv : conversations){
            if(conv.getName().equals(selectedValue)){
                convID = conv.getId();
                break;
            }
        }
        return convID;
    }
    
    /**
     * This method returns the ID of the user selected.
     * 
     * @return receiverID if found, -50 if there is no selected conv, -10 for group chat
     */
    private int getSelectedReceiverID(){
        
        String convName = "";
        try {
            convName = getClearSelectedValue(conversationsList.getSelectedValue().toString()); // name of conversation
        } catch(java.lang.NullPointerException ex){
            System.out.println("EXCEPTION: No conversation is selected in conversationsList.");
            sendMessageTextPane.setText("");
            return -50;
        }
        
        int receiverID=-10;
        ArrayList<User> global = GuiHandler.getInstance().searchGlobalUsers("", user.getId());
        for(User u : global){
            if(convName.equals(u.getUsername())){
                receiverID = u.getId();
                break;
            }
        }
        return receiverID;
    }
    
    /**
     * This method returns the ID of the file selected.
     * 
     * @return convID if it is founded, -100 if there is not file selected.
     */
    private int getSelectedFileID(){
        int convID =-100;
        String selectedValue = null;
        try{
            selectedValue = getClearFileId(filesList.getSelectedValue().toString());
        }catch(java.lang.NullPointerException ex){
            System.out.println("EXCEPTION: no file is selected on filesList.");
            return -100;
        }
        convID = Integer.parseInt(selectedValue);
        return convID;
    }
    
    /**
     * This method returns the file's name of the selected file.
     * 
     * @return selectedValue - name of the selected file. 
     */
    private String getSelectedFileName(){
        String selectedValue = getClearFileName(filesList.getSelectedValue().toString());
        return selectedValue;
    }
    
    /**
     * This method take some part of the conversation's name.
     * 
     * @param convName - All the conversation name.
     * @return clear - Part of the conversation name.
     */
    public String getClearSelectedValue(String convName){
        String[] parts = convName.split("\\(");
        String clear = parts[0];
        clear = clear.substring(0,clear.length()-1);
        return clear;
    }
    
    /**
     * This method takes some parts of the file ID.
     * 
     * @param dirty - All the file ID.
     * @return clear - Part of the file ID.
     */
    private String getClearFileId(String dirty){
        String[] parts = dirty.split("|");
        String clear = parts[0];
        return clear;
    }
    
    /**
     * This method takes some parts of the file name.
     * 
     * @param dirty - All the file name.
     * @return clear - Part of the file name without blanks.
     */
    private String getClearFileName(String dirty){
//        System.out.println("dirty: " + dirty);
        String[] parts = dirty.split("|");
        String clear= "";
        for(int i=2; i<parts.length; i++)
            clear += parts[i];
        
//        System.out.println("clear: " + clear);
        return clear.trim();
    }
    
    /**
     * This method returns the selected conversation name.
     * 
     * @return the selected conversation name.
     */
    public String getSelectedConversationName(){
        return getClearSelectedValue(conversationsList.getSelectedValue().toString());
    }
    
    /**
     * This method returns the user.
     *          
     * @return user.
     */
    public User getUser() { return user; }

    /**
     * This method sets the user.
     * 
     * @param user
     */
    public void setUser(User user) { this.user = user; }
    
    /**
     * Main method which starts the class.
     * 
     * @param args - the command line arguments.
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
            java.util.logging.Logger.getLogger(HomePage.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(HomePage.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(HomePage.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(HomePage.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new HomePage().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem aboutSubMenu;
    private javax.swing.JMenuItem addDeleteUserSubMenu;
    private javax.swing.JButton addUserToConversationBut;
    private javax.swing.JMenu addressBookMenu;
    private javax.swing.JMenu adminFeaturesMenu;
    private javax.swing.JMenuItem adminPanelSubMenu;
    private javax.swing.JButton attachFile;
    private javax.swing.JMenuItem blockUnblockUserSubMenu;
    private javax.swing.JMenuItem changePasswordMenu;
    private javax.swing.JMenuItem checkStatsSubMenu;
    private javax.swing.JList conversationsList;
    private javax.swing.JPanel conversationsPanel;
    private javax.swing.JMenuItem filesDatabaseSubMenu;
    private javax.swing.JList filesList;
    private javax.swing.JMenu helpMenu;
    private javax.swing.JCheckBoxMenuItem jCheckBoxMenuItem1;
    private javax.swing.JMenu jMenu1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JScrollPane jScrollPane4;
    private javax.swing.JScrollPane localAddresBookScrollPane;
    private javax.swing.JList localAddressBookList;
    private javax.swing.JLabel logo;
    private javax.swing.JMenu materialRepoMenu;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JTextArea messageHistoryTextArea;
    private javax.swing.JButton newConversationButton;
    private javax.swing.JPanel sendMessagePanel;
    private javax.swing.JTextPane sendMessageTextPane;
    private javax.swing.JButton sendTextBut;
    private javax.swing.JMenu settingsMenu;
    private javax.swing.JMenu statisticsMenu;
    private javax.swing.JRadioButtonMenuItem statusAvailableSubMenu;
    private javax.swing.JRadioButtonMenuItem statusBusySubMenu;
    private javax.swing.JMenu statusMenu;
    private javax.swing.ButtonGroup userStatus;
    // End of variables declaration//GEN-END:variables
}
