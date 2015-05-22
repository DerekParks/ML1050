package magic.effects;

import cards.Card;

public class DiscardCardEffect extends Effect {

	// It doesn't matter which of these is used, but most likely it will be the
	// parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}
	
	public void executeEffect(Object theObject) {
		myPlayer.discard((Card)theObject);
	}

}
