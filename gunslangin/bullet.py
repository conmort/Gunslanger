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

    # Getter and Setter for bullet_type
    @property
    def bullet_type(self):
        return self._bullet_type

    @bullet_type.setter
    def bullet_type(self, value):
        self._bullet_type = value

    # Getter and Setter for is_loaded
    @property
    def is_loaded(self):
        return self._is_loaded

    @is_loaded.setter
    def is_loaded(self, value):
        self._is_loaded = value

    # Getter and Setter for is_stored
    @property
    def is_stored(self):
        return self._is_stored

    @is_stored.setter
    def is_stored(self, value):
        self._is_stored = value

    # Getter and Setter for speed
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    # Getter and Setter for coordinates
    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    # Getter and Setter for health
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
    
    # Getter and Setter for movement
    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, value):
        self._movement = value

    # Getter and Setter for movement_per_turn
    @property
    def movement_per_turn(self):
        return self._movement_per_turn

    @movement_per_turn.setter
    def movement_per_turn(self, value):
        self._movement_per_turn = value

    # Getter and Setter for damage
    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

class EtherealBullet(Bullet):
    def __init__(self) -> None:
        super().__init__()