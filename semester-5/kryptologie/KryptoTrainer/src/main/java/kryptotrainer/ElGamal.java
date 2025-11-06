package kryptotrainer;

import mybiginteger.*;

import java.util.Random;

/**
 * <p>Title: KryptoTrainer</p>
 * <p>Description: Übungsumgebung für das Wahlfach Kryptologie</p>
 * <p>Copyright: Copyright (c) 2006 / Samuel Beer</p>
 * <p>Company: Zürcher Hochschule Winterthur</p>
 * @author Samuel Beer
 * @version 1.0
 */

public class ElGamal {

  int bitLengthPublicKey;          // Länge der Primzahl p in Bits

  BigInteger[] publicKeyAlice;     // Öffentlicher Schlüssel (p,g,A) von Alice

  BigInteger privateKeyAlice;      // Privater Schlüssel a von Alice

  BigInteger plainText;            // Klartext Bob -> Alice

  BigInteger[] cipheredText;       // Chiffrat (B,c) Bob -> Alice

  BigInteger decipheredText;       // Dechiffrierter Text Bob -> Alice


  /************************************************************************
   ************************************************************************
   * Methoden, die ausprogrammiert werden müssen.
   ************************************************************************
   ************************************************************************/

  /**
   * Öffentlichen Schlüssel (p,g,A) und privaten Schlüssel (a) für Alice
   * generieren und in publicKeyAlice bzw. privateKeyAlice speichern.
   */
  public void generateKeyPair() {
    BigInteger.createTableOfPrimes(10000); // für die Methode myProbableSafePrime notwendig
    BigInteger p = BigInteger.myProbableSafePrime(bitLengthPublicKey, 100, new Random());
    BigInteger sizeZP = p.subtract(BigInteger.ONE);
    BigInteger q = sizeZP.divide(BigInteger.valueOf(2));
    BigInteger g = BigInteger.probablePrime(bitLengthPublicKey, new Random());
    while (true) {
      BigInteger v1 = g.modPow(sizeZP.divide(BigInteger.valueOf(2)), p);
      BigInteger v2 = g.modPow(sizeZP.divide(q), p);
      if (!v1.equals(BigInteger.ONE) && !v2.equals(BigInteger.ONE)) {
        break;
      }

      do { // generate g with 1 < g < p-2
        g = BigInteger.probablePrime(bitLengthPublicKey, new Random());
      } while (g.compareTo(BigInteger.ONE) <= 0 || g.compareTo(p.subtract(BigInteger.valueOf(2))) >= 0);
    }

    BigInteger a;
    do { // generate a with 1 < g < p-2
      a = new BigInteger(bitLengthPublicKey, new Random());
    } while (a.compareTo(BigInteger.ONE) <= 0 || a.compareTo(p.subtract(BigInteger.valueOf(2))) >= 0);
    BigInteger A = g.modPow(a, p);
    privateKeyAlice = a;
    publicKeyAlice = new BigInteger[] {p, g, A};
  }

  /**
   * Chiffrat (B,c) Bob -> Alice erstellen und in cipheredText abspeichern.
   */
  public void createCipheredText() {
    BigInteger A = publicKeyAlice[2];
    BigInteger g = publicKeyAlice[1];
    BigInteger p = publicKeyAlice[0];
    BigInteger b;
    do { // generate a with 1 < g < p-2
      b = BigInteger.probablePrime(bitLengthPublicKey, new Random());
    } while (b.compareTo(BigInteger.ONE) <= 0 || b.compareTo(p.subtract(BigInteger.valueOf(2))) >= 0);
    BigInteger B = g.modPow(b, p);
    BigInteger c = (A.modPow(b, p).multiply(plainText)).mod(p);
    cipheredText = new BigInteger[] {B, c};
  }

  /**
   * Dechiffrierten Text Bob -> Alice erstellen und in decipheredText abspeichern.
   */
  public void createDecipheredText() {
    BigInteger B = cipheredText[0];
    BigInteger c = cipheredText[1];
    BigInteger p = publicKeyAlice[0];
    BigInteger a = privateKeyAlice;
    decipheredText = (c.multiply(B.modPow(p.subtract(BigInteger.ONE).subtract(a), p))).mod(p);
  }


  /************************************************************************
   ************************************************************************
   * Methoden, die fertig vorgegeben sind.
   ************************************************************************
   ************************************************************************/

  public ElGamal() {
  }

  public void setBitLength(int len) {
    bitLengthPublicKey = len;
  }

  public void setPlainText(BigInteger plain) {
    plainText = plain;
  }

  public BigInteger[] getCipheredText() {
    return cipheredText;
  }

  public BigInteger getDecipheredText() {
    return decipheredText;
  }

  public BigInteger[] getPublicKey() {
    return publicKeyAlice;
  }

  public BigInteger getPrivateKey() {
    return privateKeyAlice;
  }
}
