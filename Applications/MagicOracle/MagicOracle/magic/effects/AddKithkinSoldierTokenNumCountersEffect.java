package magic.effects;

public class AddKithkinSoldierTokenNumCountersEffect extends Effect{

	// It really doesn't matter which of these executeEffects is called, but 
	// most likely it will be the parameter-less one
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		for(int i=0; i<myCard.getNumCounters(); i++)
		{
			Effect newEffect = new AddKithkinSoldierTokenEffect();
			newEffect.setMyCard(myCard);
			newEffect.setMyPlayer(myPlayer);
			newEffect.executeEffect();
		}
	}

}
