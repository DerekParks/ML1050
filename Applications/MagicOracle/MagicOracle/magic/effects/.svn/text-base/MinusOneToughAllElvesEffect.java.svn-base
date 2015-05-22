package magic.effects;

import java.util.Vector;

import cards.cardComparator;
import cards.creatures.CreatureCard;

public class MinusOneToughAllElvesEffect extends Effect{

	// It doesn't matter which of these executeEffects is called, but more than
	// likely it will be the parameter-less one.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		Vector<CreatureCard> creaturesInPlay = myPlayer.getCreaturesInPlay();
		for(int i=0; i<creaturesInPlay.size(); i++)
		{
			if(cardComparator.subTypeEquals(creaturesInPlay.elementAt(i), "Elf"))
			{
				creaturesInPlay.elementAt(i).changeToughness(-1);
			}
		}
	}

}
