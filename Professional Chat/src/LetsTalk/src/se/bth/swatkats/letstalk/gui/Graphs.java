package se.bth.swatkats.letstalk.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Toolkit;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JSplitPane;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import se.bth.swatkats.letstalk.connection.GuiHandler;
import se.bth.swatkats.letstalk.connection.packet.UserActivity;
import se.bth.swatkats.letstalk.user.User;



/**
 * This class provides the window which has differents graphs.
 * 
 * @author Sokratis Papadopoulos and David Alarcon Prada.
 */
public class Graphs extends JFrame {
    private JPanel panel,panel2,panel3,panel4;
    private JSplitPane split1,split2,split3;
    static final int widgt = 350; // ancho
    static final int height=300;    //alto
    
    private ArrayList<User> globalUsers; //all global users of application
    private HashMap<String, Integer> totalMessagesPerDay; // date - num_of_total_messages_in_application
    private HashMap<String, Integer> totalMessagesPerUser; // username - num_of_total_user_messages
    private ArrayList<UserActivity> act;
    private HashMap<String, Integer> totalLoginsPerDay;
    private HashMap<String, Integer> totalTimeOnlinePerDay;
    
    /**
     * Creates new form Graphs.
     */
    public Graphs(){
        
        globalUsers = new ArrayList<>();
        totalMessagesPerDay = new HashMap<>();
        totalMessagesPerUser = new HashMap<>();
        act = new ArrayList<>();
        totalLoginsPerDay = new HashMap<>();
        totalTimeOnlinePerDay = new HashMap<>();
        
        //fetch global users
        globalUsers = GuiHandler.getInstance().searchGlobalUsers("", GuiHandler.getInstance().getUser().getId());
        globalUsers.add(GuiHandler.getInstance().getUser());
        
        //total messages by users
        for(User u : globalUsers){
            System.out.println(u.getUsername() + " " + GuiHandler.getInstance().getTotalMessagesSentByUser(u.getId()));
            totalMessagesPerUser.put(u.getUsername(), GuiHandler.getInstance().getTotalMessagesSentByUser(u.getId()));
        }
        
        act = GuiHandler.getInstance().fetchUserActivity(-1); //-1 for global
        
        //total messages per day in application
        SimpleDateFormat dt = new java.text.SimpleDateFormat("YYYY-MM-dd");
        String prev = dt.format(act.get(0).getCheckIn());
        long minutesOnlineOnDay =0;
        Integer loginCountsOnDay = 0;

        minutesOnlineOnDay += getDateDiff(act.get(0).getCheckIn(), act.get(0).getCheckOut(), TimeUnit.MINUTES);
        this.totalMessagesPerDay.put(prev, GuiHandler.getInstance().messagesSentOnASpecificDay(prev));
        
//System.out.println("first day is : " + prev + " with " +GuiHandler.getInstance().messagesSentOnASpecificDay(prev) + " messages");
        
        for(UserActivity a: act){
            if(!dt.format(a.getCheckIn()).equals(prev)){ //next day found
                totalLoginsPerDay.put(prev, loginCountsOnDay);
                totalTimeOnlinePerDay.put(prev, (int) minutesOnlineOnDay);
                
                prev = dt.format(a.getCheckIn()); //get next day
                loginCountsOnDay=1;
                this.totalMessagesPerDay.put(prev, GuiHandler.getInstance().messagesSentOnASpecificDay(prev));
                //System.out.println("next day is : " + prev + " with " + GuiHandler.getInstance().messagesSentOnASpecificDay(prev) + " messages");
            } else {
                loginCountsOnDay++;
                minutesOnlineOnDay += getDateDiff(a.getCheckIn(), a.getCheckOut(), TimeUnit.MINUTES);
                
            }
        }
                   
//        System.out.println("GLOBAL USERS");
//        for (User u : globalUsers){
//            System.out.println(u.getId() + " " + u.getUsername());
//        }
//            
//        System.out.println("USER ACTIVITY");
//        for (UserActivity a : act){
//            System.out.println(a.getUserId() + " " + a.getCheckIn() + " --> " + a.getCheckOut());
//        }
//        
//        System.out.println("TOTAL LOGINS PER DAY");
//        for (Map.Entry<String, Integer> entry : totalLoginsPerDay.entrySet()) {
//            System.out.println( entry.getKey() + " - " + entry.getValue());
//        }
//        
//        System.out.println("TOTAL TIME ONLINE PER DAY");
//        for (Map.Entry<String, Integer> entry : totalTimeOnlinePerDay.entrySet()) {
//            System.out.println( entry.getKey() + " - " + entry.getValue());
//        }
//        
//        System.out.println("TOTAL MESSAGES PER USER");
//        for (Map.Entry<String, Integer> entry : totalMessagesPerUser.entrySet()) {
//            System.out.println( entry.getKey() + " - " + entry.getValue());
//        }
//        
//        System.out.println("TOTAL MESSAGES PER DAY");
//        for (Map.Entry<String, Integer> entry : totalMessagesPerDay.entrySet()) {
//            System.out.println( entry.getKey() + " - " + entry.getValue());
//        }
        
        
        setTitle("Graphs");
        setSize(800,700);
        setLocationRelativeTo(null);
        //setDefaultCloseOperation(EXIT_ON_CLOSE);
        this.setResizable(false);
        setVisible(true);
        init();
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
    
    
    /**
     * This method does the necessary actions to draw the graphs.
     */
    private void init() {
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("img/iconHead.png")));     
        
