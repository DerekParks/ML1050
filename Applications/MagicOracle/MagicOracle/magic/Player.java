package magic;

import java.util.Vector;

import magic.effects.AddBlackEffect;
import magic.effects.AddGreenEffect;
import magic.effects.AddWhiteEffect;
import magic.effects.Effect;
import mana.Mana;
import statistics.Statistics;
import strategy.Strategy;
import utils.Logger;
import abilities.Ability;
import cards.Card;
import cards.artifacts.ArtifactCard;
import cards.creatures.CreatureCard;
import cards.enchantments.EnchantmentCard;
import cards.lands.LandCard;
import cards.planeswalkers.PlaneswalkerCard;
import decks.Deck;
import exceptions.LoseGameException;

public class Player {

	Player myOpponent;

	// Used for logging purposes.
	private String name;

	Statistics scoreKeeper;

	private int myLife;

	private int handsize = 7;

	private boolean draw;

	private Vector<LandCard> landsInPlay;

	private Vector<CreatureCard> creaturesInPlay;

	private Vector<PlaneswalkerCard> planeswalkersInPlay;

	private Vector<EnchantmentCard> enchantmentsInPlay;

	private Vector<ArtifactCard> artifactsInPlay;

	private Vector<CreatureCard> attackingCreatures;

	private Deck library;

	private Vector<Card> hand;

	private Vector<Effect> upkeepEffects;

	private Vector<Effect> endOfTurnEffects;

	// Variables to keep track of what has happened so far this turn

	private boolean hasPlayedLand;

	private boolean hasAttacked;

	// The brains of the whole operation, each player has a strategy.

	private Strategy myStrategy;

	private String deckLocation;

	// The log. Used for debug purposes.
	private Logger log;

	private Mana availableLands;

	private Mana manaPool;

	/**
	 * This creates a new player based on the parameters that were sent in. This
	 * player does not need to be created new for every game, it is capable of
	 * cleaning up and starting a new game each time.
	 * 
	 * @param deckLocation
	 *            should contain the location of the XML file used to build the
	 *            deck.
	 * @param fileName
	 *            The name of the output file that the statistics will be
	 *            written to. Make sure this file is either writeable, or if it
	 *            is being created new, that the directory is writeable.
	 * @throws LoseGameException
	 */
	Player(String deckLocation, String fileName, String name) {
		this.name = name;
		// Create the log
		log = new Logger(name + ".log", name, 3);
		// Initialize vectors
		scoreKeeper = new Statistics(fileName);
		this.deckLocation = deckLocation;

	}

	/**
	 * We can't send in the opponents for each Player until we've created both
	 * players, so we have to define a separate method to set the opponent once
	 * both players have been created.
	 * 
	 * @param theOpponent
	 *            This should be a valid (not null) Player, that has already
	 *            been "new"'ed.
	 */
	public void setOpponent(Player theOpponent) {
		myOpponent = theOpponent;
	}

	/**
	 * Controls the phases of the game. The phases are as follows: 1) Untap 2)
	 * Upkeep 3) Draw 4) First Main Phase 5) Combat a) Beginning of Combat b)
	 * Attack c) Block d) Damage e) End of Combat 6) Second Main Phase 7) End of
	 * Turn effects 8) Discard
	 * 
	 * @throws LoseGameException
	 */
	public void playTurn() throws LoseGameException {
		log.print("Starting my turn", 1);
		try {
			untapAllPermanents();
			createManaPool();
			upkeep();
			draw();
			mainPhase();
			preCombat();
			attack();
			postCombat();
			mainPhase();
			endTurn();
		} catch (LoseGameException e) {
			throw e;
		}
	}

	private void preCombat() {
		log.print("Starting my precombat phase.", 1);
		// TODO: Precombat still needs to be implemented.
	}

	private void postCombat() {
		log.print("Starting my postcombat phase.", 3);
		// TODO: Postcombat still needs to be implemented.
	}

