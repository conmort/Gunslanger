class Town:
    def __init__(self, row=5, col=5):
        self.row = row
        self.col = col
        self.grid = [[None for _ in range(col)] for _ in range(row)]
        self.player_position = (row // 2, col // 2)  # Starting position of the player
        self.buildings = {}  # Dictionary to store buildings in the Town