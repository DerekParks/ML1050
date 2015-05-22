package magic.effects;

import cards.creatures.CreatureCard;

public class AddGreenBeastTokenEffect extends Effect {

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		CreatureCard theToken = new CreatureCard("Token",3,3);
		theToken.subtypes[0] = "Beast";
		myPlayer.addCreatureInPlay(theToken);
	}

}
