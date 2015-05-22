package magic.effects;

import java.util.Vector;

import cards.artifacts.EquipmentCard;
import cards.creatures.CreatureCard;

/**
 * TODO: This is only supposed to occur whenever this creature attacks or 
 * blocks, but for now it doesn't mater so I'll leave it to a later design
 * to figure out how to do that.  It also doesn't work if this creature is 
 * blocking, since it just asks the player which of its creatures are 
 * attacking.  That's probably a more important TODO.
 */
public class AddToughNumAttackersEffect extends Effect {

	// It really doesn't matter which one of these is called, but most likely
	// the parameter-less one, since I don't know what parameter would be being
	// passed.
	
	public void executeEffect() {
		executeEffect(myCard);
	}

	public void executeEffect(Object theObject) {
		// Create an end of turn effect for when we add power or toughness 
		// until end of turn.
		Effect newEffect;
		Vector<CreatureCard> creatures = myPlayer.getCreaturesInPlay();
		for(int i=0; i<creatures.size(); i++)
		{
			if(creatures.elementAt(i).isAttacking())
			{
				// Add the power, then remember to take it off at end of turn.
				((EquipmentCard)myCard).getAttachedCreature().changeToughness(1);
				newEffect = new MinusOneToughToCreatureEffect();
				newEffect.setMyCard(myCard);
				newEffect.setMyPlayer(myPlayer);
				myPlayer.addEndOfTurnEffect(newEffect);
			}
		}		
	}

}
