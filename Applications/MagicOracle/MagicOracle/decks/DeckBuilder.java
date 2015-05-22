package decks;

import java.util.Scanner;
import java.util.Stack;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import magic.Player;
import magic.costs.Cost;
import magic.effects.Effect;
import mana.AbilityCost;

import org.xml.sax.Attributes;
import org.xml.sax.ContentHandler;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

import abilities.Ability;
import cards.Card;
import cards.artifacts.ArtifactCard;
import cards.creatures.CreatureCard;
import cards.enchantments.EnchantmentCard;
import cards.instants.InstantCard;
import cards.lands.LandCard;
import cards.planeswalkers.PlaneswalkerCard;
import cards.sorceries.SorceryCard;

public class DeckBuilder extends DefaultHandler implements ContentHandler {

	/**
	 * Holds the filename of the deck to read
	 */
	private String fileName;

	/**
	 * The deck that will be returned
	 */
	private Stack<Card> deck = new Stack<Card>();

	/**
	 * The cards to be added to the deck
	 */
	private Card[] nextCards;

	/**
	 * The ability to be added to the cards
	 */
	private Ability nextAbility;

	/**
	 * The name of the deck
	 */
	private String deckName;

	/**
	 * The player the deck is being built for.
	 */
	private Player player;

	/**
	 * Constructor
	 * 
	 * @param fileName
	 *            The file name of the XML file to parse
	 * @param p
	 *            The player the deck is being built for.
	 */
	public DeckBuilder(String fileName, Player p) {
		this.fileName = fileName;
		this.player = p;

	}

	/**
	 * Builds an XML reader to parse the XML file with
	 * 
	 * @return The new XML reader
	 * @throws Exception
	 *             If the parser could not be created for whatever reason
	 */
	public XMLReader makeXMLReader() throws Exception {
		SAXParserFactory spf = SAXParserFactory.newInstance();
		SAXParser sp = spf.newSAXParser();
		return sp.getXMLReader();

	}

