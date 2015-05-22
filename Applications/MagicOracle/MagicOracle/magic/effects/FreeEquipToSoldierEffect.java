package magic.effects;

import cards.Card;

public class FreeEquipToSoldierEffect extends Effect {

	// The default executeEffect should never be called since it is very 
	// dependent on what creature entered play in order for this effect to
	// happen.
	
	public void executeEffect() {
		throw new RuntimeException("ERROR:  default executeEffect was inappropriately " +
		"called in FreeEquipToSoldierEffect");
	}

	/**
	 * theObject in this case should be the creature that entered play in
	 * order for this effect to be triggered.  myCard should be the equipment
	 * that is already in play.
	 */
	public void executeEffect(Object theObject) {
		myPlayer.getStrategy().attachEquipmentToSoldier(myCard, (Card)theObject);
	}

}
