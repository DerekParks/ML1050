package magic.effects;

import cards.Card;
import cards.cardComparator;
import cards.creatures.CreatureCard;

public class AddOnePowerIfElfEffect extends Effect {

	// The default executeEffect should never be called since we need to know 
	// whether the creature that entered play was an elf.

	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in AddOnePowerIfElfEffect");
	}

	/**
	 * The card passed into this function needs to be a card, since we're 
	 * going to cast it to be a card so that we can test whether it is an elf 
	 * or not. 
	 */
	public void executeEffect(Object theObject) {
		if(cardComparator.subTypeEquals((Card)theObject, "Elf"))
		{
			((CreatureCard)myCard).changePower(1);
		}
		
	}

}
