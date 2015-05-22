package magic.effects;

import cards.Card;

public class TapSelfEffect extends Effect {
	
	// It doesn't matter which of these is used, bust most likely will be the
	// parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		((Card)theObject).tap();
	}

}
