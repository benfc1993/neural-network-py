import unittest
from .matrix import Matrix


class MyTestCase(unittest.TestCase):
    def test_from_array(self):
        target = Matrix(2, 3, 2)
        arr = [[2, 2, 2], [2, 2, 2]]
        m = Matrix.from_array(arr)
        self.check_matrix(m, target)

    def test_from_array(self):
        target = [1, 2, 3, 4]
        arr = [[1, 2], [3, 4]]
        m = Matrix.from_array(arr)
        n = Matrix.to_flat_array(m)
        self.assertEqual(n, target,
                         'Flattened matrix should be a list with length rows * cols with all data in sequence')

    def test_randomise(self):
        m = Matrix(2, 2)
        m.randomise()

        for r in range(m.rows):
            for c in range(m.cols):
                self.assertGreaterEqual(m.data[r][c], -1, 'values should be greater than -1')
                self.assertLessEqual(m.data[r][c], 1, 'values should be less than 1')

    def test_scale(self):
        m = Matrix(2, 2, 2)
        m.scale(3)
        self.check_values(m, 6)

    def test_add(self):
        m = Matrix(2, 2, 4)
        m.add(3)
        self.check_values(m, 7)

    def test_add_exception(self):
        m = Matrix(2, 2)
        n = Matrix(3, 3)
        self.assertRaises(ValueError, Matrix.add, m, n)

    def test_subtract(self):
        m = Matrix(2, 2, 2)
        n = Matrix(2, 2, 3)
        n.subtract(m)
        self.check_values(n, 1)

    def test_subtract_exception(self):
        m = Matrix(2, 2)
        n = Matrix(3, 3)
        self.assertRaises(ValueError, Matrix.s_subtract, m, n)

    def test_add_matrix(self):
        m = Matrix(2, 2, 4)
        n = Matrix(2, 2, 3)
        m.add(n)
        self.check_values(m, 7)

    def test_element_wise_multiplication(self):
        m = Matrix(2, 2, 4)
        n = Matrix(2, 2, 3)
        m.element_wise_multiply(n)
        self.check_values(m, 12)

    def test_element_wise_multiplication(self):
        m = Matrix(2, 2, 4)
        n = Matrix(2, 2, 3)
        m.element_wise_multiply(n)
        self.check_values(m, 12)

    # Util functions
    def check_values(self, matrix, value):
        for r in range(matrix.rows):
            for c in range(matrix.cols):
                self.assertEqual(matrix.data[r][c], value, f'each value in the matrix should be {value}')

    def check_matrix(self, matrix, target):
        for r in range(matrix.rows):
            for c in range(matrix.cols):
                self.assertEqual(matrix.data[r][c], target.data[r][c],
                                 f'Value at {r}, {c}, should be {target.data[r][c]}')


if __name__ == '__main__':
    unittest.main()
