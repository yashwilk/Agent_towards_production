"""Makes the project's modules (main, agent, config, ...) importable from
tests without installing the project as a package."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
