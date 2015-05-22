package magic;

import java.util.Random;

import utils.Logger;
import exceptions.LoseGameException;

public class Game {

	// The two players used in this game
	Player alan;

	Player brandon;

	Logger log;

	/**
	 * Default constructor
	 * 
	 * @param alan
	 *            The first player to play this game.
	 * @param brandon
	 *            The second player to play this game.
	 */
	Game(Player alan, Player brandon) {
		this.alan = alan;
		this.brandon = brandon;
		alan.setOpponent(brandon);
		brandon.setOpponent(alan);
		log = new Logger("game.log", "Game", 3);
	}

	/**
	 * Starts the game
	 * 
	 */
	public void start() {
		alan.reset();
		brandon.reset();
		// Creates a random number between 0 and 1
		Random generator = new Random();
		int coinflip = generator.nextInt(2);
		// If Alan wins then he skips his first draw (this is reset after
		// skipping 1 draw) and goes first
		try {
			if (coinflip == 0) {
				log.print("Player 1 won the toss!", 1);
				alan.setDraw(false);
				while (alan.getLife() > 0 && brandon.getLife() > 0) {
					alan.playTurn();
					brandon.playTurn();
				}

			} else {
				// Otherwise brandon skips his first draw and goes first
				log.print("Player 2 won the toss!", 1);
				brandon.setDraw(false);
				while (alan.getLife() > 0 && brandon.getLife() > 0) {
					brandon.playTurn();
					alan.playTurn();
				}
			}
		} catch (LoseGameException e) {
			System.out.println(e.getMessage());
		}
	}

	/**
	 * Used strictly for testing purposes before attack and defend are
	 * implemented.
	 */
	public void slowlyKillPlayers() throws LoseGameException{
		alan.changeLife(-1);
		brandon.changeLife(-1);
	}
}