	/**
	 * Should only be called by the active player. This asks the strategy which
	 * creatures should attack and then declares these to the defenders.
	 * 
	 * @throws LoseGameException
	 * 
	 */
	private void attack() throws LoseGameException {
		log.print("Attacking.", 1);
		attackingCreatures = myStrategy.chooseAttackers();
		myOpponent.defend(attackingCreatures);
		attackingCreatures.removeAllElements();
	}

	/**
	 * Should only be called on the defender. This calls the strategy to ask
	 * which creatures should defend.
	 * 
	 * @param attackers
	 * @throws LoseGameException
	 */
	public void defend(Vector<CreatureCard> attackers) throws LoseGameException {
		log.print("Defending.", 1);
		myOpponent.calculateCombatDamage(attackers, myStrategy
				.chooseDefenders(attackers));
	}

	/**
	 * Calculates all combat damage. This should only be called once the
	 * attackers and defenders have been chosen and should be called on the
	 * attacker (since they should determine where the damage should be
	 * assigned). Therefore neither the attackers nor the blockers should be
	 * null. The first location in the blockers vector corresponds to the
	 * blockers that will block the attacker in the first location.
	 * 
	 * @param attackers
	 *            The attackers in this combat phase.
	 * @param blockers
	 *            The blockers in this combat phase.
	 * @throws LoseGameException
	 */
	public void calculateCombatDamage(Vector<CreatureCard> attackers,
			Vector<Vector<CreatureCard>> blockers) throws LoseGameException {
		for (int i = 0; i < blockers.size(); i++) {
			log.print("Attacker: " + attackers.get(i).getName(), 2);
			for (int j = 0; j < blockers.get(i).size(); j++) {
				log.print("/tBlocker:" + blockers.get(i).get(j).getName(), 2);
			}
		}
		myStrategy.assignDamage(attackers, blockers);
		int totalDamage = 0;
		for (int i = 0; i < attackers.size(); i++) {
			totalDamage += attackers.get(i).getPower();
			myOpponent.changeLife(-attackers.get(i).getPower());
		}
		log.print(name + " dealt " + totalDamage + " combat damage to "
				+ myOpponent.name, 2);
	}

	public void untapAllPermanents() {
		log.print("Untapping my creatures.", 1);
		for (int i = 0; i < creaturesInPlay.size(); i++) {
			creaturesInPlay.get(i).untap();
			// Summoning sickness is removed for all creatures
			creaturesInPlay.get(i).setCanAttack(true);
		}
		log.print("Untapping my enchantments.", 1);
		for (int i = 0; i < enchantmentsInPlay.size(); i++) {
			enchantmentsInPlay.get(i).untap();
		}
		log.print("Untapping my lands.", 1);
		for (int i = 0; i < landsInPlay.size(); i++) {
			landsInPlay.get(i).untap();
		}
		log.print("Untapping my artifacts.", 1);
		for (int i = 0; i < artifactsInPlay.size(); i++) {
			artifactsInPlay.get(i).untap();
		}
	}

	public void mainPhase() {
		log.print("Starting my main phase.", 1);

		myStrategy.chooseMainPhaseAction();

		// This will contact the strategy to see what needs to occur during this
		// phase.
	}

	public Vector<Ability> createAbilities() {
		Vector<Ability> abilities = new Vector<Ability>();
		for (int i = 0; i < creaturesInPlay.size(); i++) {
			for (int j = 0; j < creaturesInPlay.get(i).getActivatedAbilities()
					.size(); j++) {
				abilities.add(creaturesInPlay.get(i).getActivatedAbilities()
						.get(j));
			}
		}
		for (int i = 0; i < landsInPlay.size(); i++) {
			for (int j = 0; j < landsInPlay.get(i).getActivatedAbilities()
					.size(); j++) {
				abilities
						.add(landsInPlay.get(i).getActivatedAbilities().get(j));
			}
		}
		for (int i = 0; i < enchantmentsInPlay.size(); i++) {
			for (int j = 0; j < enchantmentsInPlay.get(i)
					.getActivatedAbilities().size(); j++) {
				abilities.add(enchantmentsInPlay.get(i).getActivatedAbilities()
						.get(j));
			}
		}
		for (int i = 0; i < artifactsInPlay.size(); i++) {
			for (int j = 0; j < artifactsInPlay.get(i).getActivatedAbilities()
					.size(); j++) {
				abilities.add(artifactsInPlay.get(i).getActivatedAbilities()
						.get(j));
			}
		}
		return abilities;
	}

