package decks;

import java.util.Random;
import java.util.Stack;

import magic.Player;
import cards.Card;
import exceptions.LoseGameException;

public class Deck {

	DeckBuilder loader;

	Stack<Card> cards;
	
	private String name;

	public Deck(String xmlFile, Player p) {
		loader = new DeckBuilder(xmlFile, p);
		cards = loader.buildDeck();
		name = loader.getDeckName();
		//print();
		shuffle();
		//print();
	}
	
	public void print()
	{
		System.out.println("Here's my deck: <" + name + ">");
		for (int i = 0; i < cards.size(); i++) {
			cards.get(i).print();
		}
	}

	/**
	 * Shuffles the deck.
	 *
	 */
	public void shuffle() {
		//Temporary deck to hold new order
		Stack<Card> tempCards = new Stack<Card>();
		//As long as there are cards left in the deck
		while(!cards.empty())
		{
			//Select a random number between 0 and the size of the cards stack
			Random generator = new Random();
			int nextCard = generator.nextInt(cards.size());
			//Push that card onto the temp stack and remove it from the cards stack
			tempCards.push(cards.get(nextCard));
			cards.remove(nextCard);
		}
		//Set the cards stack to the temp cards stack
		cards = tempCards;
	}

	/**
	 * Returns the top card of the deck. The deck must contain at least one card
	 * for this method to be called.
	 * 
	 * @return The top card of the deck
	 * @throws LoseGameException 
	 */
	public Card draw() throws LoseGameException {
		if(cards.size() > 0)
			return cards.pop();
		else
			throw new LoseGameException("");
	}

	public String getName() {
		return name;
	}
	
	/**
	 * This method will remove the specified card from the deck.
	 * @param cardToRemove The card being removed from the deck.  This should
	 * be a card that already exists in the deck.
	 */
	public void removeCard(Card cardToRemove)
	{
		cards.removeElement(cardToRemove);
	}
	
	/**
	 * This method takes the specified card and puts it on the top of the 
	 * stack.
	 * @param cardToPush The card that will be put on top of the deck.
	 */
	public void putCardOnTop(Card cardToPush)
	{
		cards.insertElementAt(cardToPush, 0);
	}
}
