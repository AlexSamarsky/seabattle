import os
from board import Board
from errors import WrongCoords, CoordOccupied, BoardShipsError

class Game():
    _computer_board = None
    _player_board = None
    _playing = False
    _mounting_ships = False
    _computer_turn = False
    
    def __init__(self):
        self._playing = True
        self._mounting_ships = True
        print('Добро пожаловать в игру морской бой!')
        self._computer_board = Board()
        self._player_board = Board()
        self.fill_board(self._computer_board)
        print('Корабли компьютера установлены!')
            
            
    def fill_board(self, board):
        cnt = 0
        while True:
            if cnt >= 10:
                raise BoardShipsError('Не установлены корабли, что-то пошло не так. Обратитесь к разработчику!')
            try:
                board.set_ships_random()
                break
            except BoardShipsError:
                board.new_board()
                cnt += 1
                    
    def input_player_ships(self):
        cnt = 0
        while True:
            cnt += 1
            if cnt == 10:
                print('Видимо вы не хотите играть, раз не отвечаете корректно! Игра прекращена')
            response = input('Корабли можно поставить автоматически, хотите это сделать? (y/n): ')
            if response == 'y':
                self.fill_board(self._player_board)
                self._mounting_ships = False
                return
            elif response == 'n':
                while True:
                    unmounted_ships = self._player_board.get_unmounted_ships()
                    if unmounted_ships and not len(unmounted_ships):
                        self._mounting_ships = False
                        return
                    val = []
                    for ship in unmounted_ships:
                        val.append(str(ship))
                    
                    print (self._player_board.to_str())
                    str_ships = ', '.join(val)
                    print (f'Остались корабли {str_ships}')
                    coords = input('Введите координаты установки корабля в формате A1 или A1 A2: ')
                    try:
                        self._player_board.set_next_ship(coords)
                    except WrongCoords as msg:
                        print(msg)
                    except CoordOccupied as msg:
                        print(msg)
    
    def make_moves(self):
        while True:
            print('\n\nВаша доска получилась такой:')
            print(self._player_board)
            print('Ваши выстрелы по доске компьютера:')
            print(self._computer_board.to_str(hidden=True))
            if self._computer_turn:
                try:
                    coord = self._player_board.get_random_not_hit_coord()
                    print(f'Компьютер выстрелил по координатам {coord}')
                    os.system('read -s -n 1 -p "Нажмите любую клавишу для продолжения...\n"')
                    if self._player_board.make_shot_and_hit(coord):
                        print('И компьютер попал!')
                        if self._player_board.all_ships_sunk():
                            print('Компьютер уничтожил все ваши корабли! Вы проиграли! Спасибо за игру!')
                            return
                        else:
                            print('Еще один ход за компьютером!')
                    else:
                        self._computer_turn = not self._computer_turn
                        print('И компьютер промазал, теперь ваш ход')
                except BoardShipsError as msg:
                    print('Ошибка!!! Игра завершена')
                    print(msg)
                    return
            else:
                coord = input('Введите координаты куда хотие выстрелить в формате A1: ')
                try:
                    coord = Board.get_hit_coord(coord)
                    if self._computer_board.make_shot_and_hit(coord):
                        print('Вы попали!')
                        if self._computer_board.all_ships_sunk():
                            print('ПОЗДРАВЛЯЮ! Вы уничтожили все корабли противника!')
                            return
                    else:
                        self._computer_turn = not self._computer_turn
                        print('И вы промазали, теперь ход компьютера')
                except WrongCoords as msg:
                    print('!!!!ОШИБКА!!!!')
                    print(msg)
                except CoordOccupied as msg:
                    print('!!!!ОШИБКА!!!!')
                    print(msg)
    
    def start_game(self):
        self.input_player_ships()
        print ('Все корабли установлены!')
        self.make_moves()
        
if __name__ == '__main__':
    try:
        game = Game()
        game.start_game()
    except BoardShipsError as msg:
        print(msg)