	public void upkeep() {
		log.print("Starting my upkeep.", 1);
		for (int i = 0; i < upkeepEffects.size(); i++) {
			upkeepEffects.get(i).executeEffect();
		}
		hasPlayedLand = false;

	}

	public void endTurn() {
		log.print("Running my end of turn effects.", 1);
		// TODO: losing all mana, resetting
		// damage on creatures, and anything else we can think of.
		for (int i = 0; i < endOfTurnEffects.size(); i++) {
			endOfTurnEffects.elementAt(i).executeEffect();
		}
		if (hand.size() > handsize) {
			myStrategy.discardToHandSize();
		}
	}

	public int getLife() {
		return myLife;
	}

	/**
	 * 
	 * @param change
	 *            The change in the player's life. This can be a positive or
	 *            negative quantity depending on whether the player is gaining
	 *            or losing life.
	 * @throws LoseGameException
	 */
	public void changeLife(int change) throws LoseGameException {
		myLife += change;
		if (myLife <= 0) {
			throw new LoseGameException(name
					+ " had their life decreased below 0 and lost the game");
		}
	}

	public void discard(Card cardToDiscard) {
		boolean discarded = false;
		for (int i = 0; !discarded && i < hand.size(); i++) {
			if (hand.get(i).getName().equals(cardToDiscard.getName())) {
				hand.remove(i);
				discarded = true;
			}
		}
	}

	/**
	 * This adds a land card to the player's "in play" area, based on the Card
	 * that was sent in.
	 * 
	 * @param theLand
	 *            The card that the player will put into play under their
	 *            control.
	 */
	public void addLand(LandCard theLand) {
		landsInPlay.add(theLand);
	}

	public Vector<LandCard> getLandsInPlay() {
		return landsInPlay;
	}

	/**
	 * Attempts to remove the specified land from play under the player's
	 * control, and returns whether it was able to do so.
	 * 
	 * @param theLand
	 *            The land that is being removed from play
	 * @return Whether the land was actually able to be removed. If it couldn't
	 *         be removed, most likely the land didn't exist under the user's
	 *         control in the first place.
	 */
	public boolean removeLandInPlay(LandCard theLand) {
		return landsInPlay.remove(theLand);
	}

	/**
	 * This adds a creature card into the player's "in play" area, based on the
	 * Card that was sent in.
	 * 
	 * @param theCreature
	 *            The creature that the player will be putting into play.
	 */
	public void addCreatureInPlay(CreatureCard theCreature) {
		// TODO: Call creatureEntersPlay on each card in play
		creaturesInPlay.add(theCreature);
	}

	public Vector<CreatureCard> getCreaturesInPlay() {
		return creaturesInPlay;
	}

	/**
	 * This removes the given creature from play (probably by dying), by
	 * removing the creature from the creaturesInPlay vector
	 * 
	 * @param theCreature
	 *            The creature being removed from play
	 * @return Whether the creature was able to be removed from play. If it
	 *         wasn't able to be removed, most likely this was not a creature
	 *         the player had in play.
	 */
	public boolean removeCreatureInPlay(CreatureCard theCreature) {
		return creaturesInPlay.remove(theCreature);
	}

	/**
	 * This adds a planeswalker card into the player's "in play" area, based on
	 * the Card that was sent in.
	 * 
	 * @param theCreature
	 *            The creature that the player will be putting into play.
	 */
	public void addPlaneswalkerInPlay(PlaneswalkerCard theCreature) {
		// TODO: Call creatureEntersPlay on each card in play
		planeswalkersInPlay.add(theCreature);
	}

