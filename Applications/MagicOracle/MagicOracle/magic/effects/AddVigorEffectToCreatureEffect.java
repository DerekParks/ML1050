package magic.effects;

import cards.creatures.CreatureCard;

public class AddVigorEffectToCreatureEffect extends Effect {

	// The default executeEffect should never be called since we need what 
	// creature to add this effect to.
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in AddVigorEffectToCreatureEffect");		
	}

	public void executeEffect(Object theObject) {
		CreatureCard theCreature = (CreatureCard)theObject;
		Effect theEffect = new VigorEffect();
		theEffect.setMyPlayer(myPlayer);
		theEffect.setMyCard(theCreature);
		theCreature.addBeforeDamageTakenEffect(theEffect);
	}

}
