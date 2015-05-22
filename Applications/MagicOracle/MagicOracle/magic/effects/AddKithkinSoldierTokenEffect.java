package magic.effects;

import cards.creatures.CreatureCard;

public class AddKithkinSoldierTokenEffect extends Effect {

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		CreatureCard theToken = new CreatureCard("Token",1,1);
		theToken.subtypes[0] = "Kithkin";
		theToken.subtypes[1] = "Soldier";
		myCard=theToken;
		myPlayer.addCreatureInPlay(theToken);
	}

}
