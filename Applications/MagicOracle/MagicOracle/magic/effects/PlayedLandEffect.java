package magic.effects;

public class PlayedLandEffect extends Effect{

	@Override
	public void executeEffect() {
		myPlayer.setHasPlayedLand(true);
		
	}

	@Override
	public void executeEffect(Object theObject) {
		executeEffect();
		
	}

}
