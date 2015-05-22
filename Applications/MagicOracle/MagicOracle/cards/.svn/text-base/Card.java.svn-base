package cards;

import java.util.Scanner;
import java.util.Vector;

import magic.Player;
import magic.effects.Effect;
import abilities.Ability;
import cards.artifacts.ArtifactCard;
import cards.creatures.CreatureCard;
import cards.enchantments.EnchantmentCard;
import cards.instants.InstantCard;
import cards.sorceries.SorceryCard;

public abstract class Card {

	// These Vectors will hold the list of effects that have to happen when
	// the indicated event happens.
	private Vector<Effect> playEffects;

	private Vector<Effect> leavePlayEffects;

	private Vector<Effect> creatureEntersPlayEffects;

	private Vector<Effect> instantEntersPlayEffects;

	private Vector<Effect> sorceryEntersPlayEffects;

	private Vector<Effect> enchantmentEntersPlayEffects;

	private Vector<Effect> artifactEntersPlayEffects;

	private Vector<Effect> drawEffects;

	private Vector<Effect> opponentDrawEffects;

	private Vector<Effect> attackersChosenEffects;

	private Vector<Ability> activatedAbilities;

	// Keeps track of the number of counters on the card
	private int numCounters = 0;

	public String[] subtypes = new String[2];

	public String name;

	protected boolean inPlay = false;

	protected boolean tapped = false;

	// This is the player that played this card
	protected Player thePlayer;

	public Card(String name) {
		this.name = name;
		playEffects = new Vector<Effect>();
		leavePlayEffects = new Vector<Effect>();
		creatureEntersPlayEffects = new Vector<Effect>();
		instantEntersPlayEffects = new Vector<Effect>();
		sorceryEntersPlayEffects = new Vector<Effect>();
		enchantmentEntersPlayEffects = new Vector<Effect>();
		artifactEntersPlayEffects = new Vector<Effect>();
		drawEffects = new Vector<Effect>();
		opponentDrawEffects = new Vector<Effect>();
		activatedAbilities = new Vector<Ability>();
	}

	public void addPlayEffect(Effect playEffect) {
		playEffects.add(playEffect);
	}

	public void updateSubtype(String newSubtypes) {
		Scanner myScanner = new Scanner(newSubtypes).useDelimiter(" ");
		for (int i = 0; myScanner.hasNext(); i++) {
			subtypes[i] = myScanner.next();
		}
	}

	/**
	 * Updates all of the effects associated with this card to include the
	 * player and card.
	 * 
	 * @param p
	 *            The player who owns this card.
	 */
	public void updateEffects(Player p) {

		thePlayer = p;
		
		for (int i = 0; i < playEffects.size(); i++) {
			playEffects.get(i).setMyCard(this);
			playEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < leavePlayEffects.size(); i++) {
			leavePlayEffects.get(i).setMyCard(this);
			leavePlayEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < creatureEntersPlayEffects.size(); i++) {
			creatureEntersPlayEffects.get(i).setMyCard(this);
			creatureEntersPlayEffects.get(i).setMyPlayer(p);
		}

		for (int i = 0; i < instantEntersPlayEffects.size(); i++) {
			instantEntersPlayEffects.get(i).setMyCard(this);
			instantEntersPlayEffects.get(i).setMyPlayer(p);
		}

		for (int i = 0; i < sorceryEntersPlayEffects.size(); i++) {
			sorceryEntersPlayEffects.get(i).setMyCard(this);
			sorceryEntersPlayEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < enchantmentEntersPlayEffects.size(); i++) {
			enchantmentEntersPlayEffects.get(i).setMyCard(this);
			enchantmentEntersPlayEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < artifactEntersPlayEffects.size(); i++) {
			artifactEntersPlayEffects.get(i).setMyCard(this);
			artifactEntersPlayEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < drawEffects.size(); i++) {
			drawEffects.get(i).setMyCard(this);
			drawEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < opponentDrawEffects.size(); i++) {
			opponentDrawEffects.get(i).setMyCard(this);
			opponentDrawEffects.get(i).setMyPlayer(p);
		}
		for (int i = 0; i < activatedAbilities.size(); i++) {
			activatedAbilities.get(i).setMyCard(this);
			activatedAbilities.get(i).setMyPlayer(p);
			for (int j = 0; j < activatedAbilities.get(i).getEffects().size(); j++) {
				
				activatedAbilities.get(i).getEffects().get(j).setMyCard(this);
				activatedAbilities.get(i).getEffects().get(j).setMyPlayer(p);
			}
		}
	}
	
