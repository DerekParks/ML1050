package statistics;

import java.io.FileOutputStream;
import java.io.PrintStream;

public class Statistics {
	
	StartingHand handStorage;
	FileOutputStream out;
	PrintStream fout;
	
	/**
	 * This opens up the file that we'll be writing to based on the filename 
	 * sent in
	 * @param filename This should be either a new file that the user has 
	 * permission to create, or a file that the user has permissions to write 
	 * to.
	 */
	public Statistics(String filename)
	{
		try
		{
			out = new FileOutputStream(filename);
			fout = new PrintStream( out );
		}
		catch(Exception e)
		{
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	/**
	 * This function is called to start the game.  It creates the starting hand
	 * structure based on which deck this is, and passes in the array of 
	 * strings with the names of the cards in the starting hand.
	 * @param deckType Should be either "Elf" or "Kithkin", based on which deck
	 * this is keeping track of.
	 * @param startingCards The array of strings representing the names of the
	 * cards in the starting hand.
	 */
	public void startGame(String deckType, String[] startingCards)
	{
		if(deckType == "Elf")
		{
			handStorage = new ElfStartingHand(startingCards);
		}
		else if(deckType == "Kithkin")
		{
			handStorage = new KithkinStartingHand(startingCards);
		}
		else
		{
			System.out.println("Unrecognized deck type!");
			System.exit(1);
		}
	}
	
	/**
	 * This function should only be called after startGame is called.  It takes 
	 * the original starting hand and the win or loss and writes this game to a
	 * file.  It then clears the starting hand.
	 * @param didIWin Should be true or false based on whether the game that 
	 * was started was a win or a loss.
	 */
	public void endGame(boolean didIWin)
	{
		String WorL;
		if(didIWin)
		{
			WorL = "W";
		}
		else
		{
			WorL = "L";
		}
		fout.println(WorL + "," + handStorage.startingHandAsString());
		handStorage = null;
	}
	
	/**
	 * This should be called at the end of the collection process.
	 */
	public void closeFile()
	{
		fout.close();
	}

}
