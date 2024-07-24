class Bullet:
    def __init__(self) -> None:
        self.bullet_type = ""
        self.is_loaded = False
        self.is_stored = False
        self.coordinates = None
        self.direction = ""
        self.health = 1
        self.movement = 1
        self.movement_per_turn = 1
        self.damage = 1
        print(f'Bullet initialized with health: {self.health}')

class EtherealBullet(Bullet):
    # Doesn’t hit bullets (friendly or enemy)
    def __init__(self) -> None:
        super().__init__()

class BigBullet(Bullet):
    # Is bigger with more health -- does not deal damage to Slangers
    def __init__(self) -> None:
        super().__init__()
        self.health = 3

class SmallBullet(Bullet):
    # Is faster with less health -- does not deal damage to bullets
    def __init__(self) -> None:
        super().__init__()
        self.movement = 2
        self.movement_per_turn = 2