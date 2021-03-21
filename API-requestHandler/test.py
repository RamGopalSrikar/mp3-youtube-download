from enum import Enum

class status (Enum):
    EMPTY = 0
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3

def testing():
    print(status.EMPTY.value)


testing()