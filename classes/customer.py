__all__ = ('City', 'Customer', 'calculate_distance')


class City:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Customer:
    def __init__(self, num: int, x: float, y: float, demand: int):
        self._City = City(x, y)
        self._num = num
        self._demand = demand

    @property
    def num(self):
        return self._num

    @property
    def city(self):
        return self._City

    @property
    def demand(self):
        return self._demand

