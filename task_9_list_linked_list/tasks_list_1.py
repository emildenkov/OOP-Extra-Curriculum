"""
Тема 9, Списък 1 - Избрани задачи:

1. Да се състави функция, която по два зададени сортирани свързани списъка,
   връща като резултат един нов сортиран списък от всички възли на двата входни списъка.

2. Да се създаде програма за обръщане на прост свързан списък (първият елемент
   става последен, вторият става предпоследен и т.н. - последният става първи).
   Да се намери алгоритъм в линейно време O(n).
   Да се реализират рекурсивен и нерекурсивен алгоритъм и да се сравнят сложностите.

3. Да се реализира стек чрез свързан списък.
"""

import time


# ========================================================================
# BASE CLASSES
# ========================================================================

class Node:

    def __init__(self, data=None):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:

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

    def is_empty(self):
        return self.head is None

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    @classmethod
    def from_list(cls, lst):
        ll = cls()
        for item in lst:
            ll.append(item)
        return ll

    def __len__(self):
        return self.size

    def __repr__(self):
        items = self.to_list()
        return " -> ".join(str(x) for x in items) + " -> None"

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


# ========================================================================
# TASK 1: Merging two sorted linked lists
# ========================================================================

def merge_sorted_lists(list1, list2):

    merged = LinkedList()
    dummy = Node(0)
    current = dummy

    p1 = list1.head
    p2 = list2.head

    while p1 and p2:
        if p1.data <= p2.data:
            current.next = Node(p1.data)
            p1 = p1.next
        else:
            current.next = Node(p2.data)
            p2 = p2.next
        current = current.next
        merged.size += 1

    remaining = p1 if p1 else p2
    while remaining:
        current.next = Node(remaining.data)
        current = current.next
        merged.size += 1
        remaining = remaining.next

    merged.head = dummy.next
    return merged


def demo_merge():
    print("=" * 60)
    print("TASK 1: Merging two sorted linked lists")
    print("=" * 60)

    list1 = LinkedList.from_list([1, 3, 5, 7, 9, 11, 15])
    list2 = LinkedList.from_list([2, 4, 6, 8, 10, 12, 14])

    print(f"\nList 1: {list1}")
    print(f"List 2: {list2}")

    merged = merge_sorted_lists(list1, list2)
    print(f"Merged: {merged}")
    print(f"Length: {merged.size}")

    list3 = LinkedList.from_list([1, 100, 200])
    list4 = LinkedList.from_list([2, 3, 4, 5, 50, 150, 250, 300])

    print(f"\nList 3: {list3}")
    print(f"List 4: {list4}")

    merged2 = merge_sorted_lists(list3, list4)
    print(f"Merged: {merged2}")

    list5 = LinkedList()
    list6 = LinkedList.from_list([1, 2, 3])
    merged3 = merge_sorted_lists(list5, list6)
    print(f"\nEmpty + [1,2,3]: {merged3}")


# ========================================================================
# TASK 2: Reversing a linked list
# ========================================================================

def reverse_iterative(linked_list):

    prev = None
    current = linked_list.head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    linked_list.head = prev
    return linked_list


def _reverse_recursive_helper(node):

    if node is None or node.next is None:
        return node

    new_head = _reverse_recursive_helper(node.next)

    node.next.next = node
    node.next = None

    return new_head


def reverse_recursive(linked_list):
    linked_list.head = _reverse_recursive_helper(linked_list.head)
    return linked_list


def demo_reverse():
    print("\n" + "=" * 60)
    print("TASK 2: Reversing a linked list")
    print("=" * 60)

    ll1 = LinkedList.from_list([1, 2, 3, 4, 5])
    print(f"\nOriginal:           {ll1}")
    reverse_iterative(ll1)
    print(f"After iterative:    {ll1}")

    ll2 = LinkedList.from_list([10, 20, 30, 40, 50])
    print(f"\nOriginal:           {ll2}")
    reverse_recursive(ll2)
    print(f"After recursive:    {ll2}")

    # Performance comparison
    print(f"\n{'='*60}")
    print("COMPLEXITY COMPARISON")
    print("-" * 60)

    sizes = [100, 1000, 5000, 10000]
    print(f"{'Size':<10} {'Iterative (ms)':<18} {'Recursive (ms)':<18}")
    print("-" * 46)

    for size in sizes:
        data = list(range(size))
        ll_iter = LinkedList.from_list(data)
        start = time.perf_counter()
        reverse_iterative(ll_iter)
        iter_time = (time.perf_counter() - start) * 1000

        ll_rec = LinkedList.from_list(data)
        import sys
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(size + 100, old_limit))
        start = time.perf_counter()
        reverse_recursive(ll_rec)
        rec_time = (time.perf_counter() - start) * 1000
        sys.setrecursionlimit(old_limit)

        print(f"{size:<10} {iter_time:<18.4f} {rec_time:<18.4f}")

    print(f"""
Theoretical analysis:
  Iterative algorithm:
    - Time:  O(n) — single pass through the list
    - Space: O(1) — only 3 extra pointers (prev, current, next)

  Recursive algorithm:
    - Time:  O(n) — n recursive calls
    - Space: O(n) — recursion stack of depth n

  Conclusion: Both have linear time complexity O(n),
  but the iterative version is more memory-efficient: O(1) vs O(n).
  For large lists, the recursive version may cause a stack overflow.
""")


# ========================================================================
# TASK 3: Stack via linked list
# ========================================================================

class StackLinkedList:

    def __init__(self):
        self._list = LinkedList()

    def push(self, data):
        self._list.prepend(data)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")

        data = self._list.head.data
        self._list.head = self._list.head.next
        self._list.size -= 1
        return data

    def peek(self):
        if self.is_empty():
            return None
        return self._list.head.data

    def is_empty(self):
        return self._list.is_empty()

    def size(self):
        return self._list.size

    def __repr__(self):
        items = self._list.to_list()
        return f"Stack(top -> {items})"

    def __iter__(self):
        return iter(self._list)


def demo_stack():
    print("=" * 60)
    print("TASK 3: Stack via linked list")
    print("=" * 60)

    stack = StackLinkedList()

    print("\nPush operations:")
    for val in [10, 20, 30, 40, 50]:
        stack.push(val)
        print(f"  push({val}) -> {stack}")

    print(f"\nPeek: {stack.peek()}")
    print(f"Size: {stack.size()}")

    print("\nPop operations:")
    while not stack.is_empty():
        val = stack.pop()
        print(f"  pop() -> {val}, stack: {stack}")

    print(f"\nIs empty? {stack.is_empty()}")

    print("\nApplication: Reversing a string via stack")
    text = "Hello World"
    stack2 = StackLinkedList()
    for char in text:
        stack2.push(char)

    reversed_text = ""
    while not stack2.is_empty():
        reversed_text += stack2.pop()

    print(f"  Original: '{text}'")
    print(f"  Reversed: '{reversed_text}'")


if __name__ == "__main__":
    demo_merge()
    demo_reverse()
    demo_stack()