	public void play() {
		for (int j = 0; j < playEffects.size(); j++) {
			// Use the default executeEffect since the card already knows the
			// player
			playEffects.elementAt(j).executeEffect();
		}
	}

	public void leavePlay() {
		for (int j = 0; j < leavePlayEffects.size(); j++) {
			// Use the default executeEffect since the card already knows the
			// player
			leavePlayEffects.elementAt(j).executeEffect();
		}
	}

	public void addCreatureEntersPlayEffect(Effect theEffect) {
		creatureEntersPlayEffects.add(theEffect);
	}

	public void creatureEntersPlay(CreatureCard c) {
		for (int j = 0; j < creatureEntersPlayEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we need to do
			// something to the creature upon it entering play.
			creatureEntersPlayEffects.elementAt(j).executeEffect(c);
		}
	}

	public void addInstantEntersPlayEffect(Effect theEffect) {
		instantEntersPlayEffects.add(theEffect);
	}

	public void instantEntersPlay(InstantCard i) {
		for (int j = 0; j < instantEntersPlayEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we need to do
			// something to the instant upon it entering play.
			instantEntersPlayEffects.elementAt(j).executeEffect(i);
		}
	}

	public void addSorceryEntersPlayEffect(Effect theEffect) {
		sorceryEntersPlayEffects.add(theEffect);
	}

	public void sorceryEntersPlay(SorceryCard s) {
		for (int j = 0; j < sorceryEntersPlayEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we need to do
			// something to the sorcery upon it entering play.
			sorceryEntersPlayEffects.elementAt(j).executeEffect(s);
		}
	}

	public void addEnchantmentEntersPlayEffect(Effect theEffect) {
		enchantmentEntersPlayEffects.add(theEffect);
	}

	public void enchantmentEntersPlay(EnchantmentCard e) {
		for (int j = 0; j < enchantmentEntersPlayEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we need to do
			// something to the enchantment upon it entering play.
			enchantmentEntersPlayEffects.elementAt(j).executeEffect(e);
		}
	}

	public void addArtifactEntersPlayEffect(Effect theEffect) {
		artifactEntersPlayEffects.add(theEffect);
	}

	public void artifactEntersPlay(ArtifactCard a) {
		for (int j = 0; j < artifactEntersPlayEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we need to do
			// something to the artifact upon it entering play.
			artifactEntersPlayEffects.elementAt(j).executeEffect(a);
		}
	}

	public void addAttackersChosenEffect(Effect theEffect) {
		attackersChosenEffects.add(theEffect);
	}

	/**
	 * This method needs to be called on each card once the player has chosen
	 * what creatures will be attacking.
	 */
	public void attackersChosen() {
		for (int j = 0; j < attackersChosenEffects.size(); j++) {
			// Use the executeEffect without an argument, since there are
			// really no arguments, the player just chose the creatures to
			// attack with.
			attackersChosenEffects.elementAt(j).executeEffect();
		}
	}

	/**
	 * Called whenever the player draws a card, in case the card for any reason
	 * needs to do something when that happens.
	 * 
	 * @param drawCard
	 *            The card that the player drew.
	 */
	public void playerDraw(Card drawCard) {
		for (int j = 0; j < drawEffects.size(); j++) {
			// Use the executeEffect with an argument, in case we care what the
			// player drew, and not just THAT they drew a card.
			drawEffects.elementAt(j).executeEffect(drawCard);

		}
	}

