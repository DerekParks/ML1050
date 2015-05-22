package mana;

import java.util.Vector;

import magic.Player;
import magic.costs.Cost;
import cards.Card;

/**
 * This holds all costs necessary for an ability
 * 
 * @author Alan
 * 
 */
public class AbilityCost {

	/**
	 * The mana necessary to play this ability.
	 */
	private Mana cost;

	/**
	 * Any additional costs necessary to play this ability.
	 */
	private Vector<Cost> additionalCosts;

	public AbilityCost() {
		cost = new Mana();
		additionalCosts = new Vector<Cost>();
	}

	public void addCost(Cost c) {
		additionalCosts.add(c);
	}

	public boolean playable(Player p, Card c) {
		// Create an object holding the untapped lands for a player
		Mana availableLands = p.getManaPool();
		// Get the total untapped land for the player
		int totalUntappedMana = availableLands.getConvertedManaCost();
		// If the cost requires black
		if (cost.getBlack() > 0) {
			// If there aren't enough black lands untapped
			if (availableLands.getBlack() < cost.getBlack()) {
				// The card isn't playable
				return false;
			} else {
				// Otherwise use the black to meet the black requirement and
				// subtract this cost from the total untapped land.
				totalUntappedMana -= (cost
						.getBlack());
			}
		}
		if (cost.getRed() > 0) {
			if (availableLands.getRed() < cost.getRed()) {
				return false;
			} else {
				totalUntappedMana -= (cost.getRed());
			}
		}
		if (cost.getGreen() > 0) {
			if (availableLands.getGreen() < cost.getGreen()) {
				return false;
			} else {
				totalUntappedMana -= (cost.getGreen());
			}
		}
		if (cost.getBlue() > 0) {
			if (availableLands.getBlue() < cost.getBlue()) {
				return false;
			} else {
				totalUntappedMana -= (cost.getBlue());
			}
		}
		if (cost.getWhite() > 0) {
			if (availableLands.getWhite() < cost.getWhite()) {
				return false;
			} else {
				totalUntappedMana -= (cost.getWhite());
			}
		}
		// If the cost requires any colorless, then just take it from whatever's
		// left over from the untapped land.
		if (cost.getColorless() > 0) {
			// If there isn't enough untapped land to pay for the cost
			if (totalUntappedMana < cost.getColorless()) {
				// It cannot be played
				return false;
			}
		}
		// Check each of the other costs and see if any of them can't be met
		for (int i = 0; i < additionalCosts.size(); i++) {
			// If any of the additional costs can't be met then this ability
			// cost cannot be met
			if (!additionalCosts.get(i).playable(p, c)) {
				return false;
			}
		}

		// If it's met all of the above requirements (hasn't returned false for
		// any of the other restrictions) then it can be played.
		return true;
	}

	public Mana getCost() {
		return cost;
	}

	public void setCost(Mana cost) {
		this.cost = cost;
	}
}
