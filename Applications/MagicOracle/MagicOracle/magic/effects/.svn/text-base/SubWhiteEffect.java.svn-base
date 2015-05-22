package magic.effects;

public class SubWhiteEffect extends Effect{
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		if(myPlayer.getManaPool().decreaseWhite())
		{
			System.out.println("Tapped successfully");
		}
		else
		{
			System.out.println("Error: there was a problem");
		}
	}

}
