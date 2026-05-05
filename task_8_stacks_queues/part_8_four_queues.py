from collections import deque
import random


class StoreQueues:

    def __init__(self, seed=42):
        random.seed(seed)

        self.queue1 = deque(sorted(random.sample(range(1, 101), 36)))
        self.queue2 = deque(sorted(random.sample(range(101, 201), 24)))
        self.queue3 = deque(sorted(random.sample(range(201, 301), 24)))
        self.queue4 = deque()

    def print_queues(self, label=""):
        if label:
            print(f"\n--- {label} ---")
        print(f"  Queue 1 ({len(self.queue1):2d} people): {list(self.queue1)}")
        print(f"  Queue 2 ({len(self.queue2):2d} people): {list(self.queue2)}")
        print(f"  Queue 3 ({len(self.queue3):2d} people): {list(self.queue3)}")
        print(f"  Queue 4 ({len(self.queue4):2d} people): {list(self.queue4)}")
        total = len(self.queue1) + len(self.queue2) + len(self.queue3) + len(self.queue4)
        print(f"  Total: {total} people")

    @staticmethod
    def extract_every_nth(queue, n):
        remaining = deque()
        extracted = deque()

        for i, person in enumerate(queue, 1):
            if i % n == 0:
                extracted.append(person)
            else:
                remaining.append(person)

        return remaining, extracted

    def iteration_1(self):
        print("\n" + "=" * 70)
        print("ITERATION 1: Opening register 4")
        print("=" * 70)

        self.queue1, from_q1 = self.extract_every_nth(self.queue1, 3)
        print(f"\n  From queue 1 (every 3rd): {list(from_q1)} ({len(from_q1)} people)")

        self.queue2, from_q2 = self.extract_every_nth(self.queue2, 4)
        print(f"  From queue 2 (every 4th): {list(from_q2)} ({len(from_q2)} people)")

        self.queue3, from_q3 = self.extract_every_nth(self.queue3, 6)
        print(f"  From queue 3 (every 6th): {list(from_q3)} ({len(from_q3)} people)")

        self.queue4.extend(from_q1)
        self.queue4.extend(from_q2)
        self.queue4.extend(from_q3)

        self.print_queues("After iteration 1")

    def iteration_2(self):
        print("\n" + "=" * 70)
        print("ITERATION 2: Balancing")
        print("=" * 70)

        total = len(self.queue1) + len(self.queue2) + len(self.queue3) + len(self.queue4)
        equilibrium = total // 4
        remainder = total % 4

        print(f"\n  Total people: {total}")
        print(f"  Equilibrium count per queue: {equilibrium}")
        print(f"  Remainder (distributed to first queues): {remainder}")

        sizes = {
            1: len(self.queue1),
            2: len(self.queue2),
            3: len(self.queue3),
            4: len(self.queue4)
        }

        print(f"\n  Current sizes: {sizes}")
        print(f"  Required changes:")
        for q_num, size in sizes.items():
            target = equilibrium + (1 if q_num <= remainder else 0)
            diff = size - target
            if diff > 0:
                print(f"    Queue {q_num}: needs to decrease by {diff} (from {size} to {target})")
            elif diff < 0:
                print(f"    Queue {q_num}: needs to increase by {abs(diff)} (from {size} to {target})")
            else:
                print(f"    Queue {q_num}: no change ({size})")

        pool = deque()

        target_4 = equilibrium + (1 if 4 <= remainder else 0)
        excess_4 = len(self.queue4) - target_4
        if excess_4 > 0:
            for _ in range(excess_4):
                if self.queue4:
                    pool.append(self.queue4.popleft())
            print(f"\n  From queue 4: {excess_4} people moved to pool")

        extraction_rules = {1: 3, 2: 4, 3: 6}
        for q_num, nth in extraction_rules.items():
            q_ref = [self.queue1, self.queue2, self.queue3][q_num - 1]
            target_q = equilibrium + (1 if q_num <= remainder else 0)
            if len(q_ref) > target_q:
                excess = len(q_ref) - target_q
                remaining, extracted = self.extract_every_nth(q_ref, nth)
                actual_extract = min(len(extracted), excess)
                for i in range(actual_extract):
                    pool.append(extracted[i])
                for i in range(actual_extract, len(extracted)):
                    remaining.append(extracted[i])

                if q_num == 1:
                    self.queue1 = remaining
                elif q_num == 2:
                    self.queue2 = remaining
                elif q_num == 3:
                    self.queue3 = remaining

                if actual_extract > 0:
                    print(f"  From queue {q_num}: {actual_extract} people moved to pool")

        queues = [self.queue1, self.queue2, self.queue3, self.queue4]

        while pool:
            min_size = min(len(q) for q in queues)
            for q in queues:
                if len(q) == min_size and pool:
                    q.append(pool.popleft())
                    break

        self.print_queues("After iteration 2 (balanced)")

        sizes_final = [len(self.queue1), len(self.queue2), len(self.queue3), len(self.queue4)]
        max_diff = max(sizes_final) - min(sizes_final)
        print(f"\n  Max difference between queues: {max_diff}")
        print(f"  Final sizes: {sizes_final}")


def main():
    print("=" * 70)
    print("TASK 8: Four store queues with balancing")
    print("=" * 70)

    store = StoreQueues(seed=42)
    store.print_queues("Initial state")

    store.iteration_1()
    store.iteration_2()


if __name__ == "__main__":
    main()