	/**
	 * Parses through the file until the deck has been built.
	 * 
	 * @return The built deck
	 */
	public Stack<Card> buildDeck() {
		try {
			// Create a reader to read the XML file
			XMLReader reader = makeXMLReader();
			// Set the content handler to the reader to be this file (see
			// startElement & endElement)
			reader.setContentHandler(this);
			// Parse the file
			reader.parse(fileName);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// Update the effects found in the deck to include the player and card.
		for (int i = 0; i < deck.size(); i++) {
			deck.get(i).updateEffects(player);
		}

		// Return the deck
		return deck;
	}

	/**
	 * Creates a new instance of an effect given the name.
	 * 
	 * @param name
	 *            The name of the effect
	 * @return The new effect.
	 */
	public Effect buildEffect(String name) {
		try {
			// The package needs to be specified as part of the name and
			// "Effect" needs to be appended onto the end of it.
			return (Effect) (Class.forName("magic.effects." + name + "Effect")
					.newInstance());
		} catch (InstantiationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}

	/**
	 * This is part of the content handler. Everytime a tag is started in the
	 * XML file, this method is called.
	 */
	public void startElement(String uri, String localname, String type,
			Attributes atts) {
		// If the tag was "card" then create the nextCards array holding the
		// given number of that card
		if (type.equalsIgnoreCase("card")) {
			nextCards = createCards(atts);
		} else if (type.equalsIgnoreCase("ability")) {
			// If the tag was "ability" then create a new ability that will have
			// effects appended onto it
			nextAbility = new Ability();
			nextAbility.setType(atts.getValue("type"));
			nextAbility.setName(atts.getValue("name"));
		} else if (type.equalsIgnoreCase("cost")) {
			nextAbility.setCost(buildCost(atts));
		} else if (type.equalsIgnoreCase("effect")) {
			// If the tag was "effect" then build the effect and add it onto the
			// ability
			nextAbility.getEffects().add(buildEffect(atts.getValue("name")));
		} else if (type.equalsIgnoreCase("staticAbilities")) {
			buildStaticAbilities(atts.getValue("name"));
		} else if (type.equalsIgnoreCase("deck")) {
			deckName = atts.getValue("name");
		}
	}

	private AbilityCost buildCost(Attributes atts) {
		char[] costArray = atts.getValue("value").toCharArray();
		String subCost = atts.getValue("additionalCosts");
		AbilityCost cost = new AbilityCost();
		for (int i = 0; i < costArray.length; i++) {
			if (costArray[i] == 'r') {
				cost.getCost().incrementRed();
			} else if (costArray[i] == 'u') {
				cost.getCost().incrementBlue();
			} else if (costArray[i] == 'b') {
				cost.getCost().incrementBlack();
			} else if (costArray[i] == 'g') {
				cost.getCost().incrementGreen();
			} else if (costArray[i] == 'w') {
				cost.getCost().incrementWhite();
			} else if (costArray[i] == 'c') {
				cost.getCost().incrementColorless();
			}

		}
		if (subCost != null) {
			Scanner myScanner = new Scanner(subCost).useDelimiter(",");
			while (myScanner.hasNext()) {
				String additionalCost = myScanner.next();
				try {
					if(!additionalCost.equals(""))
						cost.addCost(((Cost) (Class.forName("magic.costs."
							+ additionalCost + "Cost")).newInstance()));
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
		return cost;
	}

	/**
	 * Builds static abilities for the creatures
	 * 
	 * @param abilities
	 *            The comma delimited group of static abilities.
	 */
	private void buildStaticAbilities(String abilities) {
		// Create a scanner with a "," as the delimiter. This is used to parse
		// the static abilities field of the XML file.
		Scanner abilityScanner = new Scanner(abilities).useDelimiter(",");
		while (abilityScanner.hasNext()) {
			String nextAbility = abilityScanner.next();
			if (nextAbility.equalsIgnoreCase("lifelink")) {
				for (int i = 0; i < nextCards.length; i++) {
					if (nextCards[i] instanceof CreatureCard) {
						((CreatureCard) nextCards[i]).setLifelink(true);
					}
				}
			} else if (nextAbility.equalsIgnoreCase("firstStrike")) {
				for (int i = 0; i < nextCards.length; i++) {
					if (nextCards[i] instanceof CreatureCard) {
						((CreatureCard) nextCards[i]).setFirstStrike(true);
					}
				}
			} else if (nextAbility.equalsIgnoreCase("flying")) {
				for (int i = 0; i < nextCards.length; i++) {
					if (nextCards[i] instanceof CreatureCard) {
						((CreatureCard) nextCards[i]).setFlying(true);
					}
				}
			} else if (nextAbility.equalsIgnoreCase("vigilance")) {
				for (int i = 0; i < nextCards.length; i++) {
					if (nextCards[i] instanceof CreatureCard) {
						((CreatureCard) nextCards[i]).setVigilance(true);
					}
				}
			}
		}

	}

	/**
	 * Everytime an end tag is found, this method is called. This is also part
	 * of the content handler.
	 */
	public void endElement(String uri, String localname, String type) {

		// If the end tag is ability
		if (type.equalsIgnoreCase("ability")) {
			// Then if it's an activated ability
			if (nextAbility.getType().equalsIgnoreCase("activated")) {
				for (int i = 0; i < nextCards.length; i++) {
					// add it to the activated abilities vector for each of
					// these cards
					nextCards[i].getActivatedAbilities().add(nextAbility);
				}
			} else if (nextAbility.getType().equalsIgnoreCase(
					"creatureEntersPlay")) {
				// If it's a creatureEntersPlay ability
				for (int i = 0; i < nextCards.length; i++) {
					// Add the effects of the ability to the
					// creatureEntersPlayEffects vector. In this case the
					// abilities vector just holds all of the values in order to
					// append them all at the end. The vector doesn't actually
					// bind all those effects as one ability.
					nextCards[i].setCreatureEntersPlayEffects(nextAbility
							.getEffects());
				}
			} else if (nextAbility.getType().equalsIgnoreCase("leavePlay")) {
				// If it's a leavePlay ability then add it to the
				// leavePlayEffects vector. See creatureEntersPlay for full
				// comments.
				for (int i = 0; i < nextCards.length; i++) {
					nextCards[i].setLeavePlayEffects(nextAbility.getEffects());
				}
			} else if (nextAbility.getType().equalsIgnoreCase(
					"enchantmentEntersPlay")) {
				// If it's an enchantmentEntersPlay ability then add it to the
				// leavePlayEffects vector. See creatureEntersPlay for full
				// comments.
				for (int i = 0; i < nextCards.length; i++) {
					nextCards[i].setEnchantmentEntersPlayEffects(nextAbility
							.getEffects());
				}
			}

			/**
			 * Need to add additional abilities as they're introduced into the
			 * game
			 */

		} else if (type.equalsIgnoreCase("card")) {
			for (int i = 0; i < nextCards.length; i++) {
				deck.push(nextCards[i]);
			}
		}
	}

	public void characters(char[] ch, int start, int length) {
		/**
		 * Reuse if any characters end up occuring in the XML
		 */
		/*
		 * final String text = new String(ch, start, length);
		 * if(text.trim().length() > 0) { print("Characters", text); }
		 */
	}

	/**
	 * Creates a card array from the attributes contained in the card tag.
	 * 
	 * @param atts
	 *            The attributes used to build a card.
	 * @return The array of all cards created with those attributes (if number >
	 *         1)
	 */
	public Card[] createCards(Attributes atts) {
		// The type of the card
		String type = atts.getValue("type");
		// The power of the card if it's a creature
		String power = atts.getValue("power");
		// The toughness of the card if it's a creature
		String toughness = atts.getValue("toughness");
		// The subtypes of the card
		String subtype = atts.getValue("subtype");
		// The number of that card that are instantiated
		int number = Integer.parseInt(atts.getValue("number"));
		// The name of the card
		String name = atts.getValue("name");
		// The cards array to hold the values
		Card[] cards = new Card[number];

		// If it's a land
		if (type.equalsIgnoreCase("land")) {
			// Create all of the cards and add them to the cards array
			for (int i = 0; i < number; i++) {
				cards[i] = new LandCard(name);
				// If it has a subtype, update the subtypes
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		} else if (type.equalsIgnoreCase("creature")) {
			// If it's a creature and it doesn't have a power and toughness,
			// throw an error.
			if (power == null || toughness == null) {
				System.out
						.println("Error: Invalid power or toughness on creature "
								+ name);
			} else {
				// Otherwise create the correct number of those cards with the
				// appropriate name, power, and toughness.
				for (int i = 0; i < number; i++) {
					cards[i] = new CreatureCard(name, Integer.parseInt(power),
							Integer.parseInt(toughness));
					// if it has subtypes, update them.
					if (subtype != null)
						cards[i].updateSubtype(subtype);
				}
			}

		} else if (type.equalsIgnoreCase("enchantment")) {
			for (int i = 0; i < number; i++) {
				cards[i] = new EnchantmentCard(name);
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		} else if (type.equalsIgnoreCase("artifact")) {
			for (int i = 0; i < number; i++) {
				cards[i] = new ArtifactCard(name);
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		} else if (type.equalsIgnoreCase("instant")) {
			for (int i = 0; i < number; i++) {
				cards[i] = new InstantCard(name);
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		} else if (type.equalsIgnoreCase("sorcery")) {
			for (int i = 0; i < number; i++) {
				cards[i] = new SorceryCard(name);
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		} else if(type.equalsIgnoreCase("planeswalker"))
		{
			for (int i = 0; i < number; i++) {
				cards[i] = new PlaneswalkerCard(name);
				if (subtype != null)
					cards[i].updateSubtype(subtype);
			}
		}
		else {
			System.out
					.println("Error: Attempted to parse card with invalid type");
			return null;
		}
		return cards;
	}

	public Stack<Card> getDeck() {
		return deck;
	}

	public String getDeckName() {
		return deckName;
	}

}
