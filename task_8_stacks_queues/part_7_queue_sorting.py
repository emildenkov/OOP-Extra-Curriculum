from collections import deque
import random


def count_prime_divisibility(n, primes=(2, 3, 5, 7, 11)):
    if n == 0:
        return (len(primes), list(primes))

    n = abs(n)
    divisors = []
    for p in primes:
        if n % p == 0:
            divisors.append(p)
    return (len(divisors), divisors)


def sort_queue_by_divisibility(queue):

    elements = list(queue)

    def sort_key(x):
        count, _ = count_prime_divisibility(x)
        return (-count, x)

    elements.sort(key=sort_key)
    return deque(elements)


def main():
    print("=" * 70)
    print("TASK 7: Queue sorting by divisibility by 2, 3, 5, 7, 11")
    print("=" * 70)

    random.seed(42)
    queue = deque(random.randint(1, 500) for _ in range(100))

    print(f"\nOriginal queue ({len(queue)} elements):")
    elements_list = list(queue)
    for i in range(0, len(elements_list), 10):
        chunk = elements_list[i:i + 10]
        print(f"  [{i:3d}-{i + len(chunk) - 1:3d}]: {chunk}")

    # Divisibility analysis
    print(f"\n{'='*70}")
    print("DIVISIBILITY ANALYSIS")
    print("-" * 70)

    divisibility_groups = {}
    for elem in queue:
        count, divisors = count_prime_divisibility(elem)
        if count not in divisibility_groups:
            divisibility_groups[count] = []
        divisibility_groups[count].append((elem, divisors))

    for count in sorted(divisibility_groups.keys(), reverse=True):
        group = divisibility_groups[count]
        print(f"\n  Divisible by {count} of {{2,3,5,7,11}} ({len(group)} elements):")
        for val, divs in sorted(group, key=lambda x: x[0])[:15]:
            print(f"    {val:4d} -> divisors: {divs}")
        if len(group) > 15:
            print(f"    ... ({len(group) - 15} more)")

    sorted_queue = sort_queue_by_divisibility(queue)

    print(f"\n{'='*70}")
    print("SORTED QUEUE")
    print("-" * 70)
    print(f"{'Pos.':<6} {'Value':<10} {'Div.count':<10} {'Divisors':<20}")
    print("-" * 70)

    sorted_list = list(sorted_queue)
    for i, elem in enumerate(sorted_list):
        count, divisors = count_prime_divisibility(elem)
        divs_str = ", ".join(str(d) for d in divisors) if divisors else "-"
        print(f"{i + 1:<6} {elem:<10} {count:<10} {divs_str:<20}")


if __name__ == "__main__":
    main()