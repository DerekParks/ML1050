package utils;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;

/**
 * NOTE: This file is not quite working. I just have the messages printing to
 * the console for the time being.
 * 
 * @author Alan
 * 
 */
public class Logger {

	private int debugLevel;

	private PrintStream output;

	private String source;

	public Logger(String fileName, int debugLevel) {
		this.debugLevel = debugLevel;
		try {
			FileOutputStream out = new FileOutputStream(fileName);
			output = new PrintStream(out);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	public Logger(String fileName, String source, int debugLevel) {
		this.debugLevel = debugLevel;
		this.source = source;
		try {
			FileOutputStream out = new FileOutputStream(fileName);
			output = new PrintStream(out);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Prints a message with a given debug level.
	 * 
	 * @param message
	 *            The message to print.
	 * @param debug
	 *            The debug level of the message. Only outputs if this is less
	 *            than or equal to the debugLevel for the log.
	 */
	public void print(String message, int debug) {
		if (debug <= debugLevel) {
			if (source != null) {
				output.println("(" + source + ") " + message);
				System.out.println("(" + source + ") " + message);
			}

			else {
				output.println(message);
				System.out.println(message);
			}

		}
	}

	public void kill() {
		output.close();
	}
}
