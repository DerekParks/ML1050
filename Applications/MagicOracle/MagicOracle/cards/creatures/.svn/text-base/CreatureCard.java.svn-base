package cards.creatures;

import java.util.Vector;

import magic.effects.Effect;
import utils.Logger;
import cards.Card;
import cards.artifacts.EquipmentCard;

public class CreatureCard extends Card{
	private int power;
	private int toughness;
	private int currentHealth;
	
	private boolean flying = false;
	private boolean vigilance = false;
	private boolean firstStrike = false;
	private boolean lifelink = false;
	private boolean trample = false;
	private boolean isAttacking = false;
	
	// This will be the list of equipment the creature has attached to it.
	private Vector<EquipmentCard> attachedEquipment;
	// Any effects that have to take place just before this creature takes 
	// damage.
	private Vector<Effect> beforeDamageTakenEffects;
	// Any effects that have to take place just after the creature takes 
	// damage.
	private Vector<Effect> afterDamageTakenEffects;
	
	private Logger log;
	
	/**
	 * Initialized to false due to summoning sickness
	 */
	private boolean canAttack = false;
	
	public CreatureCard(String name, int newPower, int newToughness)
	{
		super(name);
		power = newPower;
		toughness = newToughness;
		currentHealth = toughness;
		attachedEquipment = new Vector<EquipmentCard>();
		log = new Logger("CreatureCard.log", name, 3);
		beforeDamageTakenEffects = new Vector<Effect>();
		afterDamageTakenEffects = new Vector<Effect>();
	}
	
	/**
	 * Checks the current health of the creature (basically toughness minus 
	 * damage taken this turn).  If that value falls to or below zero, the
	 * creature informs its player that it's dead and should be removed from
	 * play.
	 */
	public void checkHealth()
	{
		if(currentHealth <= 0)
		{
			log.print(name + " died!", 2);
			die();
		}
	}
	
	/**
	 * Perform all actions that the creature needs to do in order to die.  ie
	 * remove itself from the player's control, remove all equipment from 
	 * itself, etc
	 */
	public void die()
	{
		for(int i=0; i<attachedEquipment.size(); i++)
		{
			attachedEquipment.elementAt(i).removeCreature();
		}
		attachedEquipment.removeAllElements();
		thePlayer.removeCreatureInPlay(this);		
	}
	
	/**
	 * Changes the power by an amount specified in the parameter.
	 * @param changeAmount The amount that the power should change by.  This 
	 * value can be positive or negative, and CAN drop the power below zero.
	 */
	public void changePower(int changeAmount)
	{
		power += changeAmount;
	}
	
	/**
	 * Adds or subtracts from the toughness based on the parameter sent in
	 * @param changeAmount The amount that the toughness should change by.  
	 * This value can be positive or negative.  This function then modifies the
	 * currentHealth variable through a call to changeCurrentHealth.
	 */
	public void changeToughness(int changeAmount)
	{
		toughness += changeAmount;
		changeCurrentHealth(changeAmount);
	}
	
	/**
	 * Adds or subtracts from the current health based on the parameter sent 
	 * in.The currentHealth variable is then sent to checkHealth to determine 
	 * if this change causes the creature to die.
	 * @param changeAmount The amount that the health is going to change by.  
	 * This value can be positive or negative depending on whether the creature
	 * is being hurt or "healed", but most likely would always be negative.  
	 * The resetHealth function takes care of the healing each turn.
	 */
	public void changeCurrentHealth(int changeAmount)
	{
		currentHealth += changeAmount;
		checkHealth();
	}
	
	/**
	 * This function would most likely be called at the end of a turn, and is
	 * called to remove all damage that the creature took this turn by 
	 * resetting the current health to the toughness;
	 */
	public void resetHealth()
	{
		currentHealth = toughness;
	}

	public boolean isFirstStrike() {
		return firstStrike;
	}

	public void setFirstStrike(boolean firstStrike) {
		this.firstStrike = firstStrike;
	}

	public boolean isTrample() {
		return trample;
	}

	public void setTrample(boolean trample) {
		this.trample = trample;
	}

	public boolean isFlying() {
		return flying;
	}

	public void setFlying(boolean flying) {
		this.flying = flying;
	}

	public boolean isLifelink() {
		return lifelink;
	}

	public void setLifelink(boolean lifelink) {
		this.lifelink = lifelink;
	}

	public int getToughness() {
		return toughness;
	}

	public void setToughness(int toughness) {
		this.toughness = toughness;
	}

	public boolean isVigilance() {
		return vigilance;
	}

	public void setVigilance(boolean vigilance) {
		this.vigilance = vigilance;
	}

	/**
	 * @return the isAttacking
	 */
	public boolean isAttacking() {
		return isAttacking;
	}

	/**
	 * @param isAttacking setting whether or not the creature is currently
	 * attacking.
	 */
	public void setAttacking(boolean isAttacking) {
		this.isAttacking = isAttacking;
	}
	
	/**
	 * This method should only be called if the creature doesn't already have
	 * this piece of equipment on them.  If this equipment is attached to 
	 * another creature, this method will first remove it from that creature.
	 * @param newEquipment The new equipment to put on the creature
	 */
	public void attachEquipment(EquipmentCard newEquipment)
	{
		// First check if it's already attached to someone
		if(newEquipment.isAttached())
		{
			newEquipment.getAttachedCreature().removeEquipment(newEquipment);
		}
		attachedEquipment.add(newEquipment);
	}
	
	/**
	 * This method should only be called to move the equipment to another 
	 * creature.  Simply removing the equipment onto nothing is against the 
	 * rules
	 * @param theEquipment The equipment this creature is having removed off 
	 * of it.
	 */
	public void removeEquipment(EquipmentCard theEquipment)
	{
		attachedEquipment.remove(theEquipment);
	}
	
	public int getPower() {
		return power;
	}
	
	public void addBeforeDamageTakenEffect(Effect theEffect)
	{
		beforeDamageTakenEffects.add(theEffect);
	}
	
	public void addAfterDamageTakenEffect(Effect theEffect)
	{
		afterDamageTakenEffects.add(theEffect);
	}
	
	public void takeDamage(int damageToTake)
	{
		for(int i=0; i<beforeDamageTakenEffects.size(); i++)
		{
			beforeDamageTakenEffects.elementAt(i).executeEffect(damageToTake);
		}
		changeCurrentHealth(-1*damageToTake);
		for(int i=0; i<afterDamageTakenEffects.size(); i++)
		{
			afterDamageTakenEffects.elementAt(i).executeEffect(damageToTake);
		}
	}

	public boolean isCanAttack() {
		return canAttack;
	}

	public void setCanAttack(boolean canAttack) {
		this.canAttack = canAttack;
	}
}
