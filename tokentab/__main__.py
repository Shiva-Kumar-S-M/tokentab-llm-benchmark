"""
Entry point module when run with `python -m tokentab`.
"""

import sys
from tokentab.cli import main

if __name__ == "__main__":
    main(sys.argv[1:])
