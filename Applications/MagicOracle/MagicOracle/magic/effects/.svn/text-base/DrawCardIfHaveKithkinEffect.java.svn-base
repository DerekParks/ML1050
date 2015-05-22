package magic.effects;

import java.util.Vector;

import cards.cardComparator;
import cards.creatures.CreatureCard;
import exceptions.LoseGameException;

public class DrawCardIfHaveKithkinEffect extends Effect {

	// It doesn't matter which of these is called, all we're doing is checking
	// if the player controls a kithkin, and if so drawing a card.

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		if (playerHasKithkin()) {
			try {

				myPlayer.draw();
			} catch (LoseGameException e) {
				System.out
						.println(myPlayer.getName()
								+ " tried to draw from the DrawCardIfHaveKithkin effect");
			}
		}
	}

	/**
	 * This is just a small helper function that checks through a players'
	 * creatures, enchantments, and artifacts to see if that player controls a
	 * Kithkin.
	 */
	private boolean playerHasKithkin() {
		Vector<CreatureCard> creatures = myPlayer.getCreaturesInPlay();
		for (int i = 0; i < creatures.size(); i++) {
			if (cardComparator.subTypeEquals(creatures.elementAt(i), "Kithkin")) {
				return true;
			}
		}
		Vector<CreatureCard> enchantments = myPlayer.getCreaturesInPlay();
		for (int i = 0; i < enchantments.size(); i++) {
			if (cardComparator.subTypeEquals(enchantments.elementAt(i),
					"Kithkin")) {
				return true;
			}
		}
		Vector<CreatureCard> artifacts = myPlayer.getCreaturesInPlay();
		for (int i = 0; i < artifacts.size(); i++) {
			if (cardComparator.subTypeEquals(artifacts.elementAt(i), "Kithkin")) {
				return true;
			}
		}
		return false;
	}

}
