import os
import time
from GameInfo import GameInfo

local_appdata = os.getenv("LOCALAPPDATA")
log_path = f"{local_appdata}/OPP/Saved/Logs/OPP.log"

def process_line(line):
    for phase in game_session.phases_dict:  # continuously check through newest line for every game phase
        if phase in line:
            game_session.set_game_phase(phase)

            if phase == "GameStageInfo changed":  # check if stage changed to set info about the trial
                trial_id = line.split("Mission:", 1)[1].split(",", 1)[0].strip()
                difficulty = line.split("difficulty:", 1)[1].split(",", 1)[0].strip()
                player_count = line.split("Players:", 1)[1].split(",", 1)[0].strip()

                game_session.set_trial(trial_id)
                game_session.set_difficulty(difficulty)
                game_session.set_player_count(player_count)
            game_session.update_presence()
            break

def game_client_open():
    with open(log_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        try:
            if "Log file closed" in lines[-1]: # check last line for log file closed message
                return False
            return True
        except: # pretty sure this can fail because the log is deleted and recreated when you relaunch so you can get an index error
            return False

while True:
    game_session = None
    if game_client_open():
        game_session = GameInfo()
        with open(log_path,"r", encoding='utf-8') as f:
            for line in f:
                process_line(line)

            while True:
                line = f.readline()
                if line:
                    print(line)
                    if "Log file closed" in line:
                        break
                    process_line(line)
                else:
                    time.sleep(5)

    if game_session:
        game_session.drp.close()
    time.sleep(30)