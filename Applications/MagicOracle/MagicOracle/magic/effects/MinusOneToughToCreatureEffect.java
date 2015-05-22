package magic.effects;

import cards.creatures.CreatureCard;

public class MinusOneToughToCreatureEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}

	/**
	 * I can't really see why this would ever be called, but just in case I'll
	 * allow it.
	 */
	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).changeToughness(-1);
	}


}
