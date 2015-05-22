package abilities;

import java.util.Vector;

import magic.Player;
import magic.effects.Effect;
import mana.AbilityCost;
import cards.Card;

public class Ability {

	private Vector<Effect> effects;

	private String type;

	private AbilityCost cost = new AbilityCost();

	private String name;

	private Card myCard;

	private Player myPlayer;

	public Ability() {
		effects = new Vector<Effect>();
	}

	public Vector<Effect> getEffects() {
		return effects;
	}

	public void setEffects(Vector<Effect> effects) {
		this.effects = effects;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	/**
	 * Checks to see if the ability can be played given the current conditions.
	 * 
	 * @param p
	 *            The player playing the ability.
	 * @param c
	 *            The card containing the ability.
	 * @return True if the card can be played or false if it cannot be played.
	 */
	public boolean playable(Player p, Card c) {
		return cost.playable(p, c);

	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public AbilityCost getCost() {
		return cost;
	}

	public void setCost(AbilityCost cost) {
		this.cost = cost;
	}

	public Card getMyCard() {
		return myCard;
	}

	public void setMyCard(Card myCard) {
		this.myCard = myCard;
	}

	public Player getMyPlayer() {
		return myPlayer;
	}

	public void setMyPlayer(Player myPlayer) {
		this.myPlayer = myPlayer;
	}

	/**
	 * Plays the ability (executes each of its individual effects)
	 * 
	 */
	public void play() {
		for (int i = 0; i < effects.size(); i++) {
			effects.get(i).executeEffect();
		}
	}
	
	/**
	 * If a target is required for the ability then this is included in this call. 
	 * @param o The target of the ability
	 */
	public void play(Object o) {
		for (int i = 0; i < effects.size(); i++) {
			effects.get(i).executeEffect(o);
		}
	}
}
