package magic.effects;

public class PutElfCardOnTopEffect extends Effect {

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		myPlayer.getStrategy().putCardOnTop("Elf");
	}

}
