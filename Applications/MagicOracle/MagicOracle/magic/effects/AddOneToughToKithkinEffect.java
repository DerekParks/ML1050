package magic.effects;

import cards.Card;
import cards.cardComparator;
import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to add toughness to it.
 */
public class AddOneToughToKithkinEffect extends Effect{
	
	// It doesn't matter which one of these executeEffects is called.
	
	public void executeEffect()
	{
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		if(cardComparator.subTypeEquals((Card)theObject, "Kithkin"))
		{
			((CreatureCard)theObject).changeToughness(1);
		}
	}

}
