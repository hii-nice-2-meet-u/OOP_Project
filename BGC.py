import sys

try:
    from BGC_SYSTEM import *
except Exception as e:
    print(f"ImportError: {e}", file=sys.stderr)
