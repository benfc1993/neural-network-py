from Matrix.Matrix import Matrix

a = Matrix(2, 2)
arr = [[4,2], [1,3]]
b = Matrix.from_array(arr)

a.add(2)
a.scale(3)
a.minus(b)
a.minus(1)

at = a.transpose()
ac = a.copy()

print(b.data)
print(a.data)
at.print()
ac.print()

c = Matrix.multiply(a, b)
c.print()
