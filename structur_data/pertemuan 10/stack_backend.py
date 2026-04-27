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

    def display(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        self.top = None
        self._size = 0

    def contains(self, item):
        current = self.top
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def push_many(self, items):
        for item in items:
            self.push(item)

    def pop_all(self):
        result = []
        while not self.is_empty():
            result.append(self.pop())
        return result

    def reverse(self):
        items = self.to_list()
        self.clear()
        for item in items:
            self.push(item)

    def __str__(self):
        return "Stack: " + " -> ".join(str(i) for i in self.to_list()) + " -> None"

    def __len__(self):
        return self._size

    def __contains__(self, item):
        return self.contains(item)


def cek_kurung(ekspresi):
    stack = StackLinkedList()
    buka = "({["
    tutup = ")}]"
    pasangan = {")": "(", "}": "{", "]": "["}
    for char in ekspresi:
        if char in buka:
            stack.push(char)
        elif char in tutup:
            if stack.is_empty() or stack.peek() != pasangan[char]:
                return False, stack.to_list()
            stack.pop()
    return stack.is_empty(), stack.to_list()


def balik_string(teks):
    stack = StackLinkedList()
    for char in teks:
        stack.push(char)
    return "".join(stack.pop_all())
