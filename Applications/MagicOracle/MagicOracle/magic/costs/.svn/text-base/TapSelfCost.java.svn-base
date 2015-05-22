package magic.costs;

import magic.Player;
import cards.Card;

public class TapSelfCost extends Cost{

	@Override
	public boolean playable(Player p, Card c) {
		if(!c.isTapped())
		{
			return true;
		}
		return false;
	}

}
