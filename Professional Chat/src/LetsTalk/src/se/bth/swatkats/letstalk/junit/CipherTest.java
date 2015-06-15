package se.bth.swatkats.letstalk.junit;

import static org.junit.Assert.*;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.Serializable;
import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Arrays;

import javax.crypto.KeyAgreement;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import org.junit.Test;

import se.bth.swatkats.letstalk.Constants;
import se.bth.swatkats.letstalk.Utils;
import se.bth.swatkats.letstalk.connection.encryption.CryptModule;
import se.bth.swatkats.letstalk.connection.encryption.Encrypter;

public class CipherTest {

	private SecretKey key1;

	private SecretKey key2;

	private KeyPair kp1;

	@Test
	public void test() {
		try {
			PublicKey alicepublic = initKeyExchange();
			PublicKey bobpublic = generateKeyPairFromClientKey(alicepublic);
			retreiveKey(bobpublic);
		} catch (Exception e) {
			e.printStackTrace();
		}
		assertArrayEquals(key1.getEncoded(), key2.getEncoded());
	}

	public PublicKey initKeyExchange() throws Exception {
		kp1 = CryptModule.kpg.genKeyPair();
		PublicKey pbk1 = kp1.getPublic();
		return pbk1;
	}

	public PublicKey generateKeyPairFromClientKey(PublicKey pbk1)
			throws Exception {
		KeyPair kp = CryptModule.kpg.genKeyPair();
		key2 = agreeSecretKey(kp.getPrivate(), pbk1, true);
		System.out.println("Bob: " + Utils.toHexString(key2.getEncoded()));
		return kp.getPublic();
	}

	// -----------------------------------------------------------------------------------

	public void retreiveKey(PublicKey pbk2) throws Exception {
		key1 = agreeSecretKey(kp1.getPrivate(), pbk2, true);
		System.out.println("Alice: " + Utils.toHexString(key1.getEncoded()));
	}

	public static SecretKey agreeSecretKey(PrivateKey prk_self,
			PublicKey pbk_peer, boolean lastPhase) throws Exception {
		// instantiates and inits a KeyAgreement
		KeyAgreement ka = KeyAgreement.getInstance("DH");
		ka.init(prk_self);
		// Computes the KeyAgreement
		ka.doPhase(pbk_peer, lastPhase);
		// Generates the shared secret
		byte[] secret = ka.generateSecret();

		// === Generates an AES key ===
		MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
		byte[] bkey = Arrays.copyOf(sha256.digest(secret),
				Constants.AES_KEY_SIZE / Byte.SIZE);

		SecretKey desSpec = new SecretKeySpec(bkey, "AES");
		return desSpec;
	}

	@Test
	public void testEncryptDecryptString() {
		test();
		String orig = "hello";
		try {
			assertEquals(
					orig,
					Encrypter.decrypt(key1,
							Encrypter.encrypt(key2, orig)));
		} catch (Exception e) {
			fail();
			e.printStackTrace();
		}

	}

	@Test
	public void testEncryptDecryptPerson() {
		test();
		Person orig = new Person("Jack", 21);
		Person sec = null;
		try {
			sec = (Person) Encrypter.decrypt(key2,
					Encrypter.encrypt(key1, orig));
		} catch (Exception e) {
			e.printStackTrace();
			fail();
		}
		assertEquals(orig, sec);
	}

	static class Person implements Serializable {
		private static final long serialVersionUID = 0;
		private final String name;
		private final int age;

		Person(String name, int age) {
			this.name = name;
			this.age = age;
		}

		@Override
		public boolean equals(Object o) {
			if (this == o) {
				return true;
			}
			if (o == null || getClass() != o.getClass()) {
				return false;
			}

			Person person = (Person) o;

			if (age != person.age) {
				return false;
			}
			if (!name.equals(person.name)) {
				return false;
			}

			return true;
		}

		@Override
		public int hashCode() {
			int result = name.hashCode();
			result = 31 * result + age;
			return result;
		}
	}
}