	public void opponentDraw(Card drawCard) {
		for (int j = 0; j < opponentDrawEffects.size(); j++) {
			// If somehow we know what card the opponent drew, most likely that
			// means we care what they drew, so use the executeEffect with a
			// parameter
			if (drawCard != null) {
				opponentDrawEffects.elementAt(j).executeEffect(drawCard);
			}
			// Otherwise use the parameter-less version.
			else {
				opponentDrawEffects.elementAt(j).executeEffect();
			}
		}
	}

	public void tap() {
		tapped = true;
	}

	public void untap() {
		tapped = false;
	}

	public int addCounter() {
		numCounters++;
		return numCounters;
	}

	public int removeCounter() {
		numCounters--;
		return numCounters;
	}

	public void print() {
		System.out.println("My name is: " + name + ", my tapped value is: "
				+ tapped + " and my inPlay value is: " + inPlay);
		System.out.print("I am a: ");
		for (int i = 0; i < subtypes.length; i++) {
			if (subtypes[i] != null)
				System.out.print(subtypes[i] + " ");
		}
		System.out.println(" " + this.toString());
		if (playEffects.size() > 0) {
			System.out.println("I have the following play effects: ");
			for (int i = 0; i < playEffects.size(); i++) {
				System.out.println("\t" + playEffects.get(i));
			}
		}
		if (leavePlayEffects.size() > 0) {
			System.out.println("I have the following leaves play effects: ");
			for (int i = 0; i < leavePlayEffects.size(); i++) {
				System.out.println("\t" + leavePlayEffects.get(i));
			}
		}
		if (creatureEntersPlayEffects.size() > 0) {
			System.out
					.println("I have the following creature enters play effects: ");
			for (int i = 0; i < creatureEntersPlayEffects.size(); i++) {
				System.out.println("\t" + creatureEntersPlayEffects.get(i));
			}
		}
		if (instantEntersPlayEffects.size() > 0) {
			System.out
					.println("I have the following creature enters play effects: ");
			for (int i = 0; i < instantEntersPlayEffects.size(); i++) {
				System.out.println("\t" + instantEntersPlayEffects.get(i));
			}
		}
		if (sorceryEntersPlayEffects.size() > 0) {
			System.out
					.println("I have the following sorcery enters play effects: ");
			for (int i = 0; i < sorceryEntersPlayEffects.size(); i++) {
				System.out.println("\t" + sorceryEntersPlayEffects.get(i));
			}
		}
		if (enchantmentEntersPlayEffects.size() > 0) {
			System.out
					.println("I have the following enchantment enters play effects: ");
			for (int i = 0; i < enchantmentEntersPlayEffects.size(); i++) {
				System.out.println("\t" + enchantmentEntersPlayEffects.get(i));
			}
		}
		if (artifactEntersPlayEffects.size() > 0) {
			System.out
					.println("I have the following artifact enters play effects: ");
			for (int i = 0; i < artifactEntersPlayEffects.size(); i++) {
				System.out.println("\t" + artifactEntersPlayEffects.get(i));
			}
		}
		if (drawEffects.size() > 0) {
			System.out.println("I have the following draw effects: ");
			for (int i = 0; i < drawEffects.size(); i++) {
				System.out.println("\t" + drawEffects.get(i));
			}
		}
		if (opponentDrawEffects.size() > 0) {
			System.out.println("I have the opponent draw effects: ");
			for (int i = 0; i < opponentDrawEffects.size(); i++) {
				System.out.println("\t" + opponentDrawEffects.get(i));
			}
		}
		if (activatedAbilities.size() > 0) {
			System.out.println("I have the following activated abilities: ");
			for (int i = 0; i < activatedAbilities.size(); i++) {
				System.out.println("\t" + activatedAbilities.get(i)
						+ " made of");
				for (int j = 0; j < activatedAbilities.get(i).getEffects()
						.size(); j++) {
					System.out.println("\t\t"
							+ activatedAbilities.get(i).getEffects().get(j));
				}
			}
		}
	}

