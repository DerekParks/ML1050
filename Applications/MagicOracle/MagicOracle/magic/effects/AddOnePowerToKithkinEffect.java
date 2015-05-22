package magic.effects;

import cards.Card;
import cards.cardComparator;
import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to add power to it.
 */
public class AddOnePowerToKithkinEffect extends Effect{
	
	// It doesn't matter which one of these executeEffects is called.
	
	public void executeEffect()
	{
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		if(cardComparator.subTypeEquals((Card)theObject, "Kithkin"))
		{
			((CreatureCard)theObject).changePower(1);
		}
	}

}
