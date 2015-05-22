package magic.effects;

import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to remove flying to it.
 *
 */
public class RemoveFlyingEffect extends Effect{

	// It doesn't matter which of these executeEffects is called, but more than
	// likely it will be the parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).setFlying(false);		
	}

}
