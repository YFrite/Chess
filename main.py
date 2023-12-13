from src.controller import Controller
from src.settings import CAPTURE
from src.states.game import Game
from src.states.menu import Menu
from src.states.splash import Splash

if __name__ == "__main__":
    app = Controller(CAPTURE)

    states = {"SPLASH": Splash(),
              "MENU": Menu(),
              "GAME": Game()}

    app.state_machine.setup_states(states, start_state="SPLASH")
    app.main()

