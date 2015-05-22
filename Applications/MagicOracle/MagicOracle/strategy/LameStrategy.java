package strategy;

import java.util.Vector;

import magic.Player;
import utils.Logger;
import abilities.Ability;
import cards.Card;
import cards.creatures.CreatureCard;
import cards.instants.InstantCard;

public class LameStrategy extends Strategy {

	Logger log;

	public LameStrategy(Player p) {
		super(p);
		log = new Logger("LameStrategy.log", "LameStrategy", 3);
	}

	@Override
	public void attachEquipmentToSoldier(Card equipmentCard, Card creatureCard) {
		// TODO Auto-generated method stub

	}

	/**
	 * Chooses the attackers to attack with.
	 */
	public Vector<CreatureCard> chooseAttackers() {
		Vector<CreatureCard> attackers = new Vector<CreatureCard>();
		for (int i = 0; i < myPlayer.getCreaturesInPlay().size(); i++) {
			if (myPlayer.getCreaturesInPlay().get(i).isCanAttack()) {
				attackers.add(myPlayer.getCreaturesInPlay().get(i));
			}
		}
		// Attack with all creatures.
		return attackers;
	}

	@Override
	public Vector<Vector<CreatureCard>> chooseDamageAssignment(
			Vector<CreatureCard> attackers,
			Vector<Vector<CreatureCard>> defenders) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Vector<Vector<CreatureCard>> chooseDefenders(
			Vector<CreatureCard> attackers) {

		Vector<Vector<CreatureCard>> blockers = new Vector<Vector<CreatureCard>>();
		for (int i = 0; i < attackers.size(); i++) {
			blockers.add(new Vector<CreatureCard>());
		}
		return blockers;
	}

	@Override
	public void chooseManaColorToGain() {
		// TODO Auto-generated method stub

	}

	@Override
	public void chooseManaColorToLose() {
		if(myPlayer.getManaPool().getWhite() > 0)
		{
			myPlayer.getManaPool().decreaseWhite();
		}
		else if(myPlayer.getManaPool().getGreen() > 0)
		{
			myPlayer.getManaPool().decreaseGreen();
		}
		else if(myPlayer.getManaPool().getBlack() > 0)
		{
			myPlayer.getManaPool().decreaseBlack();
		}
		else if(myPlayer.getManaPool().getRed() > 0)
		{
			myPlayer.getManaPool().decreaseRed();
		}
		else if(myPlayer.getManaPool().getBlue() > 0)
		{
			myPlayer.getManaPool().decreaseBlue();
		}

	}

	@Override
	public void moveCardToTopOfDeck(String type) {
		// TODO Auto-generated method stub

	}

	/**
	 * Determines how to assign damage for the combat phase. This is called by
	 * the attacker.
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
				// After damage has been dealt, see who is still alive.
				blockers.get(i).get(j).checkHealth();
				attackers.get(i).checkHealth();
				// The attacker has been blocked so remove it from the attackers
				// vector.
				attackers.remove(i);
			}
		}

	}

	@Override
	public String addColorOfChoice(String choices) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void chooseMainPhaseAction() {
		Vector<Ability> abilities = myPlayer.createAbilities();
		myPlayer.print();
		for (int i = 0; i < myPlayer.getHand().size(); i++) {
			boolean cardPlayed = false;
			for (int j = 0; !cardPlayed
					&& j < myPlayer.getHand().get(i).getActivatedAbilities()
							.size(); j++) {
				if (myPlayer.getHand().get(i).getActivatedAbilities().get(j)
						.playable(myPlayer, myPlayer.getHand().get(i))
						&& !(myPlayer.getHand().get(i) instanceof InstantCard)) {
					// log.print(cards.get(i).getName() + " has " +
					// cards.get(i).getActivatedAbilities().get(j).getName() + "
					// which I want to play",2);
					// Play the ability
					if (myPlayer.getHand().get(i).getActivatedAbilities()
							.get(j).getName().equals("play")) {
						log.print("Playing "
								+ myPlayer.getHand().get(i).getName(), 2);
						myPlayer.getHand().get(i).getActivatedAbilities()
								.get(j).play();
						cardPlayed = true;
						myPlayer.updateManaPool();
					}
				}
			}
		}

		myPlayer.print();
	}

	public Card putCardOnTop(String cardType) {
		// TODO Auto-generated method stub
		return null;
	}

	public void discardToHandSize() {
		if (myPlayer.getHand().size() > myPlayer.getHandsize()) {
			for (int i = myPlayer.getHand().size() - 1; i > myPlayer
					.getHandsize(); i--) {
				myPlayer.getHand().remove(i);
			}
		}

	}

	public void untapLand() {
		// TODO Auto-generated method stub

	}

	@Override
	public void updateManaPool() {
		for (int i = 0; i < myPlayer.getCreaturesInPlay().size(); i++) {
			if (myPlayer.getCreaturesInPlay().get(i).getName()
					.equalsIgnoreCase("Llanowar Elves")
					&& !myPlayer.getCreaturesInPlay().get(i).isTapped()) {
				myPlayer.getCreaturesInPlay().get(i).tap();
				myPlayer.getManaPool().incrementGreen();
			}
		}

	}

}
