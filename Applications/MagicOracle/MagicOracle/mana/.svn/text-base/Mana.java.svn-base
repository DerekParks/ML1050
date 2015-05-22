package mana;

import utils.Logger;


/**
 * This class defines all mana with methods of accessing it.
 * @author Alan
 *
 */
public class Mana {

	/**
	 * The amount of red mana.
	 */
	private int red=0;
	/**
	 * The amount of green mana.
	 */
	private int green=0;
	/**
	 * The amount of blue mana.
	 */
	private int blue=0;
	/**
	 * The amount of black mana.
	 */
	private int black=0;
	/**
	 * The amount of white mana.
	 */
	private int white=0;
	/**
	 * The amount of colorless mana.
	 */
	private int colorless=0;
	
	private Logger log = new Logger("Mana.log", "Mana", 3);
	
	public int getBlack() {
		return black;
	}
	public void setBlack(int black) {
		this.black = black;
	}
	public int getBlue() {
		return blue;
	}
	public void setBlue(int blue) {
		this.blue = blue;
	}
	public int getColorless() {
		return colorless;
	}
	public void setColorless(int colorless) {
		this.colorless = colorless;
	}
	public int getGreen() {
		return green;
	}
	public void setGreen(int green) {
		this.green = green;
	}
	public int getRed() {
		return red;
	}
	public void setRed(int red) {
		this.red = red;
	}
	public int getWhite() {
		return white;
	}
	public void setWhite(int white) {
		this.white = white;
	}
	public void incrementWhite()
	{
		white++;
	}
	public void incrementBlack()
	{
		black++;
	}
	public void incrementGreen()
	{
		green++;
	}
	public void incrementBlue()
	{
		blue++;
	}
	public void incrementRed()
	{
		red++;
	}
	public void incrementColorless()
	{
		colorless++;
	}
	public int getConvertedManaCost()
	{
		return black+red+colorless+green+blue+white;
	}
	public boolean decreaseWhite()
	{
		if(white<= 0)
		{
			return false;
		}
		else
		{
			white--;
			return true;
		}
	}
	public boolean decreaseBlack()
	{
		if(black<= 0)
		{
			return false;
		}
		else
		{
			black--;
			return true;
		}
	}
	public boolean decreaseGreen()
	{
		if(green<= 0)
		{
			return false;
		}
		else
		{
			green--;
			return true;
		}
	}
	public boolean decreaseBlue()
	{
		if(blue<= 0)
		{
			return false;
		}
		else
		{
			blue--;
			return true;
		}
	}
	public boolean decreaseRed()
	{
		if(red<= 0)
		{
			return false;
		}
		else
		{
			red--;
			return true;
		}
	}
	
	public void print()
	{
		log.print("Blue: " + blue, 3);
		log.print("Black: " + black, 3);
		log.print("Green: " + green, 3);
		log.print("Red: " + red, 3);
		log.print("White: " + white, 3);
		log.print("Colorless: " + colorless, 3);
	}
	/**
	 * Adds the new pool mana object to the current mana object
	 * @param newPool
	 */
	public void add(Mana newPool) {
		
		for(int i=0; i<newPool.getBlack(); i++)
		{
			incrementBlack();
		}
		for(int i=0; i<newPool.getRed(); i++)
		{
			incrementRed();
		}
		for(int i=0; i<newPool.getBlue(); i++)
		{
			incrementBlue();
		}
		for(int i=0; i<newPool.getGreen(); i++)
		{
			incrementGreen();
		}
		for(int i=0; i<newPool.getWhite(); i++)
		{
			incrementWhite();
		}
		for(int i=0; i<newPool.getColorless(); i++)
		{
			incrementColorless();
		}
		
	}
	
	
}
