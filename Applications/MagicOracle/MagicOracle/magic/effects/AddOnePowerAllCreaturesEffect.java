package magic.effects;

import java.util.Vector;

import cards.creatures.CreatureCard;

/**
 * This class has a requirement that the card that is passed in is a creature
 * card, since we're going to add power to it.
 *
 */
public class AddOnePowerAllCreaturesEffect extends Effect{

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
			creaturesInPlay.elementAt(i).changePower(1);
		}		
	}

}
