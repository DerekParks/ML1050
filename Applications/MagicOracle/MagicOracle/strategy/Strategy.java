package strategy;

import java.util.Vector;

import magic.Player;
import cards.Card;
import cards.creatures.CreatureCard;

public abstract class Strategy {
	
	Player myPlayer;
	
	Strategy(Player thePlayer)
	{
		myPlayer = thePlayer;
	}
	
	public abstract void assignDamage(Vector<CreatureCard> attackers, Vector<Vector<CreatureCard>> blockers);
	/**
	 *  This method is where Strategy decides which of its creatures should be
	 *  sent into battle.
	 */
	public abstract Vector<CreatureCard> chooseAttackers();
	
	/**
	 * This method is where strategy receives the creatures that were sent to
	 * attack and chooses which of its creatures are defending against each of 
	 * those attacking creatures.  Those creatures should be lined up in same
	 * positions that the attackers were sent in in.
	 */
	public abstract Vector<Vector<CreatureCard>> chooseDefenders(Vector<CreatureCard> attackers);
	
	/**
	 * This method receives the attackers that were sent in, the defenders that
	 * were lined up for each of those attackers, and returns a re-ordered
	 * vector of vectors that shows how damage should be assigned to each of
	 * those defenders.
	 * @param attackers The original attacking creatures that were sent in
	 * @param defenders The defenders that the defending player lined up for
	 * each attacking creature.
	 * @return A Vector of Vectors with the defenders lined up for each 
	 * attacker they were blocking in the order the attacker wishes to assign 
	 * damage.
	 */
	public abstract Vector<Vector<CreatureCard>> chooseDamageAssignment(
							Vector<CreatureCard> attackers,
							Vector<Vector<CreatureCard>> defenders);
	
	/**
	 * This is the primary function that the strategy will use to perform all
	 * its actions.  This includes choosing when to attack and when to end the
	 * turn.
	 */
	public abstract void chooseMainPhaseAction();
	
	/**
	 * This method needs to exist so that when the player plays a creature
	 * card that upon entering play the equipment can be attached to the 
	 * creature for free, and the strategy has the opportunity to tell the 
	 * player to do so.
	 * @param equipmentCard The equipment card that the player can attach.
	 */
	public abstract void attachEquipmentToSoldier(Card equipmentCard, Card creatureCard);
	
	/**
	 * This method will be called whenever the player has a choice of which 
	 * mana to spend to play a card.  Most likely this is because the cost of
	 * the card includes one or more colorless mana.
	 */
	public abstract void chooseManaColorToLose();
	
	/**
	 * This method is called whenever the player has the option to gain a mana
	 * of any color, and gives the player one of whichever color mana it thinks
	 * is best for the situation.
	 */
	public abstract void chooseManaColorToGain();
	
	/**
	 * This method looks for a card of the specified type, and moves it to the 
	 * top of the deck.  This entails removing the card from the deck, 
	 * shuffling the deck, and pushing the card back on top.
	 * @param type The type of card that the player may look for and put on 
	 * top.  This should be a type of card such as "Elf", "Kithkin", or 
	 * "Elemental".
	 */
	public abstract void moveCardToTopOfDeck(String type);
	
	/**
	 * This method allows the strategy to put any card from their deck on top
	 * of their deck.  The strategy doesn't get to do this, it has to return
	 * the card that they want on top, and the effect will take care of it.
	 * @param cardType The type of card that the strategy can put on top.  
	 * Every strategy won't have to know how to handle every card type that
	 * could be sent in, but if one is sent in that it doesn't know about, 
	 * throw a runtime exception.
	 * @return The card that the user wants to put on top of the library.
	 */
	public abstract Card putCardOnTop(String cardType);
	
	/**
	 * This allows the strategy to choose from the colors in the choices string
	 * to add one mana of that color to their mana pool.
	 * @param choices A string representing the options the strategy has to add
	 * to their mana pool.  This should be a string of characters containing
	 * only b, g, r, u, and w.
	 * @return A single character representing the color that the strategy 
	 * wants.
	 */
	public abstract String addColorOfChoice(String choices);
	
	/**
	 * Asks the strategy which cards to discard in order to get the player down to their hand size.
	 */
	public abstract void discardToHandSize();
	
	/**
	 * This gives the strategy the opportunity to untap a land of their choice.
	 */
	public abstract void untapLand();

	/**
	 * This gives the strategy the opportunity to add additional resources to the mana pool.
	 *
	 */
	public abstract void updateManaPool();
}
