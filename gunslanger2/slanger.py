class Slanger:
    def __init__(self) -> None:
        self.name = "Undefined"

        # List of Bullet objects
        self.loaded_bullets = []
        self.stored_bullets = []

        # Slanger's stats
        self.movement = 1
        self.health = 1
        self.gold = 1

class PlayerSlanger(Slanger):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Player"

class CPUSlanger(Slanger):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CPU"