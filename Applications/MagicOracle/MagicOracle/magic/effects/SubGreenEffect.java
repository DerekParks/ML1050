package magic.effects;

public class SubGreenEffect extends Effect{
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		if(myPlayer.getManaPool().decreaseGreen())
		{
			System.out.println("Tapped successfully");
		}
		else
		{
			System.out.println("Error: there was a problem");
		}
	}

}
