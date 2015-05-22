package magic.effects;

import cards.Card;
import cards.cardComparator;

/**
 * The Kithkin Zephyrnaut has a kinship ability that states if the player who
 * controls it reveals a card from the top of their library at the beginning of
 * their turn (in essence, drawing), they can give Kithkin Zephyrnaut +2/+2, 
 * flying and vigilance until end of turn.
 */
public class BeefZephyrnautIfKinshipEffect extends Effect{

	// The default executeEffect should never be called since it is very 
	// dependent on card type what happens in this effect

	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was " +
				"inappropriately called in BeefZephyrnautIfKinshipEffect");		
	}

	public void executeEffect(Object theObject) {
		// If theNewCard (which should be the card we drew) shares a type with
		// the zephyrnaut, beef it up until end of turn.
		if(cardComparator.subTypesEqual(myCard, (Card)theObject))
		{
			Effect effect = new FlyingForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new VigilanceForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOnePowerToCreatureForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOnePowerToCreatureForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOneToughToCreatureForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOneToughToCreatureForTurnEffect();
			effect.setMyCard(myCard);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
		}
	}

}
