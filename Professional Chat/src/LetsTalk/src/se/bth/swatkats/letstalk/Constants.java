package se.bth.swatkats.letstalk;

/**
 * A class containing all the constants needed.
 * 
 * @author JS
 *
 */
public class Constants {

	/**
	 * The port to be used to connect from client to server
	 */
	public static final int SERVERPORT = Integer.valueOf(MessageBundle.getString("Constants.SERVERPORT")); //$NON-NLS-1$
	public static final int UPLOADPORT = Integer.valueOf(MessageBundle.getString("Constants.UPLOADPORT")); //$NON-NLS-1$
	public static final int REPOSITORYUPLOADPORT = Integer.valueOf(MessageBundle.getString("Constants.REPOUPLOADPORT")); //$NON-NLS-1$
	public static final int REPOSITORYDOWNLOADPORT = Integer.valueOf(MessageBundle.getString("Constants.REPODOWNLOADPORT")); //$NON-NLS-1$
	public static final int DOWNLOADPORT = Integer.valueOf(MessageBundle.getString("Constants.DOWNLOADPORT")); //$NON-NLS-1$
	public static final String FILEPATH = MessageBundle.getString("Constants.FILEPATH"); //$NON-NLS-1$
	public static final String REPOPATH = MessageBundle.getString("Constants.REPOPATH"); //$NON-NLS-1$

	/**
	 * The host to connect to
	 */
	public final static String HOST = MessageBundle.getString("Constants.HOSTIP"); // "localhost"; //$NON-NLS-1$

	/**
	 * The unique id of the server
	 */
	public final static int SERVERID = Integer.valueOf(MessageBundle.getString("Constants.SERVERID")); //$NON-NLS-1$

	/**
	 * The symmetric encryption algorithm to use
	 */
	public static final String ENC_ALGO = MessageBundle.getString("Constants.ENC_ALGO"); //$NON-NLS-1$

	/**
	 * The message digest algorithm to use
	 */
	public static final String MSG_DIG_ALGO = MessageBundle.getString("Constants.MSG_DIG_ALGO"); //$NON-NLS-1$

	/**
	 * The Key size for the AES encryption
	 */
	public static final int AES_KEY_SIZE = Integer.valueOf(MessageBundle.getString("Constants.AES_KEY_SIZE")); //$NON-NLS-1$

	/**
	 * Parameters for Key Generation in key exchange
	 */
	public static final String KEY_GEN_PARAM = MessageBundle.getString("Constants.KEY_GEN_PARAM"); //$NON-NLS-1$

	/**
	 * Parameters for Number of bits in Key Generation
	 */
	public static final int KEY_GEN_BITS = Integer.valueOf(MessageBundle.getString("Constants.KEY_GEN_BITS")); //$NON-NLS-1$

	/**
	 * Transformation parameter
	 */
	public static final String transformation = MessageBundle.getString("Constants.transformation"); //$NON-NLS-1$

}
