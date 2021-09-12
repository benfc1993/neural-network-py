from random import random


# noinspection PyRedeclaration
class Matrix:
    def __init__(self, rows, cols, seed=0):
        self.rows: int = rows
        self.cols: int = cols
        self.data: list[list[float]] = [[seed] * cols for _i in range(rows)]

    @classmethod
    def from_array(cls, input_array):
        rows = len(input_array)
        cols = len(input_array[0]) if isinstance(input_array[0], list) else 1
        matrix = Matrix(rows, cols)

        for r in range(rows):
            for c in range(cols):
                matrix.data[r][c] = (input_array[r] if cols == 1 else input_array[r][c])

        return matrix

    @classmethod
    def to_flat_array(cls, m):
        arr = []
        for r in range(m.rows):
            for c in range(m.cols):
                arr.append(m.data[r][c])
        return arr

    def randomise(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] = random() * 2 - 1

    def scale(self, mod):
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] *= mod

    def add(self, mod):
        if isinstance(mod, Matrix) and self.rows is not mod.rows and self.cols is not mod.cols:
            raise ValueError('rows and columns must be equal')

        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] += (mod.data[r][c] if isinstance(mod, Matrix) else mod)

    @classmethod
    def s_subtract(cls, a, b):
        if a.rows is not b.rows and a.cols is not b.cols:
            raise ValueError('rows and columns must be equal')

        result = Matrix(a.rows, b.cols)
        for r in range(result.rows):
            for c in range(result.cols):
                result.data[r][c] = a.data[r][c] - b.data[r][c]

        return result

    def subtract(self, mod):
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] -= (mod.data[r][c] if isinstance(mod, Matrix) else mod)

    @classmethod
    def s_multiply(cls, a, b):
        if a.cols is not b.rows:
            raise ValueError('first matrix columns must match second rows')

        result = Matrix(a.rows, b.cols)

        for r in range(result.rows):
            for c in range(result.cols):
                total = 0
                for k in range(a.cols):
                    total += a.data[r][k] * b.data[k][c]
                result.data[r][c] = total

        return result

    def element_wise_multiply(self, mod):
        if self.rows is not mod.rows and self.cols is not mod.cols:
            raise ValueError('first matrix columns must match second rows')

        for r in range(self.rows):
            for c in range(mod.cols):
                self.data[r][c] *= mod.data[r][c]

    @classmethod
    def s_funcmap(cls, m, func):
        result = Matrix(m.rows, m.cols)
        for r in range(m.rows):
            for c in range(m.cols):
                result.data[r][c] = func(m.data[r][c])

        return result

    def funcmap(self, func):

        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] = func(self.data[r][c])

    def transpose(self):

        result = Matrix(self.cols, self.rows)
        for r in range(self.rows):
            for c in range(self.cols):
                result.data[c][r] = self.data[r][c]

        return result

    @classmethod
    def s_transpose(cls, m):
        result = Matrix(m.cols, m.rows)
        for r in range(m.rows):
            for c in range(m.cols):
                result.data[c][r] = m.data[r][c]

        return result

    def copy(self):
        copy = Matrix(self.rows, self.cols)
        for r in range(self.rows):
            for c in range(self.cols):
                copy.data[r][c] = self.data[r][c]

        return copy

    def print(self):
        print(self.data)

    @classmethod
    def deserialise(cls, data):
        m = Matrix(data['rows'], data['cols'])
        m.data = data['data']

        return m
