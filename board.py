from ship import Ship
from coord import Coord, coords_x, coords_y
import re
from errors import WrongCoords, CoordOccupied, BoardShipsError

from random import randrange

class Board():
    
    _board_cells = {}
    _ships = []

    def __init__(self):
        self.new_board()
        
    def __str__(self):
        return self.to_str()
    
    def to_str(self, hidden = False):
        s_all = ''
        s_head = ' |'
        for c in coords_y:
            s_head += f'{c}|'
        s_all += f'{s_head}'
        for r in coords_x:
            s_row = f'{r}|'
            for c in coords_y:
                cell = self.find_cell(c+r)
                s_row += f'{cell.to_str(hidden)}|'
            s_all += f'\n{s_row}'
        return s_all
        
    def find_cell(self, coords):
        return self._board_cells[coords]

    @staticmethod
    def get_coords(coords):
        req_string = f'(?i)^([{coords_y}][{coords_x}])\s*([{coords_y}][{coords_x}])?$'
        match = re.match(req_string, coords)
        if not match:
            raise WrongCoords('Не корректные координаты, они должны быть формата A1 A2 или A1')
        coord1 = match.group(1)
        coord2 = match.group(2)
        if not coord2:
            coord2 = coord1
        return str.upper(coord1), str.upper(coord2)
    
    @staticmethod
    def get_hit_coord(coord):
        req_string = f'(?i)^([{coords_y}][{coords_x}])$'
        match = re.match(req_string, coord)
        if not match:
            raise WrongCoords('Не корректные координаты, они должны быть формата A1')
        coord1 = match.group(1)
        return str.upper(coord1)
    
    @staticmethod
    def extract_coords(coords):
        try:
            coord1, coord2 = Board.get_coords(coords)
        except WrongCoords as err:
            raise WrongCoords(err)
        x1, y1 = Coord.get_coords_xy(coord1)
        x2, y2 = Coord.get_coords_xy(coord2)
        if x1-x2 != 0 and y1-y2 != 0:
            raise WrongCoords('Корабль должен быть поставлен в линию, например: A1 A2')
        
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        
        return x1, y1, x2, y2
        
    def can_mount_ship(self, coords, ship):
        x1, y1, x2, y2 = self.extract_coords(coords)
        set_ship_length = max(abs(x2-x1), abs(y2-y1)) + 1
        if set_ship_length != ship.length:
            return False
        
        can_mount = True
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                cell_coord = Coord.get_coords(x, y)
                board_cell = self.find_cell(cell_coord)
                if board_cell.busy:
                    can_mount = False
        return can_mount
    
    def set_next_ship(self, coords):
        ship_mounted = False
        for ship in self._ships:
            x1, y1, x2, y2 = self.extract_coords(coords)
            set_ship_length = max(abs(x2-x1), abs(y2-y1)) + 1
            if not ship.mounted and set_ship_length == ship.length:
                ship_mounted = self.set_ship(coords, ship)
                break
        if not ship_mounted:
            raise WrongCoords(f'Все корабли размера {set_ship_length} уже установлены')
        
    def set_ship(self, coords, ship):
        if not self.can_mount_ship(coords, ship):
            raise CoordOccupied('Невозможно поставить корабль')
        
        x1, y1, x2, y2 = self.extract_coords(coords)
        
        ship.mounted = True
        x_b1 = x1 if x1 == 0 else x1 - 1
        x_b2 = x2 if x2 + 1 == len(coords_x) else x2 + 1
        y_b1 = y1 if y1 == 0 else y1 - 1
        y_b2 = y2 if y2 + 1 == len(coords_y) else y2 + 1
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                cell_coord = Coord.get_coords(x, y)
                board_cell = self.find_cell(cell_coord)
                board_cell.ship = ship
        for x in range(x_b1, x_b2 + 1):
            for y in range(y_b1, y_b2 + 1):
                cell_coord = Coord.get_coords(x, y)
                board_cell = self.find_cell(cell_coord)
                if not board_cell.busy:
                    board_cell.busy = True
        
        return True

    def get_unmounted_ships(self):
        val = []
        for ship in self._ships:
            if not ship.mounted:
                val.append(ship)
        return val

    def check_can_mount_next_ship(self):
        for ship in self._ships:
            if not ship.mounted:
                empty_coords = []
                for coord, cell in self._board_cells.items():
                    if not cell.busy:
                        empty_coords.append(coord)
                if empty_coords and not len(empty_coords):
                    raise BoardShipsError('Не возможно поставить еще один корабль, текущая игра будет завершена!')
                
                can_mount = False
                for coord in empty_coords:
                    directions = self.fill_possible_directions(ship, coord)
                    if directions and len(directions):
                        can_mount = True
                return can_mount

    def set_ships_random(self):
        for ship in self._ships:
            if not ship.mounted:
                cnt = 0
                while True:
                    cnt += 1
                    coord = self.get_random_un_busy_coord()
                    directions = self.fill_possible_directions(ship, coord)
                    if directions and len(directions):
                        ship_coords = directions[randrange(len(directions))]
                        try:
                            self.set_ship(ship_coords, ship)
                            break
                        except CoordOccupied as msg:
                            raise CoordOccupied(msg)
                    if cnt > 10:
                        raise BoardShipsError('Не возможно поставить еще один корабль, текущая игра будет завершена!')
    
    def fill_possible_directions(self, ship, coord):
        x, y = Coord.get_coords_xy(coord)
        ship_shift = ship.length - 1
        directions = []
        if ship_shift == 0:
            directions.append(coord)
        else:            
            self.add_possible_direction(directions, ship, coord, x, y + ship_shift)
            self.add_possible_direction(directions, ship, coord, x, y - ship_shift)
            self.add_possible_direction(directions, ship, coord, x + ship_shift, y)
            self.add_possible_direction(directions, ship, coord, x - ship_shift, y)
        return directions
    
    def add_possible_direction(self, directions, ship, coord1, x, y):
        try:
            coord2_check = Coord.get_coords(x, y)
            coord2 = self.get_hit_coord(coord2_check)
            if coord2:
                coords = f'{coord1} {coord2}'
                if self.can_mount_ship(coords, ship):
                    directions.append(coords)
        except:
            return None    

    def make_shot_and_hit(self, input_coord):
        try:
            coord = self.get_hit_coord(input_coord)
        except WrongCoords as msg:
            raise WrongCoords(msg)
        
        cell = self.find_cell(coord)
        if cell.is_hit:
            raise WrongCoords(f'По координате {coord} уже был выстрел!')
        
        cell.is_hit = True
        if cell.ship:
            ship_hits = 0
            for cell_search in self._board_cells.values():
                if cell_search.ship == cell.ship and cell_search.is_hit:
                    ship_hits += 1
            
            if ship_hits == cell.ship.length:
                cell.ship.sunk = True
            return True
        return False
    
    def all_ships_sunk(self):
        for ship in self._ships:
            if not ship.sunk:
                return False
        return True
    
    def new_board(self):
        self._board_cells = {}
        self._ships = []
        for r in coords_x:
            for c in coords_y:
                coord_string = c+r
                new_coord = Coord(coord_string)
                self._board_cells[coord_string] = new_coord

        self._ships.append(Ship(3, 1))        
    
        for r in range(1, 3):
            ship = Ship(2, r)
            self._ships.append(ship)   

        for r in range(1, 4):
            ship = Ship(1, r)
            self._ships.append(ship)   
        
    def get_random_un_busy_coord(self):
        empty_coords = []
        for coord, cell in self._board_cells.items():
            if not cell.busy:
                empty_coords.append(coord)
        
        if empty_coords and not len(empty_coords):
            raise BoardShipsError('Не возможно определить свободную ячейку! Такого не должно быть!')
        coord = empty_coords[randrange(len(empty_coords))]
        return coord
        
    def get_random_not_hit_coord(self):
        empty_coords = []
        for coord, cell in self._board_cells.items():
            if not cell.is_hit:
                empty_coords.append(coord)
        
        if empty_coords and not len(empty_coords):
            raise BoardShipsError('Не возможно определить свободную ячейку! Такого не должно быть!')
        coord = empty_coords[randrange(len(empty_coords))]
        return coord
    
    
