package magic.effects;

public class SubColorlessEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		myPlayer.useColorless();
	}

}
