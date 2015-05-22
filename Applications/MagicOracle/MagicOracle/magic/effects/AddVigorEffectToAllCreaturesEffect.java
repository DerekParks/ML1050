package magic.effects;

public class AddVigorEffectToAllCreaturesEffect extends Effect {

	// It really doesn't matter which of these is called, but it will probably
	// be the default.
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		Effect theEffect;
		for(int i=0; i<myPlayer.getCreaturesInPlay().size(); i++)
		{
			theEffect = new AddVigorEffectToCreatureEffect();
			theEffect.setMyPlayer(myPlayer);
			theEffect.setMyCard(myPlayer.getCreaturesInPlay().elementAt(i));
			theEffect.executeEffect(myPlayer.getCreaturesInPlay().elementAt(i));
		}
	}

}
