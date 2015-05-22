package statistics;

public class KithkinStartingHand extends StartingHand {
	private int numDoorOfDestinies = 0;

	private int numGoldmeadowStalwart = 0;

	private int numKithkinZephyrnaut = 0;

	private int numKinsbaileBorderguard = 0;

	private int numKnightOfMeadowgrain = 0;

	private int numMilitiasPride = 0;

	private int numMosquitoGuard = 0;

	private int numPlains = 0;

	private int numSurgeOfThoughtweft = 0;

	private int numVeteransArmaments = 0;

	private int numWizenedCenn = 0;

	public KithkinStartingHand(String[] startingCards) {

		for (int i = 0; i < startingCards.length; i++) {
			updateHand(startingCards[i]);
		}
	}


	public void updateHand(String name) {
		if (name.equalsIgnoreCase("Door of Destinies")) {
			numDoorOfDestinies++;
		} else if (name.equalsIgnoreCase("Goldmeadow Stalwart")) {
			numGoldmeadowStalwart++;
		} else if (name.equalsIgnoreCase("Kithkin Zephyrnaut")) {
			numKithkinZephyrnaut++;
		} else if (name.equalsIgnoreCase("Kinsbaile Borderguard")) {
			numKinsbaileBorderguard++;
		} else if (name.equalsIgnoreCase("Knight of Meadowgrain")) {
			numKnightOfMeadowgrain++;
		} else if (name.equalsIgnoreCase("Militia's Pride")) {
			numMilitiasPride++;
		} else if (name.equalsIgnoreCase("Mosquito Guard")) {
			numMosquitoGuard++;
		} else if (name.equalsIgnoreCase("Plains")) {
			numPlains++;
		} else if (name.equalsIgnoreCase("Surge of Thoughtweft")) {
			numSurgeOfThoughtweft++;
		} else if (name.equalsIgnoreCase("Veteran's Armaments")) {
			numVeteransArmaments++;
		} else if (name.equalsIgnoreCase("Wizened Cenn")) {
			numWizenedCenn++;
		} else {
			System.out.println("Error:  Unrecognized card!");
			System.exit(1);
		}
	}

	public String startingHandAsString() {
		return (numDoorOfDestinies + "," + numGoldmeadowStalwart + ","
				+ numKithkinZephyrnaut + "," + numKinsbaileBorderguard + ","
				+ numKnightOfMeadowgrain + "," + numMilitiasPride + ","
				+ numMosquitoGuard + "," + numPlains + ","
				+ numSurgeOfThoughtweft + "," + numVeteransArmaments + "," + numWizenedCenn);
	}
}
