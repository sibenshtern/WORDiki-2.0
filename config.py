import os
from enum import Enum

DEBUG = "debug"
RELEASE = "release"

runtime = os.environ.get("wordiki_runtime")
if (runtime != DEBUG and runtime != RELEASE) or runtime is None:
    runtime = RELEASE


class DebugTime(Enum):
    TEN_MINUTES = 0
    DAY = 0
    WEEK = 0
    MONTH = 0
    THREE_MONTHS = 0
    SIX_MONTHS = 0


class ReleaseTime(Enum):
    TEN_MINUTES = 10
    DAY = 24 * 60
    WEEK = 7 * 24 * 60
    MONTH = 30 * 24 * 60
    THREE_MONTHS = 3 * 30 * 24 * 60
    SIX_MONTHS = 6 * 30 * 24 * 60


class ButtonLabels:
    BAD = "bad"


if runtime == DEBUG:
    Time = DebugTime
elif runtime == RELEASE:
    Time = ReleaseTime
