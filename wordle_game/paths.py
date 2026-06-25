from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "imgs"
DATA_DIR = PROJECT_ROOT / "data"
BUILD_DIR = PROJECT_ROOT / "build"

WORD_LIST_FILE = DATA_DIR / "cuvinte_wordle.txt"
SOLUTIONS_FILE = DATA_DIR / "solutii.txt"
COMMUNICATION_FILE = BUILD_DIR / "communication.txt"
SOLVER_SOURCE = PROJECT_ROOT / "solver" / "solver.cpp"
SOLVER_BINARY = BUILD_DIR / "solver"


def ensure_runtime_dirs():
      BUILD_DIR.mkdir(exist_ok=True)
