import os
import time

_DELAY = float(os.getenv("DEMO_DELAY", "0"))


def pause() -> None:
    if _DELAY > 0:
        time.sleep(_DELAY)
