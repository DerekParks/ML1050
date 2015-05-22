package magic.effects;

public class ShuffleIntoLibraryEffect extends Effect {

	
	// It really doesn't matter which of these is called, but most likely it 
	// will be the default executeEffect.
	public void executeEffect() {
		executeEffect(myCard);
		
	}

	public void executeEffect(Object theObject) {
		myPlayer.shuffleCardIntoLibrary(myCard);
	}

}
