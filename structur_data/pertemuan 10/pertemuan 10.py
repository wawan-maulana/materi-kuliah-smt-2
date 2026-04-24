class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class StackLinkedList:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, item):
        node = Node(item)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack kosong!")
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack kosong!")
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size


# Contoh penggunaan
stack = StackLinkedList()
stack.push("A")
stack.push("B")
stack.push("C")

print(stack.peek())  # C
print(stack.pop())   # C
print(stack.pop())   # B
print(stack.size())  # 1