	public Vector<Ability> getActivatedAbilities() {
		return activatedAbilities;
	}

	public void setActivatedAbilities(Vector<Ability> activatedAbilities) {
		this.activatedAbilities = activatedAbilities;
	}

	public Vector<Effect> getArtifactEntersPlayEffects() {
		return artifactEntersPlayEffects;
	}

	public void setArtifactEntersPlayEffects(
			Vector<Effect> artifactEntersPlayEffects) {
		this.artifactEntersPlayEffects = artifactEntersPlayEffects;
	}

	public Vector<Effect> getCreatureEntersPlayEffects() {
		return creatureEntersPlayEffects;
	}

	public void setCreatureEntersPlayEffects(
			Vector<Effect> creatureEntersPlayEffects) {
		this.creatureEntersPlayEffects = creatureEntersPlayEffects;
	}

	public Vector<Effect> getDrawEffects() {
		return drawEffects;
	}

	public void setDrawEffects(Vector<Effect> drawEffects) {
		this.drawEffects = drawEffects;
	}

	public Vector<Effect> getEnchantmentEntersPlayEffects() {
		return enchantmentEntersPlayEffects;
	}

	public void setEnchantmentEntersPlayEffects(
			Vector<Effect> enchantmentEntersPlayEffects) {
		this.enchantmentEntersPlayEffects = enchantmentEntersPlayEffects;
	}

	public boolean isInPlay() {
		return inPlay;
	}

	public void setInPlay(boolean inPlay) {
		this.inPlay = inPlay;
	}

	public Vector<Effect> getInstantEntersPlayEffects() {
		return instantEntersPlayEffects;
	}

	public void setInstantEntersPlayEffects(
			Vector<Effect> instantEntersPlayEffects) {
		this.instantEntersPlayEffects = instantEntersPlayEffects;
	}

	public Vector<Effect> getLeavePlayEffects() {
		return leavePlayEffects;
	}

	public void setLeavePlayEffects(Vector<Effect> leavePlayEffects) {
		this.leavePlayEffects = leavePlayEffects;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getNumCounters() {
		return numCounters;
	}

	public void setNumCounters(int numCounters) {
		this.numCounters = numCounters;
	}

	public Vector<Effect> getOpponentDrawEffects() {
		return opponentDrawEffects;
	}

	public void setOpponentDrawEffects(Vector<Effect> opponentDrawEffects) {
		this.opponentDrawEffects = opponentDrawEffects;
	}

	public Vector<Effect> getPlayEffects() {
		return playEffects;
	}

	public void setPlayEffects(Vector<Effect> playEffects) {
		this.playEffects = playEffects;
	}

	public Vector<Effect> getSorceryEntersPlayEffects() {
		return sorceryEntersPlayEffects;
	}

	public void setSorceryEntersPlayEffects(
			Vector<Effect> sorceryEntersPlayEffects) {
		this.sorceryEntersPlayEffects = sorceryEntersPlayEffects;
	}

	public String[] getSubtypes() {
		return subtypes;
	}

	public void setSubtypes(String[] subtypes) {
		this.subtypes = subtypes;
	}

	public boolean isTapped() {
		return tapped;
	}

	public void setTapped(boolean tapped) {
		this.tapped = tapped;
	}

	public Player getThePlayer() {
		return thePlayer;
	}

	public void setThePlayer(Player thePlayer) {
		this.thePlayer = thePlayer;
	}
	
	public boolean executeEffect(Effect effect)
	{
		for(int i=0; i<activatedAbilities.size(); i++)
		{
			for(int j=0; j<activatedAbilities.get(i).getEffects().size(); j++)
			{
				if(activatedAbilities.get(i).getEffects().get(j).equals(effect))
				{
					activatedAbilities.get(i).play();
					return true;
				}
			}
		}
		return false;
	}
}
