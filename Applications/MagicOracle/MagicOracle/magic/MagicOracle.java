package magic;

import strategy.LameStrategy;
import utils.Logger;

public class MagicOracle {

	private Player alan;

	private Player brandon;

	private Logger log;

	/**
	 * Default constructor
	 * 
	 * @param file1
	 *            The file containing the first player's deck XML.
	 * @param file2
	 *            The file containing the second player's deck XML.
	 * @param output1
	 *            The output file containing the statistics for player 1
	 * @param output2
	 *            The output file containing the statistics for player 2
	 */
	public MagicOracle(String file1, String file2, String output1,
			String output2) {
		// Create two players
		alan = new Player(file1, output1, "Player 1");
		alan.setStrategy(new LameStrategy(alan));
		brandon = new Player(file2, output2, "Player 2");
		brandon.setStrategy(new LameStrategy(brandon));
		log = new Logger("game.log", 3);

	}

	/**
	 * Run the specified number of games.
	 * 
	 * @param numGames
	 *            The number of games to run.
	 */
	public void run(int numGames) {
		// Using the same players, create and run numGames games.
		for (int i = 0; i < numGames; i++) {
			Game game = new Game(alan, brandon);
			log.print("---------------------Starting game " + i
					+ "------------------------", 1);
			game.start();
		}
	}
}
