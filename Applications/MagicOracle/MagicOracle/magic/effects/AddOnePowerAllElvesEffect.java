package magic.effects;

import java.util.Vector;

import cards.Card;
import cards.cardComparator;
import cards.creatures.CreatureCard;

/**
 * Adds +1 Power to each elf in play under this player's control
 */
public class AddOnePowerAllElvesEffect extends Effect{

	// It doesn't matter which of these executeEffects is called, but more than
	// likely it will be the parameter-less one.
	
	public void executeEffect()
	{
		executeEffect(myCard);
	}
	
	public void executeEffect(Object theObject) {
		Vector<CreatureCard> creaturesInPlay = myPlayer.getCreaturesInPlay();
		for(int i=0; i<creaturesInPlay.size(); i++)
		{
			if(cardComparator.subTypeEquals((Card)theObject, "Elf"))
			{
				creaturesInPlay.elementAt(i).changePower(1);
			}
		}		
	}

}
