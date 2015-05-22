package magic.effects;

public class AddAnyColorEffect extends Effect {

	// The default executeEffect should never be called since it is very 
	// dependent on what creature entered play in order for this effect to
	// happen.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	/**
	 * I'm not really sure what would be passed in here, but we can allow it.
	 */
	public void executeEffect(Object theObject) {
		String colorChoice = myPlayer.getStrategy().addColorOfChoice("bgruw");
		if(colorChoice == "b")
		{
			myPlayer.getManaPool().incrementBlack();
		}
		else if(colorChoice == "g")
		{
			myPlayer.getManaPool().incrementGreen();
		}
		else if(colorChoice == "r")
		{
			myPlayer.getManaPool().incrementRed();
		}
		else if(colorChoice == "u")
		{
			myPlayer.getManaPool().incrementBlue();
		}
		else if(colorChoice == "w")
		{
			myPlayer.getManaPool().incrementWhite();
		}
		else
		{
			System.out.println("ERROR: Strategy cheated and told me I could " +
					"add a " + colorChoice);
		}
	}

}
