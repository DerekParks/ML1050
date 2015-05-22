package magic.effects;

import cards.lands.LandCard;

/**
 * It is expected that the card passed into this method is a LandCard, since 
 * that card will be added to the player's Land in play.
 *
 */
public class AddLandEffect extends Effect{

	// It doesn't matter which of the executeEffects is called, but most likely
	// it will be the parameter-less one.
	
	public void executeEffect() {
		myCard.setTapped(false);
		executeEffect(myCard);
	}
	
	public void executeEffect(Object theObject) {
		myPlayer.addLand((LandCard)theObject);
		
	}

}