if __name__ == '__main__':
    board = Board()
    # board.SetShipRandom()
    # try:
    #     board.set_ship('A1 C8')
    # except WrongCoords as err:
    #     print (err)
    # except CoordOccupied as err:
    #     print (err)
    # board.set_ship('A4')
    # board.set_ship('E2 C2')
    # board.set_ship('E6 D6')
    # board.set_ship('E4 E5')
    # board.set_ship('A3 B3')
    # board.set_ship('D4 E4')
    # board.set_ship('B5 B5')
    # board.set_ship('A2 A2')

    # board.set_next_ship('E4 E2')
    # board.set_next_ship('B2 B3')
    # board.set_next_ship('A6 B6')
    # board.set_next_ship('F6 F6')
    # board.set_next_ship('D6 D6')

    # board.set_next_ship('E4 C4')
    # board.set_next_ship('F6 D6')
    # board.set_next_ship('D1 B1')
    # board.set_next_ship('A5 A3')
    # if not board.check_can_mount_next_ship():
    #     print('не возможно поставить следующий корабль')
    try:
        # board.set_next_ship('A1')
        board.set_ships_random()
        board.make_shot_and_hit('A1')
        board.make_shot_and_hit('B2')
        board.make_shot_and_hit('C3')
        board.make_shot_and_hit('D4')
    except BoardShipsError as msg:
        print(msg)
    #     pass
    print(str(board))