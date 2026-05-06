"""
Тема 9, Списък 2 - Избрани задачи:

1. __repr__(): да връща стринг от стойностите на елементите на свързания списък
   size - да се добави като атрибут на класа и да се актуализират дефинициите

2. find(value): да връща всички позиции под формата списък, на които се среща
   конкретна стойност. Ако не се среща - празен списък.
   index(value): да връща първата позиция на която се среща такава стойност.
   Ако не се среща - празен списък. Реализирано като частен случай на find().

3. slice(start=0, stop=self.size, step=1): да връща нов обект от тип свързан
   списък, съдържащ само елементите с извлечените индекси.

"""

from collections.abc import Iterable, Iterator


class Node:

    def __init__(self, data=None):
        self.data = data
        self.next = None


class ExtendedLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        self.size += 1

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of range (0-{self.size})")

        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def delete(self, data):
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def delete_at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range")

        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data

        current = self.head
        for _ in range(index - 1):
            current = current.next

        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data

    # ------------------------------------------------------------------
    # TASK: __repr__()
    # ------------------------------------------------------------------

    def __repr__(self):
        values = []
        current = self.head
        while current:
            values.append(repr(current.data))
            current = current.next
        return f"LinkedList([{', '.join(values)}], size={self.size})"

    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.data))
            current = current.next
        return " -> ".join(values) + " -> None"

    # ------------------------------------------------------------------
    # TASK: find(value) and index(value)
    # ------------------------------------------------------------------

    def find(self, value):
        positions = []
        current = self.head
        idx = 0

        while current:
            if current.data == value:
                positions.append(idx)
            current = current.next
            idx += 1

        return positions

    def index(self, value):
        all_positions = self.find(value)
        if all_positions:
            return all_positions[0]
        return []

    # ------------------------------------------------------------------
    # TASK: slice(start, stop, step)
    # ------------------------------------------------------------------

    def slice(self, start=0, stop=None, step=1):
        if stop is None:
            stop = self.size

        start = max(0, start)
        stop = min(self.size, stop)
        if step <= 0:
            raise ValueError("step must be a positive integer")

        indices = set(range(start, stop, step))

        new_list = ExtendedLinkedList()
        current = self.head
        idx = 0

        while current and idx < stop:
            if idx in indices:
                new_list.append(current.data)
            current = current.next
            idx += 1

        return new_list

    # ------------------------------------------------------------------
    # TASK: extend(variable)
    # ------------------------------------------------------------------

    @staticmethod
    def is_iterator(obj):
        check_1 = True
        if not (hasattr(obj, '__iter__') or hasattr(obj, '__next__')):
            check_1 = False

        check_2 = True
        try:
            callable(obj.__iter__) or obj.__iter__() is obj
        except:
            check_2 = False

        return check_1 or check_2

    @staticmethod
    def is_iterable_check(obj):
        return isinstance(obj, Iterable)

    def extend(self, variable):
        if isinstance(variable, Iterator):
            for item in variable:
                self.append(item)
        elif isinstance(variable, Iterable):
            for item in variable:
                self.append(item)
        else:
            raise TypeError(f"Object of type {type(variable).__name__} is not iterable")

    # ------------------------------------------------------------------
    # TASK: tostr_index and tostr_value
    # ------------------------------------------------------------------

    def tostr_index(self, index, change_in_place=False):
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range")

        current = self.head
        for _ in range(index):
            current = current.next

        str_value = str(current.data)

        if change_in_place:
            current.data = str_value

        return str_value

    def tostr_value(self, value, change_in_place=False):
        current = self.head
        while current:
            if current.data == value:
                str_value = str(current.data)
                if change_in_place:
                    current.data = str_value
                return str_value
            current = current.next

        raise ValueError(f"Value {value} not found in the list")

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def to_list(self):
        return list(self)

    @classmethod
    def from_list(cls, lst):
        ll = cls()
        for item in lst:
            ll.append(item)
        return ll


# ========================================================================
# DEMONSTRATIONS
# ========================================================================

def demo_repr_and_size():
    print("=" * 60)
    print("TASK: __repr__() and size attribute")
    print("=" * 60)

    ll = ExtendedLinkedList()
    print(f"\nEmpty list: {repr(ll)}")
    print(f"  size = {ll.size}")

    for val in [10, 20, 30, 40, 50]:
        ll.append(val)
        print(f"append({val}): {repr(ll)}")

    ll.prepend(5)
    print(f"prepend(5):  {repr(ll)}")

    ll.delete(30)
    print(f"delete(30):  {repr(ll)}")

    print(f"\nstr():  {str(ll)}")
    print(f"repr(): {repr(ll)}")
    print(f"size:   {ll.size}")


