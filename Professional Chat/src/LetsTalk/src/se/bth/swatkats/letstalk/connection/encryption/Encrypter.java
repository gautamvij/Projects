package se.bth.swatkats.letstalk.connection.encryption;

import java.io.Serializable;

import javax.crypto.Cipher;
import javax.crypto.SealedObject;
import javax.crypto.SecretKey;

import se.bth.swatkats.letstalk.Constants;

/**
 * This class de- and encrypts SealedObjects, given the key.
 * 
 * @author JS
 *
 */
public class Encrypter {

	/**
	 * Encrypts the Object
	 * 
	 * @param key
	 *            the symmetric key to encrypt
	 * @param object
	 *            the object to encrypt
	 * @return a sealed encrypted object
	 * @throws Exception
	 *             if encryption fails.
	 */
	public static SealedObject encrypt(SecretKey key, Serializable object)
			throws Exception {

		// Create cipher
		Cipher cipher = Cipher.getInstance(Constants.transformation);
		cipher.init(Cipher.ENCRYPT_MODE, key);
		return new SealedObject(object, cipher);
	}

	/**
	 * Decrypts the Object
	 * 
	 * @param key
	 *            the symmetric key, which was used to encrypt the message
	 * @param sealedObject
	 *            the sealed object to decrypt
	 * @return the decrypted object
	 * @throws Exception
	 *             if encryption fails.
	 */
	public static Object decrypt(SecretKey key, SealedObject sealedObject)
			throws Exception {
		Cipher cipher = Cipher.getInstance(Constants.transformation);
		cipher.init(Cipher.DECRYPT_MODE, key);
		return sealedObject.getObject(cipher);
	}

}