package magic.effects;

import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to add vigilance to it.
 *
 */
public class VigilanceForTurnEffect extends Effect {

	// It doesn't matter which of these executeEffects is called, but more than
	// likely it will be the parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).setVigilance(true);
		Effect newEffect = new RemoveVigilanceEffect();
		newEffect.setMyCard(myCard);
		newEffect.setMyPlayer(myPlayer);
		myPlayer.addEndOfTurnEffect(newEffect);		
	}

}
