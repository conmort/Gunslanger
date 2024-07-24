# Constants
ROW = 3
COL = 9

class Stage:
    def __init__(self) -> None:
        self.player_left = None             # slanger object
        self.player_right = None
        self.player_left_position = None    # coordinates
        self.player_right_position = None
        self.bullets_in_play = []           # bullet objects
        self.stage_lanes = [[[] for _ in range(COL) for _ in range(ROW)]]
        self.current_turn = None
        self.option_selected = ""           # movement, player_slanger, cpu_slanger, or bullet

    # Getter and Setter for player_left
    @property
    def player_left(self):
        return self._player_left

    @player_left.setter
    def player_left(self, value):
        self._player_left = value

    # Getter and Setter for player_right
    @property
    def player_right(self):
        return self._player_right

    @player_right.setter
    def player_right(self, value):
        self._player_right = value

    # Getter and Setter for player_left_position
    @property
    def player_left_position(self):
        return self._player_left_position

    @player_left_position.setter
    def player_left_position(self, value):
        self._player_left_position = value

    # Getter and Setter for player_right_position
    @property
    def player_right_position(self):
        return self._player_right_position

    @player_right_position.setter
    def player_right_position(self, value):
        self._player_right_position = value

    # Getter and Setter for bullets_in_play
    @property
    def bullets_in_play(self):
        return self._bullets_in_play

    @bullets_in_play.setter
    def bullets_in_play(self, value):
        self._bullets_in_play = value

    # Getter and Setter for stage_lanes
    @property
    def stage_lanes(self):
        return self._stage_lanes

    @stage_lanes.setter
    def stage_lanes(self, value):
        self._stage_lanes = value

    # Getter and Setter for current_turn
    @property
    def current_turn(self):
        return self._current_turn

    @current_turn.setter
    def current_turn(self, value):
        self._current_turn = value

    # Getter and Setter for option_selected
    @property
    def option_selected(self):
        return self._option_selected

    @option_selected.setter
    def option_selected(self, value):
        self._option_selected = value

    def initialize_stage(self, rows=3, cols=6):
        rows, cols = (rows, cols)
        self._stage_lanes = [[[] for _ in range(cols)] for _ in range(rows)]
