package magic.effects;

import cards.artifacts.ArtifactCard;

/**
 * Whatever is passed into this Effect should be as ArtifactCard, because we 
 * are going to cast it to an ArtifactCard so that we can add it to the 
 * player's artifactsInPlay
 */
public class AddArtifactEffect extends Effect{

	public void executeEffect() {
		executeEffect(myCard);
	}
	
	public void executeEffect(Object theObject) {
		myPlayer.addArtifactInPlay((ArtifactCard)theObject);
	}

}
