import magic.MagicOracle;

public class CardDriver {

	public static void main(String args[]) {
		MagicOracle oracle = new MagicOracle("data\\kithkinDeck.xml",
				"data\\elfDeck.xml", "player1.txt", "player2.txt");
		oracle.run(1);
	}
}
