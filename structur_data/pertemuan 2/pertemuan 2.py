fruits = ["apel", "mangga", "jeruk", "pisang", "anggur"]

print(fruits)
print(fruits[0])
print(fruits[-1])
print(fruits[1:3])

fruits.append("semangka")
fruits.insert(2, "durian")
fruits.remove("jeruk")
popped = fruits.pop()

print(len(fruits))
print(sorted(fruits))
print(fruits.count("apel"))
print(fruits.index("mangga"))

fruits.reverse()
fruits.sort()

numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(max(numbers))
print(min(numbers))
print(sum(numbers))

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2])

squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

a = [1, 2, 3]
b = [4, 5, 6]
combined = a + b
repeated = a * 3

print(3 in a)
print(10 not in b)

flat = [num for row in matrix for num in row]
print(flat)