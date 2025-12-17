package kryptotrainer;

import mybiginteger.*;

import java.util.Random;


public class ElGamalEllipt {
	
	
	  BigInteger p;   //Primzahl für GF(p)
	  
	  BigInteger a,b;  //Parameter für die elliptische Kurve (y^2 = x^3 + ax + b)
	  
	  BigInteger[] P = {BigInteger.ZERO, BigInteger.ZERO};  //ausgewählter Punkt (x,y) der elliptischen Kurve
	  
	  BigInteger kA, kB; //geheimer Schlüssel von Alice resp. von Bob
	  
	  BigInteger[] A =  {BigInteger.ZERO, BigInteger.ZERO};  //oeffentlicher Schluessel von Alice

    int shiftSize = 7; // Anzahl der Bits, um die bei der Nachrichtenkodierung verschoben wird
	  

	  /************************************************************************
	   ************************************************************************
	   * Methoden, die ausprogrammiert werden müssen.
	   ************************************************************************
	   ************************************************************************/
	  
	  
	    /**
	     * Berechnet die Verschlüsselung fuer eine Nachricht M, die als Punkt auf der elliptischen Kurve gegeben ist.
	     * @throws Exception 
	     */
	    public BigInteger[] elliptEncrypt(BigInteger[] M) throws Exception 
	    {
		      BigInteger[] B = P[0].elliptMultiply(P[1], kB, p, a, b);
          BigInteger[] intermediate = A[0].elliptMultiply(A[1], kB, p, a, b);
		      BigInteger[] C = M[0].elliptAdd(M[1], intermediate[0], intermediate[1], p, a, b);

        return new BigInteger[]{B[0], B[1], C[0], C[1]};
	    }
	    
	    
	    /**
	     * Berechnet die Entschlüsselung für die Nachricht (B,C) mithilfe von k_A.
	     * @throws Exception 
	     */
	    public BigInteger[] elliptDecrypt(BigInteger[] B, BigInteger[] C) throws Exception
	    {
        // M = C - kA*B
        BigInteger[] s = B[0].elliptMultiply(B[1], kA, p, a, b);
        BigInteger[] sNeg = { s[0], p.subtract(s[1]) }; // negate y: -y mod p
        return C[0].elliptAdd(C[1], sNeg[0], sNeg[1], p, a, b);
	    }
	    
	    
	    /**
	     * Bestimmt zuerst eine Repräsentation der gegebenen Nachricht m als Punkt auf der elliptischen Kurve und berechnet dann die zugehörige Verschlüsselung
	     * @throws Exception 
	     */
	    public BigInteger[] messageEncrypt(BigInteger m) throws Exception
	    {
        // Find point M on curve with x = m shifted left by shiftSize bits
        BigInteger originalX = m.shiftLeft(shiftSize);
        // Search in shifted bits for a valid y
        for (int i = 0; i < (1 << shiftSize); i++) {
          System.out.println(i);
          BigInteger x = originalX.add(BigInteger.valueOf(i));
          BigInteger s = x.modPow(BigInteger.valueOf(3), p).add(a.multiply(x).mod(p)).add(b).mod(p); // s = x^3 + ax + b mod p
          BigInteger y = s.myModSqrt(p);
          if (y.equals(BigInteger.valueOf(-1))) {
            continue; // no valid y found for this x
          }
          return this.elliptEncrypt(new BigInteger[]{x, y}); // Use the first valid y found
        }
        throw new Exception("No valid point found for message");
	    }
	    
	    
	    /**
	     * Bestimmt den durch das Chiffrat (B,C) verschlüsselten Punkt auf der Kurve und berechnet daraus die (durch eine Zahl repräsentierte) versendete Nachricht.
	     * @throws Exception 
	     */
	    public BigInteger messageDecrypt(BigInteger[] B, BigInteger[] C) throws Exception
	    {
        // Use already implemented elliptDecrypt method
        BigInteger[] M = this.elliptDecrypt(B, C);
        return M[0].shiftRight(shiftSize);
	    }
	 


	  /************************************************************************
	   ************************************************************************
	   * Methoden, die fertig vorgegeben sind.
	   ************************************************************************
	   ************************************************************************/

	  public ElGamalEllipt() {
	  }

	  public void setPrimeNumber(BigInteger prime) {
	    p = prime;
	  }
	  
	  public void setParam_a(BigInteger param_a)
	  {
		  a = param_a;
	  }
	  
	  public void setParam_b(BigInteger param_b)
	  {
		  b = param_b;
	  }
	  
	  public void setP(BigInteger[] point)
	  {
		  P[0] = point[0];
		  P[1] = point[1];
	  }
	  
	  public void setKeyAlice(BigInteger keyAlice) throws Exception 
	  {
		  kA = keyAlice;
		  A = P[0].elliptMultiply(P[1], kA, p, a, b);
	  }
	  
	  public void setKeyBob(BigInteger keyBob)
	  {
		  kB = keyBob;
	  }
	  
	}
