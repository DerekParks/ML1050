package magic.effects;

import cards.creatures.CreatureCard;

public class AddElfWarriorTokenEffect extends Effect {

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		CreatureCard theToken = new CreatureCard("Token",1,1);
		theToken.subtypes[0] = "Elf";
		theToken.subtypes[1] = "Warrior";
		myPlayer.addCreatureInPlay(theToken);
	}

}
