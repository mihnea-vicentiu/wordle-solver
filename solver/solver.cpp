/* The following program is meant to work as a solver for the Wordle game.

How does it work: -> it communicates with the Wordle game through a shared communication file
                  -> the communication file path can be passed as a command-line argument
                  -> the solver waits for a base-3 pattern so it can calculate the next optimal guess
                  -> once the Python game closes, the solver closes as well

How it calculates the entropy: -> We calculate the entropy of a word by comparing it with every other possible target.
Each comparison produces one of 243 possible patterns. We count the pattern appearances, then use the formula:
S = P(0) / n * log2(n / P(0)) + P(1) / n * log2(n / P(1)) + ...... + P(242) / n log2(n / P(242)), where P(k) is the number of appearances of each pattern.
After guessing the optimal word, we keep only the words that give the same pattern and repeat the process.


Why did we write the solver in C++? -> efficiency and familiarity with the language.
*/

//libraries that we need for the solver
#include <fstream>
#include <string.h>
#include <math.h>
#include <iostream>

//pragma optimization to improve performance a bit
#pragma GCC optimize("Ofast,unroll-loops")

//this function will continuously read
// from communication.txt until the Python game provides a base 3 number or a "termination string"
int get_pattern(const std::string& communication_file) {
      std::ifstream f;
      std::string DataDump;
      //read till smth. happens
      while(true) {
            f.open(communication_file);
            f >> DataDump;
            f.close();

            //if from communication.txt we receive "---" then we know that the game was stopped
            if(DataDump == "---") {
                  exit(0);
            }

            //a pattern is encoded as a base-10 number with at most 3 digits
            if(DataDump.length() <= 3) {
                  return stoi(DataDump);
            }
      }
      //the functions should never reach this point, its use is just to avoid the warning from the compiler
      return -1;
}

//push the optimal word to the Python game after calculating the optimal guess
//used to clear up the code a bit
void push_wordle(const std::string& communication_file, std::string woptim) {
      std::ofstream g;
      g.open(communication_file);

      g << woptim;
      g.close();
}

//reads all the words that will be allowed in the game
//used to clear up the code a bit
void read_wordle_dictionary(const std::string& word_list_file, std::string wordle_dictionary[], int& n) {
      std::ifstream f;
      f.open(word_list_file);
      
      while(f >> wordle_dictionary[++n]);
      --n;
      f.close();
}

/*The words have all 5 letters, and every lattern can give us 3 situations when the word is guessed so we can reprezent the given pattern as a base 3 number where 
value 0 means grey, value 1 means yellow and value 2 means green, then we convert it to base 10 and give it a cod, this function returns the cod that guess gives
in raport with word(basically is as if we need to guess "word", and out guess is "guess")*/
int pattern_find(std::string word, std::string guess) {
      int code = 0, n = word.length();
      for(int i = 0;i < n;i++) {
            //green
            if(word[i] == guess[i]) {
                  code = code * 3 + 2;
                  continue;
            }
            //yellow
            if(word.find(guess[i]) != std::string::npos) {
                  code = code * 3 + 1;
                  continue;
            }
            //gray
            code = code * 3;
      }

      return code;
}

/*This function checks every possibel guess in raport with the current set of possibel words, then it returns the optimal word*/
std::string optimal_word_find(const std::string wd[], int m, int n) {
      int nrpattern[250];
      std::string woptim;
      long double entropy_max = -1;

      for(int i = 1;i <= m;i++) {
            // m reprezents the total number of words that we can guess
            memset(nrpattern, 0x0, sizeof(nrpattern));
            // reprezents the cardinality of the curret set of possibel words
            for(int j = 1;j <= n;j++)
                  ++nrpattern[pattern_find(wd[j], wd[i])];

            // we calculate the amount of information that it gives
            long double entropy_word = 0, p;
            for(int j = 0; j < 243; j++){
                  if(nrpattern[j]) {
                        p = 1.0 * nrpattern[j] / n;
                        entropy_word += p * -log2(p);
                  }
            }

            if(entropy_word > entropy_max) {
                  entropy_max = entropy_word;
                  woptim = wd[i];
            }
      }

      return woptim;
}

/*this function returns the smaller set of possibel words by checking what words from the current set gives us the same pattern as the one that needs to be guess,
when we guess the optimal word*/
int newSet(int n, int pattern, std::string wd[], std::string woptim) {
      int newN = 0;
      for(int j = 1;j <= n;j++) {
            int cod = pattern_find(wd[j], woptim);
            if(cod == pattern) {
                  std::swap(wd[++newN], wd[j]);
            }
      }
      return newN;
}

int main(int argc, char* argv[]) {
      std::string communication_file = argc >= 2 ? argv[1] : "build/communication.txt";
      std::string word_list_file = argc >= 3 ? argv[2] : "data/cuvinte_wordle.txt";

      int m = 0;
      std::string wordle_dictionary[15000];
      read_wordle_dictionary(word_list_file, wordle_dictionary, m);

      int n = m;
      // we will always find that is optimal to start with "TAREI", so we always start with "TAREI"
      std::string woptim = "TAREI";
      push_wordle(communication_file, woptim);

      int pattern;
      pattern = get_pattern(communication_file);
      n = newSet(m, pattern, wordle_dictionary, woptim);

      while(n != 0) {
            woptim = optimal_word_find(wordle_dictionary, m, n);
            push_wordle(communication_file, woptim);

            pattern = get_pattern(communication_file);
            n = newSet(n, pattern, wordle_dictionary, woptim);
            if(pattern == 242) {
                  break;
            }
      }

      return 0;
}
