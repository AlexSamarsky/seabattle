# from coords import coords_x, coords_y
from ship import Ship

from errors import WrongCoords, CoordOccupied, WrongShip

coords_x = '123456'
coords_y = 'ABCDEF'

# coords_x = '12'
# coords_y = 'AB'

class Coord():
    _x = 0
    _y = 0
    _coord = ''
    _ship = None
    _is_busy = False
    _is_hit = False
    
    def __init__(self, coord):
        self._x, self._y = self.get_coords_xy(coord)
        self._coord = coord
        self._ship = None
        self._is_hit = False
        self._is_busy = False
    
    @staticmethod
    def get_coords_xy(coord):
        if len(coord) != 2:
            raise WrongCoords('Не корректные координаты, они должны быть формата A1')
        c1 = coord[0]
        c2 = coord[1]
        if not c1 in coords_y:
            raise WrongCoords('Не корректные координаты, они должны быть формата A1')
        if not c2 in coords_x:
            raise WrongCoords('Не корректные координаты, они должны быть формата A1')
        return coords_x.find(c2), coords_y.find(c1)       
    
    @staticmethod
    def get_coords(x, y):
        if x < 0 or y < 0:
            raise WrongCoords('Не корректные координаты')
        return f'{coords_y[y]}{coords_x[x]}'
        
    @property
    def is_hit(self):
        return self._is_hit
    
    @is_hit.setter
    def is_hit(self, is_hit):
        if self._is_hit:
            raise CoordOccupied('Координата занята')
        self._is_hit = is_hit
    
    @property
    def ship(self):
        return self._ship
    
    @ship.setter
    def ship(self, ship):
        if not isinstance(ship, Ship):
            raise WrongShip('Не корректный корабль')
        self._ship = ship
        self._is_busy = True
    
    @property
    def busy(self):
        return self._is_busy
    
    @busy.setter
    def busy(self, value):
        self._is_busy = value    
    
    @property
    def coord(self):
        return self._coord
    
    def __str__(self):
        return self.to_str()
        # if self._is_hit and self._ship:
        #     return 'X'
        # elif self._is_hit and not self._ship:
        #     return 'T'
        # elif self._ship:
        #     return '■'
        # elif not self._ship:
        #     return 'O'
    
    def to_str(self, hidden = False):
        if self._is_hit and self._ship:
            return 'X'
        elif self._is_hit and not self._ship:
            return 'T'
        elif hidden:
            return 'O'
        elif self._ship:
            return '■'
        elif not self._ship:
            return 'O'
    
if __name__ == '__main__':
    coord = Coord('A1')
    coord.hit = True
    coord.ship = Ship(1,1)
    print(f'coord.ship: {coord.ship}')
    print(f'coord: {coord}')
    