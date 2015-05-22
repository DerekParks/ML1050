package strategy;

import java.util.Vector;

import magic.Player;
import cards.Card;
import cards.creatures.CreatureCard;

public class KithkinStrategy extends Strategy{

	KithkinStrategy(Player thePlayer) {
		super(thePlayer);
	}

	public Vector<CreatureCard> chooseAttackers() {
		// TODO Auto-generated method stub
		return null;
	}

	public Vector<Vector<CreatureCard>> chooseDamageAssignment(
			Vector<CreatureCard> attackers,
			Vector<Vector<CreatureCard>> defenders) {
		// TODO Auto-generated method stub
		return null;
	}

	public Vector<Vector<CreatureCard>> chooseDefenders(
			Vector<CreatureCard> attackers) {
		// TODO Auto-generated method stub
		return null;
	}

	public void chooseMainPhaseAction() {
		// TODO Auto-generated method stub
		
	}

	public void attachEquipmentToSoldier(Card equipmentCard, Card creatureCard) {
		// TODO Auto-generated method stub
		
	}

	public void chooseManaColorToGain() {
		// TODO Auto-generated method stub
		
	}

	public void chooseManaColorToLose() {
		// TODO Auto-generated method stub
		
	}

	public void moveCardToTopOfDeck(String type) {
		// TODO Auto-generated method stub
		
	}
	/**
	 * Determines how to assign damage for the combat phase. This is called by
	 * the attacker. Presently this simply iterates through the blockers and
	 * assigns damage in a linear fashion. This should be improved.
	 * 
	 * @param attackers
	 *            The attackers for this combat phase.
	 * @param blockers
	 *            The blockers for this combat phase.
	 */
	public void assignDamage(Vector<CreatureCard> attackers,
			Vector<Vector<CreatureCard>> blockers) {
		// For each group of blockers. Each group of blockers is assigned to a
		// specific attacker.
		for (int i = 0; i < blockers.size(); i++) {
			// The damage that still needs to be dealt. This is initialized to
			// the power of the first attacker. This damage will be distributed
			// among the blockers.
			int damageLeftOver = attackers.get(i).getPower();
			// Iterate through the blocker vector assigned to this attacker.
			for (int j = 0; j < blockers.get(i).size(); j++) {
				// If the damage left over is enough to kill the blocker
				if (damageLeftOver >= blockers.get(i).get(j).getToughness()) {
					// Deal damage equal to the blocker for the full power
					blockers.get(i).get(j).changeCurrentHealth(-damageLeftOver);
					// Then subtract the toughness of the blocker from the
					// damage left over.
					damageLeftOver -= blockers.get(i).get(j).getToughness();
					// Then the blocker deals damage equal to its power to the
					// attacker.
					attackers.get(i).changeCurrentHealth(
							-blockers.get(i).get(j).getPower());
				} else {
					// If the damage isn't enough to kill the blocker.
					// First deal all of the damage to the blocker.
					blockers.get(i).get(j).changeCurrentHealth(-damageLeftOver);
					// Then the blocker deals its damage to the attacker.
					attackers.get(i).changeCurrentHealth(
							-blockers.get(i).get(j).getPower());
					// The damage left over is changed to 0 (this is done in
					// order to prevent dealing - damage (adding health) to the
					// blocker).
					damageLeftOver = 0;
				}
				//After damage has been dealt, see who is still alive.
				blockers.get(i).get(j).checkHealth();
				attackers.get(i).checkHealth();
				//The attacker has been blocked so remove it from the attackers vector.
				attackers.remove(i);
			}
		}

	}

	public Card putCardOnTop(String cardType) {
		// TODO Auto-generated method stub
		return null;
		
	}

	public String addColorOfChoice(String choices) {
		// TODO Auto-generated method stub
		return null;
	}

	public void discardToHandSize() {
		
	}

	public void untapLand() {
		
	}

	@Override
	public void updateManaPool() {
		// TODO Auto-generated method stub
		
	}


}