        panel = new JPanel();
        panel2 =new JPanel();
        panel3 = new JPanel();
        panel4 = new JPanel();
        
        split1=new JSplitPane(JSplitPane.VERTICAL_SPLIT,panel,panel3);
        split1.setOneTouchExpandable(false);
        split1.setDividerLocation(325);
        
        split2=new JSplitPane(JSplitPane.VERTICAL_SPLIT,panel2,panel4);
        split2.setOneTouchExpandable(false);
        split2.setDividerLocation(325);
        
        split3=new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,split1,split2);
        split3.setOneTouchExpandable(false);
        split3.setDividerLocation(400);

        this.setLayout(new BorderLayout());
        this.add(split3, BorderLayout.CENTER);

        // Source of data Graph 1
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        
        for (Map.Entry<String, Integer> entry : totalMessagesPerDay.entrySet()) {
            dataset.setValue(entry.getValue(), entry.getKey(), entry.getKey());
        }
        
        // Creating the Graph 1
        JFreeChart chart = ChartFactory.createBarChart3D("Total Messages Per Day","Day", "Total Messages",dataset, PlotOrientation.HORIZONTAL, true,true, false);
        chart.setBackgroundPaint(Color.decode("#ededff"));
        chart.getTitle().setPaint(Color.decode("#545454"));
        CategoryPlot p = chart.getCategoryPlot();
        p.setRangeGridlinePaint(Color.red);
        // Showing the Graph 1
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(widgt,height));
        panel.add(chartPanel);
        
       // Source of data Graph 2
        DefaultCategoryDataset dataset2 = new DefaultCategoryDataset();
        for (Map.Entry<String, Integer> entry : totalMessagesPerUser.entrySet()) {
            dataset2.setValue(entry.getValue(), entry.getKey(), entry.getKey());
        }
        // Creating the Graph 2
        JFreeChart chart2 = ChartFactory.createBarChart3D("Total Messages Per User","User", "Messages",dataset2, PlotOrientation.HORIZONTAL, true,true, false);
        chart2.setBackgroundPaint(Color.decode("#ededff"));
        chart2.getTitle().setPaint(Color.decode("#545454"));
        CategoryPlot p2 = chart2.getCategoryPlot();
        p2.setRangeGridlinePaint(Color.red);
        // Showing the Graph 2
        ChartPanel chartPanel2 = new ChartPanel(chart2);
        chartPanel2.setPreferredSize(new java.awt.Dimension(widgt,height));
        panel2.add(chartPanel2);
        
        
        // Source of data Graph 3
        DefaultCategoryDataset line_chart_dataset = new DefaultCategoryDataset();
        for (Map.Entry<String, Integer> entry : totalLoginsPerDay.entrySet()) {
            line_chart_dataset.addValue(entry.getValue(), "logins line", entry.getKey());
        }
        
//        line_chart_dataset.addValue(80, "visitas", "Julio");
//        line_chart_dataset.addValue(300, "visitas", "Agosto");
//        line_chart_dataset.addValue(600, "visitas", "Septiembre");
//        line_chart_dataset.addValue(1200, "visitas", "Octubre");
//        line_chart_dataset.addValue(2400, "visitas", "Noviembre");
        // Creating the Graph 3
        JFreeChart chart3=ChartFactory.createLineChart("Total Logins Per Day","Day","Logins",line_chart_dataset,PlotOrientation.VERTICAL,true,true,false);
        chart3.setBackgroundPaint(Color.decode("#ededff"));
        chart3.getTitle().setPaint(Color.decode("#545454"));
        // Showing the Graph 3
        ChartPanel chartPanel3 = new ChartPanel(chart3);
        chartPanel3.setPreferredSize(new java.awt.Dimension(widgt,height));
        panel3.add(chartPanel3);
        
       
        // Source of data Graph 4
        DefaultCategoryDataset line_chart_dataset2 = new DefaultCategoryDataset();
        for (Map.Entry<String, Integer> entry : this.totalTimeOnlinePerDay.entrySet()) {
            line_chart_dataset2.addValue(entry.getValue(), "time online line", entry.getKey());
        }
        
        // Creating the Graph 4
        JFreeChart chart4=ChartFactory.createLineChart("Total Time Online Per Day","Day","Time",line_chart_dataset2,PlotOrientation.VERTICAL,true,true,false);
        chart4.setBackgroundPaint(Color.decode("#ededff"));
        chart4.getTitle().setPaint(Color.decode("#545454"));
        // Showing the Graph 4
        ChartPanel chartPanel4 = new ChartPanel(chart4);
        chartPanel4.setPreferredSize(new java.awt.Dimension(widgt,height));
        panel4.add(chartPanel4);    
    }
     
    /**
     * Main method which starts the class.
     * 
     * @param args the command line arguments.
     */
    public static void main(String args[]){
        new Graphs().setVisible(true);
    }
}
    

