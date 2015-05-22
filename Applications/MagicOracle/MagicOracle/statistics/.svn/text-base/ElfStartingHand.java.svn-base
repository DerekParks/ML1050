package statistics;


public class ElfStartingHand extends StartingHand {

	private int numElvishHarbinger = 0;

	private int numElvishPromenade = 0;

	private int numEyeblightsEnding = 0;

	private int numForest = 0;

	private int numGarrukWildspeaker = 0;

	private int numImmaculateMagistrate = 0;

	private int numImperiusPerfect = 0;

	private int numJaggedScarArchers = 0;

	private int numLlanowarElves = 0;

	private int numLysAlanaHuntmaster = 0;

	private int numSwamp = 0;

	private int numVigor = 0;

	ElfStartingHand(String[] startingCards) {
		for (int i = 0; i < startingCards.length; i++) {
			if (startingCards[i].equalsIgnoreCase("Elvish Harbinger")) {
				numElvishHarbinger++;
			} else if (startingCards[i].equalsIgnoreCase("Elvish Promenade")) {
				numElvishPromenade++;
			} else if (startingCards[i].equalsIgnoreCase("Eyeblight's Ending")) {
				numEyeblightsEnding++;
			} else if (startingCards[i].equalsIgnoreCase("Forest")) {
				numForest++;
			} else if (startingCards[i].equalsIgnoreCase("Garruk Wildspeaker")) {
				numGarrukWildspeaker++;
			} else if (startingCards[i].equalsIgnoreCase("Immaculate Magistrate")) {
				numImmaculateMagistrate++;
			} else if (startingCards[i].equalsIgnoreCase("Imperius Perfect")) {
				numImperiusPerfect++;
			} else if (startingCards[i].equalsIgnoreCase("Jagged Scar Archers")) {
				numJaggedScarArchers++;
			} else if (startingCards[i].equalsIgnoreCase("Llanowar Elves")) {
				numLlanowarElves++;
			} else if (startingCards[i].equalsIgnoreCase("Lys Alana Huntmaster")) {
				numLysAlanaHuntmaster++;
			} else if (startingCards[i].equalsIgnoreCase("Swamp")) {
				numSwamp++;
			} else if (startingCards[i].equalsIgnoreCase("Vigor")) {
				numVigor++;
			} else {
				System.out.println("Error:  Unrecognized card!");
				System.exit(1);
			}
		}
	}

	public String startingHandAsString() {
		return (numElvishHarbinger + "," + numElvishPromenade + ","
				+ numEyeblightsEnding + "," + numForest + ","
				+ numGarrukWildspeaker + "," + numImmaculateMagistrate + ","
				+ numImperiusPerfect + "," + numJaggedScarArchers + ","
				+ numLlanowarElves + "," + numLysAlanaHuntmaster + ","
				+ numSwamp + "," + numVigor);
	}

	public static void main(String[] args) {
		String[] startingHand = new String[7];
		startingHand[0] = "Elvish Harbinger";
		startingHand[1] = "Elvish Harbinger";
		startingHand[2] = "Elvish Harbinger";
		startingHand[3] = "Elvish Harbinger";
		startingHand[4] = "Elvish Harbinger";
		startingHand[5] = "Elvish Harbinger";
		startingHand[6] = "Elvish Harbinger";
		ElfStartingHand theHand = new ElfStartingHand(startingHand);
		System.out.println(theHand.startingHandAsString());
	}

}
