package magic.effects;

import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to subtract power from it.
 *
 */
public class MinusOnePowerToCreatureEffect extends Effect{

	// It doesn't matter which of these executeEffects is called, but more than
	// likely it will be the parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	/**
	 * I can't really see why this would ever be called, but just in case I'll
	 * allow it.
	 */
	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).changePower(-1);
	}

}
