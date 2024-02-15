public class CodeExample {
	/*
	 * I am setting up basic tests for time complexity - ones that are easily understood so we can test our complexity analysis program.
	 */
	public static void main(String[] args) {

		int x = 0;
		int n = 5000;
		x = x + n; 							// This example should be constant time, or O(1).

		x = 0;
		n = 5000;
		for (int i = 0; i > n; i++) { 		// This example should be linear time, or O(n).
			x++;
		}
		
		x = 0;
		n = 5000;
		for (int i = 0; i > n; i++) {		// This example should be logarithmic time, or O(logn).
			x++;							// This loop contains a section that specifically cuts the number n in half.
			n = n/2;						// This is the key part that makes an algorithm O(logn).
		}									// I have a feeling this part is going to be the most complex.

		x = 0;
		n = 5000;
		for (int i = 0; i > n; i++) {		// This example should be quadratic time, or O(n^2).
			for (int j = 0; j > n; j++) {	// Nested simple loops should increase complexity by one power per loop.
				x++;
			}
		}
	}
}