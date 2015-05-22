package magic.effects;

import magic.Player;
import cards.Card;

/**
 * It is very very very very important that after the default constructor, the
 * setters for the member variables are called, since almost every effect that
 * extends this class assumes that those variables are set.
 * @author Brandon
 *
 */
public abstract class Effect {
	
	protected Card myCard;
	protected Player myPlayer;
	
	public Effect()
	{
	}
	
	/**
	 * I don't think this will ever really get called, since we'll be using
	 * a dynamic class loader, which is only capable of the default constructor
	 * @param theCard
	 * @param thePlayer
	 */
	public Effect(Card theCard, Player thePlayer)
	{
		myCard = theCard;
		myPlayer = thePlayer;
	}
	
	/**
	 * This has to define two executeEffect functions, since the card that is 
	 * being passed in is sometimes known upon creation of the effect, and is
	 * sometimes only known when the effect is executed.  An example of this
	 * contrast is a creature that needs to get -1/-1 at end of turn, compared
	 * to something that triggers upon a creature coming into play.  The former
	 * knows the card upon creation of the effect, and has no good way of 
	 * getting it later, and the latter dosen't know what card is coming into
	 * play until the card actually comes in.
	 * 
	 * How to use these functions is up to the implementor, just use the method
	 * that is appropriate for the situation.  Most of the time the default
	 * method call to executeEffect() will be sufficient.
	 */
	
	/**
	 * This method should be called for things that upon creation already know
	 * what the card and player they are to be executed on are.  Examples of 
	 * this are "At end of turn this creature gets -1/-1".  The creature card
	 * is already known in the constructor.
	 */
	abstract public void executeEffect();
	
	/**
	 * This method should be called for things that don't know what they will 
	 * be having upon creation.  An example of this is "Every time a new 
	 * creature enters play, deal 2 damage to it".  The creature card is only
	 * known when the effect actually takes place.  This will use the card
	 * passed in instead of the card that was given in the constructor.  
	 * Another example is when something happens when the creature takes 
	 * damage, but depends on how much damage the creature took.  The creature
	 * needs to have passed into it the amount of damage it took.
	 * @param theObject This is used to pass any additional information that 
	 * the card needs.  This will usually be a card, but will be specified in
	 * the individual effect.
	 */
	abstract public void executeEffect(Object theObject);

	/**
	 * @return the myCard
	 */
	public Card getMyCard() {
		return myCard;
	}

	/**
	 * @return the myPlayer
	 */
	public Player getMyPlayer() {
		return myPlayer;
	}

	/**
	 * @param myCard the myCard to set
	 */
	public void setMyCard(Card myCard) {
		this.myCard = myCard;
	}

	/**
	 * @param myPlayer the myPlayer to set
	 */
	public void setMyPlayer(Player myPlayer) {
		this.myPlayer = myPlayer;
	}

}
