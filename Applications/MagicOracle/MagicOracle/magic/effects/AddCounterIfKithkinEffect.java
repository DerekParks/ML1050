package magic.effects;

import cards.Card;
import cards.cardComparator;

public class AddCounterIfKithkinEffect extends Effect{

	/**
	 * The default executeEffect should never be called since it is very
	 * dependent on card type what happens in this effect 
	 */
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was " +
				"inappropriately called in AddCounterIfKithkinEffect");
	}

	/**
	 * Whatever is passed in here needs to be a card, since we're going to 
	 * check the card type to see if it's a Kithkin.
	 */
	public void executeEffect(Object theObject) {
		// If the creature that entered play was a kithkin, add a counter
		if(cardComparator.subTypeEquals((Card)theObject, "Kithkin"))
		{
			myCard.addCounter();
			
			// These effects have to be executed here because in the XML code
			// there is no place for a condition, so the effects have to get
			// their conditionality from here.
			Effect effect1 = new AddOnePowerAllKithkinEffect();
			effect1.setMyCard((Card)theObject);
			effect1.setMyPlayer(myPlayer);
			effect1.executeEffect();
			Effect effect2 = new AddOneToughAllKithkinEffect();
			effect2.setMyCard((Card)theObject);
			effect2.setMyPlayer(myPlayer);
			effect2.executeEffect();
		}
	}

}
