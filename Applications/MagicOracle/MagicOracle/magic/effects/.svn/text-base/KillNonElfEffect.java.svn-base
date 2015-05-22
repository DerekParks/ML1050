package magic.effects;

import cards.creatures.CreatureCard;

public class KillNonElfEffect extends Effect {

	// The default executeEffect should never be called since we're killing a 
	// creature, and we need to know which creature that is.

	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in KillNonElfEffect");
	}

	/**
	 * The card passed into this function needs to be a creature card, since 
	 * we're going to cast it to be a creature so that we can kill it.
	 */
	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).die();
		
	}

}
