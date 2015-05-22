package cards;

public class cardComparator {
	
	public static boolean subTypesEqual(Card card1, Card card2)
	{
		return card1.getSubtypes()[0].equals(card2.getSubtypes()[0]) ||
			   card1.getSubtypes()[0].equals(card2.getSubtypes()[1]) ||
			   card1.getSubtypes()[1].equals(card2.getSubtypes()[0]) ||
			   card1.getSubtypes()[1].equals(card2.getSubtypes()[1]);
	}
	
	public static boolean subTypeEquals(Card card1, String subType)
	{
		return card1.getSubtypes()[0].equals(subType) ||
			   card1.getSubtypes()[1].equals(subType);
	}

}
