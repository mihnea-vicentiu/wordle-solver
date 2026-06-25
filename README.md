# Wordle Solver

A Pygame implementation of Wordle with two ways to run it:

- manual play, where you type guesses yourself;
- solver play, where a C++ entropy-based solver chooses guesses and the Python UI visualizes the game.

The project uses a Romanian five-letter word list. The solver starts from `TAREI`, narrows the candidate set after every response pattern, and repeats until it finds the target word.

## Authors

- Mihnea-Vicentiu Buca
- Ricardo-Dumitru Petrovici

## Requirements

- Python 3.8+
- `pygame`
- `g++` with C++17 support
- Clear Sans font installed locally for the closest visual match. The archive is included in `assets/font/`.

Create a local virtual environment and install the Python dependency with:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead.

## Run

Run commands from the repository root.

Manual Wordle:

```bash
python -m wordle_game play
```

Manual Wordle with a fixed target word for testing:

```bash
python -m wordle_game play --word ABACA
```

Let the solver play one game:

```bash
python -m wordle_game solve
```

Let the solver play one fixed target word:

```bash
python -m wordle_game solve --word ABACA
```

Let the solver play forever, reset after each solved word, and continue with a new random target:

```bash
python -m wordle_game loop
```

Change the pause between solved games:

```bash
python -m wordle_game loop --reset-delay 2.5
```

The Python workflow automatically compiles the C++ solver into `build/solver` when needed. If you want to compile it manually, run:

```bash
mkdir -p build
g++ solver/solver.cpp -O2 -std=c++17 -o build/solver
```

## Release Builds

GitHub Actions can create release bundles for the two main app modes:

- `wordle-manual-linux.zip`, which opens manual play;
- `wordle-solver-loop-linux.zip`, which opens the continuous solver loop.

Create and push a version tag to trigger a release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow can also be started manually from the GitHub Actions tab.

## Project Structure

```text
wordle_game/
  cli.py              Command-line entry point
  game.py             Manual, solver, and loop workflows
  dictionary.py       Word-list loading
  paths.py            Shared project paths
  ui/                 Pygame rendering, animations, tiles, colors, and solver interaction

solver/
  solver.cpp          C++ entropy solver

data/
  cuvinte_wordle.txt  Wordle dictionary
  solutii.txt         Precomputed solution traces / reference results

assets/
  imgs/               Window icon and title image
  font/               Clear Sans font archive

build/                Generated solver binary and runtime communication file
```

## How The Solver Communicates With The Game

The UI and solver communicate through `build/communication.txt`.

- The C++ solver writes a five-letter guess.
- The Python game reads that guess, renders it, computes the Wordle color pattern, and writes the pattern back as a base-3 encoded integer.
- The solver reads the pattern, filters the candidate set, computes the next highest-entropy guess, and writes it back.
- When the target word is solved or the window is closed, the Python side sends a termination signal.

## Algorithm Summary

For each possible guess, the solver compares that guess against every currently possible target word. Each comparison produces one of `3^5 = 243` color patterns: grey, yellow, or green for each letter.

The solver counts how often each pattern appears and computes the Shannon entropy of the guess. The word with the highest entropy is chosen because it is expected to split the remaining candidates most effectively. After receiving the actual pattern from the game, the solver keeps only the words that would have produced the same pattern and repeats the process.

The included reference results report an average of about `3.98979` guesses with the current strategy and opening word.

## References

- [NYT Wordle](https://www.nytimes.com/games/wordle/index.html)
- [Wordle Unlimited](https://wordleunlimited.org/)
- [Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA&t=0s)
- [Oh, wait, actually the best Wordle opener is not "crane"...](https://www.youtube.com/watch?v=fRed0Xmc2Wg&t=0s)
- [Maximising Differential Entropy to Solve Wordle](https://aditya-sengupta.github.io/coding/2022/01/13/wordle.html)
- [Intuitively Understanding the Shannon Entropy](https://www.youtube.com/watch?v=0GCGaw0QOhA)
- [Entropy in Compression - Computerphile](https://www.youtube.com/watch?v=M5c_RFKVkko)
