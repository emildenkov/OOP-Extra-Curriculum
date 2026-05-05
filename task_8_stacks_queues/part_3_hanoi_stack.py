
class Stack:

    def __init__(self, name=""):
        self._items = []
        self.name = name

    def push(self, item):
        self._items.append(item)

    def is_empty(self):
        return len(self._items) == 0

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self.name}): {self._items}"

    def items(self):
        return list(self._items)


class HanoiTowers:

    def __init__(self, n_disks):
        self.n_disks = n_disks
        self.moves = []
        self.move_count = 0

        self.source = Stack("A (Source)")
        self.auxiliary = Stack("B (Auxiliary)")
        self.target = Stack("C (Target)")

        for disk in range(n_disks, 0, -1):
            self.source.push(disk)

    def _move_disk(self, from_stack, to_stack):
        if from_stack.is_empty():
            raise ValueError(f"Peg {from_stack.name} is empty!")

        disk = from_stack.pop()

        if not to_stack.is_empty() and to_stack.peek() < disk:
            from_stack.push(disk)
            raise ValueError(f"Invalid move: disk {disk} cannot go on top of disk {to_stack.peek()}")

        to_stack.push(disk)
        self.move_count += 1
        self.moves.append((disk, from_stack.name, to_stack.name))

    def _hanoi_recursive(self, n, source, target, auxiliary):
        if n == 1:
            self._move_disk(source, target)
            return

        self._hanoi_recursive(n - 1, source, auxiliary, target)
        self._move_disk(source, target)
        self._hanoi_recursive(n - 1, auxiliary, target, source)

    def solve(self):
        print("=" * 60)
        print(f"TOWER OF HANOI - {self.n_disks} disks")
        print("=" * 60)

        self._print_state("Initial state")
        self._hanoi_recursive(self.n_disks, self.source, self.target, self.auxiliary)
        self._print_state("Final state")

        print(f"\nTotal moves: {self.move_count}")
        print(f"Theoretical minimum: {2**self.n_disks - 1}")

        return self.moves

    def _print_state(self, label=""):
        if label:
            print(f"\n--- {label} ---")
        print(f"  {self.source}")
        print(f"  {self.auxiliary}")
        print(f"  {self.target}")

    def print_moves(self):
        print(f"\nList of moves:")
        print("-" * 45)
        for i, (disk, fr, to) in enumerate(self.moves, 1):
            print(f"  Move {i:3d}: Disk {disk} from {fr[:1]} -> {to[:1]}")

    def visualize(self):
        print("=" * 60)
        print(f"VISUALIZATION - TOWER OF HANOI ({self.n_disks} disks)")
        print("=" * 60)

        src = Stack("A")
        aux = Stack("B")
        tgt = Stack("C")
        for d in range(self.n_disks, 0, -1):
            src.push(d)

        stacks = {"A": src, "B": aux, "C": tgt}

        def print_towers():
            max_h = self.n_disks
            a_items = src.items()
            b_items = aux.items()
            c_items = tgt.items()

            for level in range(max_h - 1, -1, -1):
                a_val = str(a_items[level]) if level < len(a_items) else "|"
                b_val = str(b_items[level]) if level < len(b_items) else "|"
                c_val = str(c_items[level]) if level < len(c_items) else "|"
                print(f"    {a_val:^7} {b_val:^7} {c_val:^7}")
            print(f"    {'=A=':^7} {'=B=':^7} {'=C=':^7}")

        print("\nStart:")
        print_towers()

        for i, (disk, fr_name, to_name) in enumerate(self.moves, 1):
            fr_key = fr_name[0]
            to_key = to_name[0]
            stacks[fr_key].pop()
            stacks[to_key].push(disk)
            print(f"\nMove {i}: Disk {disk} ({fr_key} -> {to_key})")
            print_towers()


if __name__ == "__main__":
    hanoi = HanoiTowers(4)
    hanoi.solve()
    hanoi.print_moves()

    print("\n")

    hanoi3 = HanoiTowers(3)
    hanoi3.solve()
    hanoi3.visualize()