	public Vector<PlaneswalkerCard> getPlaneswalkersInPlay() {
		return planeswalkersInPlay;
	}

	/**
	 * This removes the given planeswalker from play (probably by dying), by
	 * removing the planeswalker from the planeswalkersInPlay vector
	 * 
	 * @param thePlaneswalker
	 *            The planeswalker being removed from play
	 * @return Whether the planeswalker was able to be removed from play. If it
	 *         wasn't able to be removed, most likely this was not a
	 *         planeswalker the player had in play.
	 */
	public boolean removePlaneswalkerInPlay(PlaneswalkerCard thePlaneswalker) {
		return planeswalkersInPlay.remove(thePlaneswalker);
	}

	/**
	 * This adds an enchantment card into the player's "in play" area, based on
	 * the Card that was sent in.
	 * 
	 * @param theEnchantment
	 *            The enchantment that the player will be putting into play.
	 */
	public void addEnchantmentInPlay(EnchantmentCard theEnchantment) {
		// TODO: Call enchantmentEntersPlay on each card in play
		enchantmentsInPlay.add(theEnchantment);
	}

	public Vector<EnchantmentCard> getEnchantmentsInPlay() {
		return enchantmentsInPlay;
	}

	/**
	 * This removes the given enchantment from play (was probably destroyed) by
	 * removing the enchantment from the enchantmentsInPlay vector
	 * 
	 * @param theEnchantment
	 *            The enchantment being removed from play
	 * @return Whether the enchantment was able to be removed from play. If it
	 *         wasn't able to be removed, most likely this was not an
	 *         enchantment the player had in play.
	 */
	public boolean removeEnchantmentInPlay(EnchantmentCard theEnchantment) {
		return enchantmentsInPlay.remove(theEnchantment);
	}

	/**
	 * This adds an artifact card into the player's "in play" area, based on the
	 * Card that was sent in.
	 * 
	 * @param theArtifact
	 *            The artifact that the player will be putting into play.
	 */
	public void addArtifactInPlay(ArtifactCard theArtifact) {
		// TODO: Call artifactEntersPlay on each card in play
		artifactsInPlay.add(theArtifact);
	}

	public Vector<ArtifactCard> getArtifactsInPlay() {
		return artifactsInPlay;
	}

	/**
	 * This removes the given artifact from play (was probably destroyed) by
	 * removing the artifact from the artifactsInPlay vector
	 * 
	 * @param theArtifact
	 *            The artifact being removed from play
	 * @return Whether the artifact was able to be removed from play. If it
	 *         wasn't able to be removed, most likely this was not an artifact
	 *         the player had in play.
	 */
	public boolean removeArtifactInPlay(ArtifactCard theArtifact) {
		return artifactsInPlay.remove(theArtifact);
	}

	// TODO: Add a function that gets called when an instant gets played to
	// call instantEntersPlay on each card in play.
	// TODO: Add a function that gets called when a sorcery gets played to
	// call sorceryEntersPlay on each card in play.

	/**
	 * This adds an effect card into the player's endOfTurnEffects vector, based
	 * on the Effect that was sent in.
	 * 
	 * @param theEffect
	 *            The effect that will take place at the end of turn.
	 */
	public void addEndOfTurnEffect(Effect theEffect) {
		endOfTurnEffects.add(theEffect);
	}

	public Vector<Effect> getEndOfTurnEffects() {
		return endOfTurnEffects;
	}

	/**
	 * Removes a single end of turn effect from the endOfTurnEffects vector,
	 * returning whether it was able to do so or not.
	 * 
	 * @param theEffect
	 *            The effect that we want removed from the vector. Typically
	 *            this should be an effect that has already been executed
	 * @return Whether the effect could be removed. If it returns false, the
	 *         effect didn't exist in the endOfTurnEffects vector.
	 */
	public boolean removeEndOfTurnEffect(Effect theEffect) {
		return endOfTurnEffects.remove(theEffect);
	}

