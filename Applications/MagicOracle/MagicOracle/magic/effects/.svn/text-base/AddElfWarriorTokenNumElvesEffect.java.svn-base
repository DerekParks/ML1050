package magic.effects;

import cards.cardComparator;

public class AddElfWarriorTokenNumElvesEffect extends Effect{

	// It really doesn't matter which of these executeEffects is called, but 
	// most likely it will be the parameter-less one
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		int numElves = 0;
		for(int i=0; i<myPlayer.getCreaturesInPlay().size(); i++)
		{
			if(cardComparator.subTypeEquals(myPlayer.getCreaturesInPlay().elementAt(i), "Elf"))
			{
				numElves++;
			}
		}
		for(int i=0; i<myPlayer.getEnchantmentsInPlay().size(); i++)
		{
			if(cardComparator.subTypeEquals(myPlayer.getEnchantmentsInPlay().elementAt(i), "Elf"))
			{
				numElves++;
			}
		}
			
		for(int i=0; i<numElves; i++)
		{
			Effect newEffect = new AddElfWarriorTokenEffect();
			newEffect.setMyCard(myCard);
			newEffect.setMyPlayer(myPlayer);
			newEffect.executeEffect();
		}
	}

}
