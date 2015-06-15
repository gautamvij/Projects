package se.bth.swatkats.letstalk.connection.encryption;

import java.io.Serializable;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Arrays;

import javax.crypto.KeyAgreement;
import javax.crypto.SealedObject;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.Utils;

/**
 * This class is responsible for encryption and key exchanges
 * 
 * @author JS
 *
 */
public class CryptModule {

	public static KeyPairGenerator kpg;

	static {
		try {
			// === Generates and inits a KeyPairGenerator ===
			kpg = KeyPairGenerator.getInstance(Constants.KEY_GEN_PARAM);
			kpg.initialize(Constants.KEY_GEN_BITS);
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
	}

	private SecretKey key;

	private KeyPair kp1;

	/**
	 * Called when initiating the key exchange. Called by Alice.
	 * 
	 * @return the public key of Alice
	 * @throws Exception
	 *             if something goes wrong.
	 */
	public PublicKey initKeyExchange() throws Exception {
		kp1 = kpg.genKeyPair();
		PublicKey pbk1 = kp1.getPublic();
		return pbk1;
	}

	/**
	 * Second step of the exchange. Called by Bob. After calling this function,
	 * Bob knows the private key.
	 * 
	 * @param pbk1
	 *            the public key of Alice
	 * @return the public key of Bob
	 * @throws Exception
	 *             if something goes wrong.
	 */
	public PublicKey generateKeyPairFromClientKey(PublicKey pbk1)
			throws Exception {
		KeyPair kp = CryptModule.kpg.genKeyPair();
		key = CryptModule.agreeSecretKey(kp.getPrivate(), pbk1, true);
		System.out.println("Bob: " + Utils.toHexString(key.getEncoded()));
		return kp.getPublic();
	}

	/**
	 * Thrid step. Called by Alice. After calling this function, Alice knows the
	 * private key.
	 * 
	 * @param pbk2
	 *            the pubic key of Bob
	 * @throws Exception
	 *             if something goes wrong.
	 */
	public void retreiveKey(PublicKey pbk2) throws Exception {
		key = agreeSecretKey(kp1.getPrivate(), pbk2, true);
		System.out.println("Alice: " + Utils.toHexString(key.getEncoded()));
	}

	private static SecretKey agreeSecretKey(PrivateKey prk_self,
			PublicKey pbk_peer, boolean lastPhase) throws Exception {
		// instantiates and inits a KeyAgreement
		KeyAgreement ka = KeyAgreement.getInstance("DH");
		ka.init(prk_self);
		// Computes the KeyAgreement
		ka.doPhase(pbk_peer, lastPhase);
		// Generates the shared secret
		byte[] secret = ka.generateSecret();

		// === Generates an AES key ===
		MessageDigest sha256 = MessageDigest
				.getInstance(Constants.MSG_DIG_ALGO);
		byte[] bkey = Arrays.copyOf(sha256.digest(secret),
				Constants.AES_KEY_SIZE / Byte.SIZE);

		SecretKey desSpec = new SecretKeySpec(bkey, Constants.ENC_ALGO);
		return desSpec;
	}

	/**
	 * Encrypts the Object. Calls Encrypter with the reteived private key. 
	 * 
	 * @param object
	 *            the object to encrypt
	 * @return a sealed encrypted object
	 */
	public SealedObject encrypt(Serializable object) {
		try {
			return Encrypter.encrypt(key, object);
		} catch (Exception e) {
			System.err.print("Problems with encryption.");
			e.printStackTrace();
			return null;
		}
	}

	/**
	 * Decrypts the Object. Calls Encrypter with the reteived private key. 
	 * 
	 * @param sealedObject
	 *            the sealed object to decrypt
	 * @return the decrypted object
	 */
	public Object decrypt(SealedObject sealedObject) throws Exception {
		try {
			return Encrypter.decrypt(key, sealedObject);
		} catch (Exception e) {
			System.err.print("Problems with decryption.");
			throw new Exception(e);
		}
	}

}