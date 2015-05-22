package magic.effects;

import java.util.Vector;

import cards.cardComparator;
import cards.creatures.CreatureCard;

public class AddPowerNumElvesEffect extends Effect {

	// This requires us to target a creature to execute the effect, so the 
	// parameter-less call will throw a RuntimeException.
	
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in AddPowerNumElvesEffect");
	}

	public void executeEffect(Object theObject) {
		Vector<CreatureCard> creatures = myPlayer.getCreaturesInPlay();
		int numElves = 0;
		for(int i=0; i<creatures.size(); i++)
		{
			if(cardComparator.subTypeEquals(creatures.elementAt(i), "Elf"))
			{
				numElves++;
			}
		}
		((CreatureCard)theObject).changePower(numElves);
	}

}
