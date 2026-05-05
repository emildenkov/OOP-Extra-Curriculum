from collections import deque
import random


class DynamicQueue:

    def __init__(self, size=100, seed=42):
        self.queue = deque()
        self.history = []
        random.seed(seed)

        for _ in range(size):
            self.queue.append(random.randint(1, 200))

    def process(self, max_iterations=None):
        iteration = 0
        if max_iterations is None:
            max_iterations = 200

        print("=" * 70)
        print("TASK 6: Queue with entry/exit rules")
        print("=" * 70)
        print(f"\nInitial queue ({len(self.queue)} elements):")
        print(f"  {list(self.queue)[:20]}... (first 20)")

        while iteration < max_iterations:
            found_odd = False
            temp_queue = deque()
            current_index = 0

            while self.queue:
                element = self.queue.popleft()

                if element % 2 == 1 and not found_odd:
                    found_odd = True
                    index_of_element = current_index
                    value_of_element = element

                    difference = abs(index_of_element - value_of_element)

                    if difference < 8:
                        new_element = 2 ** difference
                    else:
                        new_element = 2 ** 3

                    self.history.append({
                        'iteration': iteration + 1,
                        'exited': element,
                        'exit_index': index_of_element,
                        'difference': difference,
                        'entered': new_element,
                        'queue_size': len(temp_queue) + len(self.queue) + 1
                    })

                    temp_queue.append(new_element)
                else:
                    temp_queue.append(element)

                current_index += 1

            self.queue = temp_queue

            if not found_odd:
                print(f"\nNo more odd elements. Stopping after {iteration} iterations.")
                break

            iteration += 1

        return self.queue

    def print_results(self, show_history=True, history_limit=30):
        if show_history:
            print(f"\nOperation history (showing {min(history_limit, len(self.history))}):")
            print("-" * 70)
            print(f"{'Iter':<5} {'Exited':<10} {'Index':<8} {'|Diff|':<8} {'Entered':<10} {'Size':<8}")
            print("-" * 70)
            for h in self.history[:history_limit]:
                print(f"{h['iteration']:<5} {h['exited']:<10} {h['exit_index']:<8} "
                      f"{h['difference']:<8} {h['entered']:<10} {h['queue_size']:<8}")

            if len(self.history) > history_limit:
                print(f"  ... ({len(self.history) - history_limit} more operations)")

        print(f"\nFinal queue ({len(self.queue)} elements):")
        print(f"  {list(self.queue)}")

        print(f"\nStatistics:")
        print(f"  Total iterations: {len(self.history)}")
        if self.history:
            total_exited = sum(h['exited'] for h in self.history)
            total_entered = sum(h['entered'] for h in self.history)
            print(f"  Sum of exited values: {total_exited}")
            print(f"  Sum of entered values: {total_entered}")

        all_even = all(x % 2 == 0 for x in self.queue)
        print(f"  All remaining are even: {'Yes' if all_even else 'No'}")


if __name__ == "__main__":
    dq = DynamicQueue(100, seed=42)
    dq.process()
    dq.print_results()