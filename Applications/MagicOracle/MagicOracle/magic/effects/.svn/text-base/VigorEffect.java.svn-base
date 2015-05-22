package magic.effects;

import cards.creatures.CreatureCard;

public class VigorEffect extends Effect {

	// The default executeEffect should never be called since we need to know
	// how much damage we're preventing here.
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in VigorEffect");		
	}

	public void executeEffect(Object theObject) {
		int damageToTake = (Integer)theObject;
		((CreatureCard)myCard).changePower(damageToTake);
		((CreatureCard)myCard).changeToughness(damageToTake);
		((CreatureCard)myCard).changeCurrentHealth(damageToTake);
		((CreatureCard)myCard).changeCurrentHealth(damageToTake);
	}

}
