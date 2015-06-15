package se.bth.swatkats.letstalk.gui;

import java.io.Serializable;
import java.sql.*;
        

/**
 * This class creates the conversation object which has information about
 * the conversation between users.
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada.
 */
public class Conversation implements Serializable{

    private static final long serialVersionUID = 6826025394745111598L;
    private int id;
    private String name;
    private Timestamp lastMessage;

    /**
     * Constructor 1 - Creates new object Conversation.
     */
    public Conversation(){
        id =0;
        name = null;
        lastMessage = null;
    }
    
    /**
     * Constructor 2 - Creates new object Conversation.
     * 
     * @param id - This number identified the conversation.
     * @param name - This variable provides a name for the conversation.
     */
    public Conversation(int id, String name){
        this.id = id;
        this.name = name;
        java.util.Date now = new java.util.Date();
        lastMessage = new Timestamp(now.getTime());
    }
    
    /**
     * Constructor 3 - Creates new object Conversation.
     * 
     * @param id - This number identified the conversation.
     * @param name - This variable provides a name for the conversation.
     * @param time  - This variable provides a timestamp for the conversation.
     */
    public Conversation(int id, String name, Timestamp time){
        this.id = id;
        this.name = name;
        lastMessage = time;
    }
    
    /**
     * This method gets the conversation id.
     * 
     * @return id
     */
    public int getId() {
        return id;
    }

    /**
     * This method sets the conversation id.
     * 
     * @param id 
     */
    public void setId(int id) {
        this.id = id;
    }
    
    /**
     * This method gets the conversation name.
     * 
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * This method sets the conversation name.
     * 
     * @param name 
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * This method gets the time of the last message.
     * 
     * @return lastMessage
     */
    public Timestamp getLastMessage() {
        return lastMessage;
    }

    /**
     * This method sets the time of the last message.
     * 
     * @param lastMessage 
     */
    public void setLastMessage(Timestamp lastMessage) {
        this.lastMessage = lastMessage;
    }
    
    
}