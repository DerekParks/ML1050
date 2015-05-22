package magic.effects;

import cards.creatures.CreatureCard;

public class DealPowerDamageToFlierEffect extends Effect {

	// The default executeEffect should never be called since we're dealing
	// this damage to a creature, so we need to know what that creature is.
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in EquipToCreatureEffect");		
	}

	public void executeEffect(Object theObject) {
		CreatureCard targetCreature = (CreatureCard)theObject;
		targetCreature.changeCurrentHealth(-1*((CreatureCard)myCard).getPower());
	}

}
