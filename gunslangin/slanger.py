class Slanger:
    def __init__(self, name="") -> None:
        self.all_bullets = []
        self.loaded_bullets = []
        self.stored_bullets = []
        self.active_bonuses = None
        self.movement = 1
        self.name = name
        self.health = 1

    # Getter and Setter for all_bullets
    @property
    def all_bullets(self):
        return self._all_bullets

    @all_bullets.setter
    def all_bullets(self, value):
        self._all_bullets = value

    # Getter and Setter for loaded_bullets
    @property
    def loaded_bullets(self):
        return self._loaded_bullets

    @loaded_bullets.setter
    def loaded_bullets(self, value):
        self._loaded_bullets = value

    # Getter and Setter for stored_bullets
    @property
    def stored_bullets(self):
        return self._stored_bullets

    @stored_bullets.setter
    def stored_bullets(self, value):
        self._stored_bullets = value

    # Getter and Setter for active_bonuses
    @property
    def active_bonuses(self):
        return self._active_bonuses

    @active_bonuses.setter
    def active_bonuses(self, value):
        self._active_bonuses = value

    # Getter and Setter for movement
    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, value):
        self._movement = value

    # Getter and Setter for all_bullets
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Getter and Setter for health
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
