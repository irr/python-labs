/*
 * http://laurentcharignon.com/blog/?p=37
 * http://www.androidsnippets.com/encrypt-decrypt-between-android-and-php
 */

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class MCrypt {

	private IvParameterSpec ivspec;
	private SecretKeySpec keyspec;
	private Cipher cipher;

	public MCrypt() {
		this("ba0113f5b71eb5ce", "ba14f4a4d7ecddbf");
	}

	public MCrypt(String key, String iv) {
		ivspec = new IvParameterSpec(iv.getBytes());
		keyspec = new SecretKeySpec(key.getBytes(), "AES");

		try {
			cipher = Cipher.getInstance("AES/CBC/NoPadding");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public byte[] encrypt(String text) throws Exception {
		if (text == null || text.length() == 0)
			throw new Exception("Empty string");

		byte[] encrypted = null;

		try {
			cipher.init(Cipher.ENCRYPT_MODE, keyspec, ivspec);

			encrypted = cipher.doFinal(padString(text).getBytes());
		} catch (Exception e) {
			throw new Exception("[encrypt] " + e.getMessage());
		}

		return encrypted;
	}

	public byte[] decrypt(String code) throws Exception {
		if (code == null || code.length() == 0)
			throw new Exception("Empty string");

		byte[] decrypted = null;

		try {
			cipher.init(Cipher.DECRYPT_MODE, keyspec, ivspec);

			decrypted = cipher.doFinal(hexToBytes(code));
		} catch (Exception e) {
			throw new Exception("[decrypt] " + e.getMessage());
		}
		return decrypted;
	}

	public static String bytesToHex(byte[] data) {
		if (data == null) {
			return null;
		}

		int len = data.length;
		String str = "";
		for (int i = 0; i < len; i++) {
			if ((data[i] & 0xFF) < 16)
				str = str + "0" + java.lang.Integer.toHexString(data[i] & 0xFF);
			else
				str = str + java.lang.Integer.toHexString(data[i] & 0xFF);
		}
		return str;
	}

	public static byte[] hexToBytes(String str) {
		if (str == null) {
			return null;
		} else if (str.length() < 2) {
			return null;
		} else {
			int len = str.length() / 2;
			byte[] buffer = new byte[len];
			for (int i = 0; i < len; i++) {
				buffer[i] = (byte) Integer.parseInt(
						str.substring(i * 2, i * 2 + 2), 16);
			}
			return buffer;
		}
	}

	private static String padString(String source) {
		char paddingChar = ' ';
		int size = 16;
		int x = source.length() % size;
		int padLength = size - x;

		for (int i = 0; i < padLength; i++) {
			source += paddingChar;
		}

		return source;
	}

	public static void main(String[] args) throws Exception {
		final String plain = args[0];
		final String crypted = MCrypt.bytesToHex(new MCrypt().encrypt(plain));
		final String decrypted = new String(new MCrypt().decrypt(crypted)).trim();
		System.out.println(String.format("Plaintext=[%s]\nEncrypted=[%s]\nDecrypted=[%s]", plain, crypted, decrypted));
	}	
}
