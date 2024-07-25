# Constants:
COLS = 3
ROWS = 7

class CombatStage:
    def __init__(self) -> None:
        # Create stage lanes:
        self.stage_lanes = [[[] for i in range(COLS)] for j in range(ROWS)]
        # If col = 3, row = 2, this looks like:
            # [[[],[],[]]]           [[['b'],[],['b']]] 
            # [[[],[],[]]]           [[['b','b'],[],[]]]
        # Each "tile" in the "grid" is a list so it can handle overlapping bullets
