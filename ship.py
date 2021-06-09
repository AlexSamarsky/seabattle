# from coord import coords_x, coords_y

from errors import WrongCoords, CoordOccupied, WrongShip
# coords_x = '123456'
# coords_y = 'ABCDEF'

# class WrongCoords(Exception):
#     pass


# class CoordOccupied(Exception):
#     pass


# class WrongShip(Exception):
#     pass


class Ship():
    
    _sunk = False
    _mounted = False
    _name = ''
    _length = 0
    
    def __init__(self, length, number):
        self._length = length
        self._number = number
        self._name = f'S{number}_{length}'

    @property
    def length(self):
        return self._length

    @property
    def sunk(self):
        return self._sunk
    
    @property
    def mounted(self):
        return self._mounted

    @sunk.setter
    def sunk(self, sunk):
        if not isinstance(sunk, bool):
            raise WrongShip('Корабль может быть потоплен (True/False)')
        self._sunk = sunk
    
    @mounted.setter
    def mounted(self, mounted):
        if not isinstance(mounted, bool):
            raise WrongShip('Корабль может быть установлен (True/False)')
        self._mounted = mounted
    
    def __str__(self):
        return self._name

