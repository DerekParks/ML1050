package magic.effects;

import java.util.Vector;

import cards.cardComparator;
import cards.creatures.CreatureCard;

/**
 * Note that this class adds not only a counter for each kithkin in play, but 
 * also a +1/+1 for each kithkin in play.  This class also assumes that the
 * card being invoked by it is a creature card.
 * @author Brandon
 *
 */
public class AddCountersNumKithkinEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		Vector<CreatureCard> creaturesInPlay = myPlayer.getCreaturesInPlay();
		for(int i=0; i<creaturesInPlay.size(); i++)
		{
			if(cardComparator.subTypeEquals(myCard, "Kithkin"))
			{
				myCard.addCounter();
				((CreatureCard)myCard).changePower(1);
				((CreatureCard)myCard).changeToughness(1);
			}
		}		
	}

}
