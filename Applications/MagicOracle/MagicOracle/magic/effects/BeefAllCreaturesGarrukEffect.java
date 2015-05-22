package magic.effects;

import cards.creatures.CreatureCard;

public class BeefAllCreaturesGarrukEffect extends Effect{

	// It really doesn't matter which of these is called, but most likely it 
	// will be the default.
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was " +
				"inappropriately called in BeefZephyrnautIfKinshipEffect");		
	}

	public void executeEffect(Object theObject) {
		for(int i=0; i<myPlayer.getCreaturesInPlay().size(); i++)
		{
			CreatureCard theCreature = myPlayer.getCreaturesInPlay().elementAt(i);
			Effect effect = new TrampleForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOnePowerToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOnePowerToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOnePowerToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOneToughToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOneToughToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
			effect = new AddOneToughToCreatureForTurnEffect();
			effect.setMyCard(theCreature);
			effect.setMyPlayer(myPlayer);
			effect.executeEffect();
		}
	}

}
