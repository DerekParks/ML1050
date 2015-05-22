package magic.effects;

import cards.Card;
import cards.cardComparator;
import cards.creatures.CreatureCard;

public class AddNumCountersKithkinToughEffect extends Effect{

	// The default executeEffect should never be called since it is very 
	// dependent on card type what happens in this effect

	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was " +
				"inappropriately called in AddNumCountersKithkinToughEffect");
	}

	/**
	 * Note that this Effect should be called on a creature coming into play,
	 * so we'll cast the card type to be CreatureCard and act based on that
	 * assumption.  If we were sent anything else, the results are going to
	 * be unpredictable and catastrophic.
	 */
	public void executeEffect(Object theObject) {
		// Note the important distinction here that "myCard" is the card 
		// already in play (i.e. Door of Destinies) and the card coming into
		// play is theNewCard.
		if(cardComparator.subTypeEquals((Card)theObject, "Kithkin"))
		{
			((CreatureCard)theObject).changeToughness(myCard.getNumCounters());
		}
		
	}

}
