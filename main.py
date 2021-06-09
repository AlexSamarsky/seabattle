from game import Game
from errors import BoardShipsError

try:
    game = Game()
    game.start_game()
except BoardShipsError as msg:
    print(msg)
