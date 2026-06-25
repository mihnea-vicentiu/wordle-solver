import sys
import tempfile
from pathlib import Path


def _project_root():
      if getattr(sys, "frozen", False):
            return Path(sys._MEIPASS)
      return Path(__file__).resolve().parent.parent


PROJECT_ROOT = _project_root()
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "imgs"
DATA_DIR = PROJECT_ROOT / "data"
BUILD_DIR = PROJECT_ROOT / "build"
RUNTIME_DIR = Path(tempfile.gettempdir()) / "wordle-solver" if getattr(sys, "frozen", False) else BUILD_DIR

WORD_LIST_FILE = DATA_DIR / "cuvinte_wordle.txt"
SOLUTIONS_FILE = DATA_DIR / "solutii.txt"
COMMUNICATION_FILE = RUNTIME_DIR / "communication.txt"
SOLVER_SOURCE = PROJECT_ROOT / "solver" / "solver.cpp"
SOLVER_BINARY = BUILD_DIR / "solver"


def ensure_runtime_dirs():
      BUILD_DIR.mkdir(exist_ok=True)
      RUNTIME_DIR.mkdir(exist_ok=True)
