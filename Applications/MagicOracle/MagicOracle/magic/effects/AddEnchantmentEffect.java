package magic.effects;

import cards.enchantments.EnchantmentCard;

public class AddEnchantmentEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		myPlayer.addEnchantmentInPlay((EnchantmentCard)theObject);
	}

}