def demo_find_index():
    print("\n" + "=" * 60)
    print("TASK: find(value) and index(value)")
    print("=" * 60)

    ll = ExtendedLinkedList.from_list([10, 20, 30, 20, 40, 20, 50])
    print(f"\nList: {ll}")

    print(f"\nfind(20): {ll.find(20)}")
    print(f"find(10): {ll.find(10)}")
    print(f"find(50): {ll.find(50)}")
    print(f"find(99): {ll.find(99)}")

    print(f"\nindex(20): {ll.index(20)}")
    print(f"index(50): {ll.index(50)}")
    print(f"index(99): {ll.index(99)}")


def demo_slice():
    print("\n" + "=" * 60)
    print("TASK: slice(start, stop, step)")
    print("=" * 60)

    ll = ExtendedLinkedList.from_list([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    print(f"\nOriginal: {ll}")

    s1 = ll.slice(2, 7)
    print(f"slice(2, 7):       {s1}")

    s2 = ll.slice(0, 10, 2)
    print(f"slice(0, 10, 2):   {s2}")

    s3 = ll.slice(1, 8, 3)
    print(f"slice(1, 8, 3):    {s3}")

    s4 = ll.slice(5)
    print(f"slice(5):          {s4}")

    s5 = ll.slice(0, 3)
    print(f"slice(0, 3):       {s5}")


def demo_extend():
    print("\n" + "=" * 60)
    print("TASK: extend(variable)")
    print("=" * 60)

    ll = ExtendedLinkedList.from_list([1, 2, 3])
    print(f"\nOriginal: {repr(ll)}")

    ll.extend([4, 5, 6])
    print(f"extend([4,5,6]):  {repr(ll)}")

    ll.extend((7, 8))
    print(f"extend((7,8)):    {repr(ll)}")

    ll.extend(map(lambda x: x * 10, [1, 2, 3]))
    print(f"extend(map(...)): {repr(ll)}")

    ll2 = ExtendedLinkedList()
    ll2.extend(range(5))
    print(f"\nNew + extend(range(5)): {repr(ll2)}")

    ll2.extend({100, 200})
    print(f"extend({{100,200}}): {repr(ll2)}")

    ll2.extend({'a': 1, 'b': 2})
    print(f"extend(dict):       {repr(ll2)}")

    print("\nType checks:")
    test_objects = [
        [1, 2, 3], {1, 2, 3}, (1, 2, 3), range(3), '123', {1: [1, 2, 3]}, 1
    ]
    for obj in test_objects:
        is_iter = ExtendedLinkedList.is_iterator(obj)
        is_iterable = ExtendedLinkedList.is_iterable_check(obj)
        print(f"  {str(obj):20s} iterator={is_iter}, iterable={is_iterable}")


def demo_tostr():
    print("\n" + "=" * 60)
    print("TASK: tostr_index() and tostr_value()")
    print("=" * 60)

    ll = ExtendedLinkedList.from_list([10, 20, 30, 40, 50])
    print(f"\nOriginal: {repr(ll)}")

    result = ll.tostr_index(2)
    print(f"\ntostr_index(2, change_in_place=False): '{result}'")
    print(f"  List: {repr(ll)}")
    print(f"  Types: {[type(x).__name__ for x in ll]}")

    result = ll.tostr_index(2, change_in_place=True)
    print(f"\ntostr_index(2, change_in_place=True):  '{result}'")
    print(f"  List: {repr(ll)}")
    print(f"  Types: {[type(x).__name__ for x in ll]}")

    ll2 = ExtendedLinkedList.from_list([100, 200, 300])
    result = ll2.tostr_value(200)
    print(f"\ntostr_value(200, change_in_place=False): '{result}'")
    print(f"  List: {repr(ll2)}")

    result = ll2.tostr_value(200, change_in_place=True)
    print(f"\ntostr_value(200, change_in_place=True):  '{result}'")
    print(f"  List: {repr(ll2)}")
    print(f"  Types: {[type(x).__name__ for x in ll2]}")


if __name__ == "__main__":
    demo_repr_and_size()
    demo_find_index()
    demo_slice()
    demo_extend()
    demo_tostr()