	/**
	 * Removes all end of turn effects from the endOfTurnEffects vector. This
	 * should typically be called at the end of the turn once all those effects
	 * have been executed.
	 */
	public void removeAllEndOfTurnEffects() {
		endOfTurnEffects.removeAllElements();
	}

	/**
	 * This function needs to ask the strategy what color it should use for the
	 * colorless mana it needs to spend. Then it spends that mana.
	 */
	public void useColorless() {
		myStrategy.chooseManaColorToLose();
	}

	/**
	 * Draws the top card from the library and adds it to the hand.
	 * 
	 * @throws LoseGameException
	 * 
	 */
	public void draw() throws LoseGameException {
		if (draw)
			try {
				log.print("Drawing...", 1);
				hand.add(library.draw());
			} catch (LoseGameException e) {
				throw new LoseGameException(name
						+ " tried to draw a card and couldn't. " + name
						+ " lost the game!");
			}
		else
			draw = true;
	}

	/**
	 * Calls shuffle on the library.
	 * 
	 */
	public void shuffle() {
		log.print("Shuffling...", 1);
		library.shuffle();
	}

	/**
	 * Resets the player to prepare for a new game. The player no longer has any
	 * permanents, their life is set to 20, their deck is reset, and they draw
	 * their first 7 cards.
	 * 
	 */
	public void reset() {
		draw = true;
		landsInPlay = new Vector<LandCard>();
		creaturesInPlay = new Vector<CreatureCard>();
		enchantmentsInPlay = new Vector<EnchantmentCard>();
		artifactsInPlay = new Vector<ArtifactCard>();
		planeswalkersInPlay = new Vector<PlaneswalkerCard>();
		endOfTurnEffects = new Vector<Effect>();
		upkeepEffects = new Vector<Effect>();
		// Create deck from the XML file and using the player to build the
		// effects.
		library = new Deck(deckLocation, this);
		// Shuffle deck (new game is starting)
		shuffle();
		hand = new Vector<Card>();
		myLife = 20;
		// Draws the first 7 cards
		for (int i = 0; i < 7; i++) {
			try {
				draw();
			} catch (LoseGameException e) {
				System.out.println(name + " was initialized incorrectly");
			}
		}

	}

	// TODO: Add the attack function. Remember in this function to call
	// attackersChosen on each of the cards in play once the attackers have
	// been chosen. Then call defend on the opponent.
	// TODO: Add the defend function

	public void setDraw(boolean draw) {
		this.draw = draw;
	}

	/**
	 * @return Whether the player has played a land yet this turn
	 */
	public boolean isHasPlayedLand() {
		return hasPlayedLand;
	}

	/**
	 * @param hasPlayedLand
	 *            Whether the player has played a land yet this turn
	 */
	public void setHasPlayedLand(boolean hasPlayedLand) {
		this.hasPlayedLand = hasPlayedLand;
	}

	/**
	 * @return the Whether the player has attacked yet this turn
	 */
	public boolean isHasAttacked() {
		return hasAttacked;
	}

	/**
	 * @param hasAttacked
	 *            Whether the player has attacked yet this turn
	 */
	public void setHasAttacked(boolean hasAttacked) {
		this.hasAttacked = hasAttacked;
	}

	/**
	 * @return the Strategy the player is currently using.
	 */
	public Strategy getStrategy() {
		return myStrategy;
	}

