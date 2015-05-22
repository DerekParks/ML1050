package cards.artifacts;

import cards.creatures.CreatureCard;

public class EquipmentCard extends ArtifactCard {

	CreatureCard myCreature;
	
	public EquipmentCard(String name) {
		super(name);
	}
	
	public void attachCreature(CreatureCard newCreature)
	{
		myCreature = newCreature;
	}
	
	public CreatureCard getAttachedCreature()
	{
		return myCreature;
	}
	
	/**
	 * This method will most likely be called as a result of the creature 
	 * dying, since equipment can't just be "removed" just cause.
	 */
	public void removeCreature()
	{
		myCreature = null;
	}
	
	public boolean isAttached()
	{
		return(myCreature != null);
	}

}
