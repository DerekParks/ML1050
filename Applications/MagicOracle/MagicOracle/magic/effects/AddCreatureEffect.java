package magic.effects;

import cards.creatures.CreatureCard;

/**
 * Whatever is passed into this Effect should be a CreatureCard, because we are
 * going to cast it to a CreatureCard so that we can add it to the player's
 * creaturesInPlay
 */
public class AddCreatureEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}
	
	public void executeEffect(Object theObject) {
		myPlayer.addCreatureInPlay((CreatureCard)theObject);
	}

}