	/**
	 * @param myStrategy
	 *            the new Strategy.
	 */
	public void setStrategy(Strategy newStrategy) {
		myStrategy = newStrategy;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getName() {
		return name;
	}

	public int getMyLife() {
		return myLife;
	}

	public void setMyLife(int myLife) {
		this.myLife = myLife;
	}

	public Mana createAvailableLands() {
		availableLands = new Mana();
		for (int i = 0; i < landsInPlay.size(); i++) {
			LandCard nextLand = landsInPlay.get(i);
			if (!nextLand.isTapped()) {
				if (nextLand.canProduceBlack()) {
					availableLands.incrementBlack();
				}
				if (nextLand.canProduceBlue()) {
					availableLands.incrementBlue();
				}
				if (nextLand.canProduceGreen()) {
					availableLands.incrementGreen();
				}
				if (nextLand.canProduceRed()) {
					availableLands.incrementRed();
				}
				if (nextLand.canProduceWhite()) {
					availableLands.incrementWhite();
				}
			}
		}
		return availableLands;
	}

	public void print() {
		log.print(("========================="), 3);
		log.print(("My name is: " + name), 3);
		log.print("My hand is: ", 3);
		for (int i = 0; i < hand.size(); i++)
			log.print("\t" + hand.get(i).name, 3);
		log.print("My land is: ", 3);
		manaPool.print();
		log.print("My life is: " + myLife, 3);
		log.print("I have the following Creatures in play: ", 3);
		for (int i = 0; i < creaturesInPlay.size(); i++) {
			log.print("\t" + creaturesInPlay.get(i).name + "("
					+ creaturesInPlay.get(i).getPower() + ","
					+ creaturesInPlay.get(i).getToughness() + ")", 3);
		}
		log.print("And the following Artifacts in play: ", 3);
		for (int i = 0; i < artifactsInPlay.size(); i++) {
			log
					.print("\t" + artifactsInPlay.get(i).name + " with "
							+ artifactsInPlay.get(i).getNumCounters()
							+ " counters.", 3);
		}
		log.print("And the following Enchantments in play: ", 3);
		for (int i = 0; i < enchantmentsInPlay.size(); i++) {
			log.print(
					"\t" + enchantmentsInPlay.get(i).name + " with "
							+ enchantmentsInPlay.get(i).getNumCounters()
							+ " counters.", 3);
		}

		log.print(("========================="), 3);
	}

	public Vector<Card> getHand() {
		return hand;
	}

	public void setHand(Vector<Card> hand) {
		this.hand = hand;
	}

	public int getHandsize() {
		return handsize;
	}

	public void setHandsize(int handsize) {
		this.handsize = handsize;
	}

	public void shuffleCardIntoLibrary(Card theCard) {
		library.putCardOnTop(theCard);
		library.shuffle();
	}

	public Vector<CreatureCard> getAttackingCreatures() {
		return attackingCreatures;
	}

	public void addAttackingCreature(CreatureCard attackingCreature) {
		this.attackingCreatures.add(attackingCreature);
	}

	public boolean tapColor(String color) {
		Effect manaEffect;
		if (color.equalsIgnoreCase("white")) {
			manaEffect = new AddWhiteEffect();
		} else if (color.equalsIgnoreCase("black")) {
			manaEffect = new AddBlackEffect();
		} else if (color.equalsIgnoreCase("green")) {
			manaEffect = new AddGreenEffect();
		} else {
			log.print("Attempted to tap invalid mana type", 3);
			return false;
		}
		for (int i = 0; i < landsInPlay.size(); i++) {
			if (landsInPlay.get(i).executeEffect(manaEffect)) {
				return true;
			}
		}
		for (int i = 0; i < creaturesInPlay.size(); i++) {
			if (creaturesInPlay.get(i).executeEffect(manaEffect)) {
				return true;
			}
		}
		return false;
	}

	/**
	 * Initializes the mana pool and updates it with the available lands
	 * 
	 */
	public void createManaPool() {
		manaPool = new Mana();
		updateManaPool();
	}

	/**
	 * Updates the mana pool with currently untapped lands. Then asks the
	 * strategy if it would like to tap any additional lands.
	 * 
	 * @return
	 */
	public void updateManaPool() {
		// Get the available lands
		Mana newPool = createAvailableLands();

		// Tap all of the lands
		for (int i = 0; i < landsInPlay.size(); i++) {
			landsInPlay.get(i).tap();
		}
		// and add them to the mana pool
		manaPool.add(newPool);
		// Ask the strategy if it would like to tap any additional resources to
		// add to the mana pool
		myStrategy.updateManaPool();
		manaPool.print();
	}

	public Mana getManaPool() {
		return manaPool;
	}

	public void setManaPool(Mana manaPool) {
		this.manaPool = manaPool;
	}

}
