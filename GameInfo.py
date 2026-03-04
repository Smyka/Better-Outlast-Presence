from pypresence import Presence
from game_constants import *

class GameInfo:
    def __init__(self):
        self.game_phase = None
        self.trial_map = None
        self.trial_name = None
        self.difficulty = None
        self.player_count = None
        self.playing_invasion = None
        self.invasion_team = None

        self.large_image = "murkoff"

        self.phases_dict = phases
        self.trial_names_dict = trial_names
        self.trial_maps_dict = trial_maps
        self.difficulty_dict = difficulty

        app_id = "1453685678012366878"
        self.drp = Presence(app_id)
        self.drp.connect()
        self.drp.update(large_image = self.large_image)

    def __str__(self):
        return (f"Game phase: {self.game_phase}\n"
                f"Trial: {self.trial_name}\n"
                f"Trial map: {self.trial_map}\n"
                f"Difficulty: {self.difficulty}\n"
                f"Player count: {self.player_count}")

    def set_game_phase(self, phase):
        self.game_phase = self.phases_dict[phase]

    def set_trial(self, trial_id):
        try:
            self.trial_name = self.trial_names_dict[trial_id]
            self.trial_map = self.trial_maps_dict[trial_id[:2]]
            self.large_image = trial_id.lower()
        except KeyError:
            print("Key error: ", trial_id)

    def set_difficulty(self, difficulty):
        self.difficulty = self.difficulty_dict[difficulty]

    def set_player_count(self, player_count):
        self.player_count = player_count


    def update_presence(self):
        if not self.game_phase:
            return "No game phase, most likely not in menu yet"

        if self.game_phase == "Menu":
            self.large_image = "murkoff"
            self.drp.update(
                state = "In the main menu",
                large_image = self.large_image
            )
            return

        if self.game_phase == "Lobby":
            self.large_image = "murkoff"
            self.drp.update(
                state="In the lobby",
                large_image=self.large_image
            )
            return

        if self.game_phase == "Loading trial":

            self.drp.update(
                state=f"{self.trial_name}",
                details="Loading trial...",
                small_image = "murkoff",
                large_image=self.large_image
            )
            return

        if self.game_phase == "StageStarted":

            self.drp.update(
                state=f"{self.trial_map} - {self.difficulty}",
                details=f"{self.trial_name}",
                small_image="murkoff",
                large_image=self.large_image
            )
            return