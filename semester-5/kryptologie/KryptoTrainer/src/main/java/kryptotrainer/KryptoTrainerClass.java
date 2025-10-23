package kryptotrainer;

import mybiginteger.BigInteger;

import javax.swing.UIManager;
import java.awt.*;
import java.util.Random;

/**
 * <p>Title: KryptoTrainer</p>
 * <p>Description: Übungsumgebung für das Wahlfach Kryptologie</p>
 * <p>Copyright: Copyright (c) 2006 / Samuel Beer</p>
 * <p>Company: Zürcher Fachhochschule Winterthur</p>
 * @author Samuel Beer
 * @version 1.0
 */

public class KryptoTrainerClass {
  boolean packFrame = false;

  //Construct the application
  public KryptoTrainerClass() {
    FrameHaupt frame = new FrameHaupt();
    //Validate frames that have preset sizes
    //Pack frames that have useful preferred size info, e.g. from their layout
    if (packFrame) {
      frame.pack();
    }
    else {
      frame.validate();
    }
    //Center the window
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    Dimension frameSize = frame.getSize();
    if (frameSize.height > screenSize.height) {
      frameSize.height = screenSize.height;
    }
    if (frameSize.width > screenSize.width) {
      frameSize.width = screenSize.width;
    }
    frame.setLocation((screenSize.width - frameSize.width) / 2, (screenSize.height - frameSize.height) / 2);
    frame.setVisible(true);
  }

  //Main method
  public static void main(String[] args) {
    try {
      UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
    }
    catch(Exception e) {
      e.printStackTrace();
    }
    new KryptoTrainerClass();
    /*
    while (true) {
      long startTime = System.currentTimeMillis();
      BigInteger prime = new BigInteger(2048, new Random());
      if (prime.isProbablePrime(10)) {
        long elapsed = System.currentTimeMillis() - startTime;
        System.out.println("Found prime: " + prime + " (Time: " + elapsed + " ms)");
        // Timer resets here for next iteration
      }
    }
    */
  }
}
