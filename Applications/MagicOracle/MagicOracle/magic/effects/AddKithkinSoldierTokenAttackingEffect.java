package magic.effects;

import cards.creatures.CreatureCard;

public class AddKithkinSoldierTokenAttackingEffect extends Effect {

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		AddKithkinSoldierTokenEffect myEffect = new AddKithkinSoldierTokenEffect();
		myEffect.setMyCard(myCard);
		myEffect.setMyPlayer(myPlayer);
		myEffect.executeEffect();
		myPlayer.addAttackingCreature((CreatureCard)myEffect.getMyCard());
	}

}
