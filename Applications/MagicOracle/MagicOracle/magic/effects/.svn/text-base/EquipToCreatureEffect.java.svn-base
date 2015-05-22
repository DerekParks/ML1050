package magic.effects;

import cards.artifacts.EquipmentCard;
import cards.creatures.CreatureCard;

public class EquipToCreatureEffect extends Effect {

	// The default executeEffect should never be called since we're attaching 
	// the card to a creature, and we need to know which creature that is.

	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in EquipToCreatureEffect");
	}

	/**
	 * The card passed into this function needs to be a creature card, since 
	 * we're going to cast it to be a creature so that we can equip it to that 
	 * creature.  The card that this effect was created with also needs to be
	 * an equipment card so that we can actually attach it to the creature.
	 */
	public void executeEffect(Object theObject) {
		((CreatureCard)theObject).attachEquipment((EquipmentCard)myCard);
		
	}

}
