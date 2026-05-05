from collections import deque
import math


def find_valid_combinations(min_count=30):
    combinations = []
    for a in range(0, 20):
        for c in range(0, 20):
            product = a * c
            b = math.isqrt(product)
            if b * b == product:
                combinations.append((a, b, c))
                if b != 0:
                    combinations.append((a, -b, c))
            if len(combinations) >= min_count * 3:
                break
        if len(combinations) >= min_count * 3:
            break
    return combinations


def compute_fx(a, b, c, x=None):
    if x is not None:
        return a * x**2 - 2 * b * x + c
    if a != 0:
        root = b / a
        return f"f(x) = {a}x^2 - {2*b}x + {c}, root x = {root:.4f}"
    elif b != 0:
        root = c / (2 * b)
        return f"f(x) = -{2*b}x + {c}, root x = {root:.4f}"
    else:
        return f"f(x) = {c} (constant)"


def classify_combination(a, c):
    if a == c:
        return "equal"
    elif a < c:
        return "less"
    else:
        return "greater"


def build_queue(combinations):
    equal_pool = deque()
    less_pool = deque()
    greater_pool = deque()

    for combo in combinations:
        a, b, c = combo
        cat = classify_combination(a, c)
        if cat == "equal":
            equal_pool.append(combo)
        elif cat == "less":
            less_pool.append(combo)
        else:
            greater_pool.append(combo)

    print(f"Available combinations: a==c: {len(equal_pool)}, a<c: {len(less_pool)}, a>c: {len(greater_pool)}")

    queue = deque()
    position = 0
    max_iterations = len(equal_pool) + len(less_pool) + len(greater_pool)

    for _ in range(max_iterations):
        slot = position % 3

        if slot == 0 and equal_pool:
            queue.append(equal_pool.popleft())
            position += 1
        elif slot == 1 and less_pool:
            queue.append(less_pool.popleft())
            position += 1
        elif slot == 2 and greater_pool:
            queue.append(greater_pool.popleft())
            position += 1
        else:
            position += 1

        if not equal_pool and not less_pool and not greater_pool:
            break

    return queue


def remove_odd_equal(queue):
    removed = deque()
    remaining = deque()

    for combo in queue:
        a, b, c = combo
        if a == c and a % 2 == 1:
            removed.append(combo)
        else:
            remaining.append(combo)

    return remaining, removed


def build_dictionaries(queue):
    dict_equal = {}
    dict_less = {}
    dict_greater = {}

    for combo in queue:
        a, b, c = combo
        fx_str = compute_fx(a, b, c)
        cat = classify_combination(a, c)

        if cat == "equal":
            dict_equal[(a, b, c)] = fx_str
        elif cat == "less":
            dict_less[(a, b, c)] = fx_str
        else:
            dict_greater[(a, b, c)] = fx_str

    return dict_equal, dict_less, dict_greater


def main():
    print("=" * 70)
    print("TASK 2: Quadratic equation f(x) = a*x^2 - 2*b*x + c")
    print("Condition: D = b^2 - a*c = 0 (single real root)")
    print("=" * 70)

    combinations = find_valid_combinations(30)
    print(f"\nFound {len(combinations)} valid combinations (a, b, c):")
    for i, (a, b, c) in enumerate(combinations[:35], 1):
        print(f"  {i:3d}. a={a}, b={b}, c={c}  |  b^2={b**2}, a*c={a*c}  |  {compute_fx(a, b, c)}")

    print(f"\n{'='*70}")
    print("BUILDING THE QUEUE")
    queue = build_queue(combinations)

    print(f"\nQueue after building ({len(queue)} elements):")
    for i, combo in enumerate(queue, 1):
        a, b, c = combo
        cat = classify_combination(a, c)
        label = {"equal": "a==c", "less": "a<c", "greater": "a>c"}[cat]
        print(f"  Position {i:3d}: ({a},{b},{c}) [{label}]")

    print(f"\n{'='*70}")
    print("REMOVAL: f(x) where a==c and a is odd")
    queue, removed = remove_odd_equal(queue)
    print(f"Removed: {len(removed)}")
    for combo in removed:
        print(f"  -> ({combo[0]}, {combo[1]}, {combo[2]})")
    print(f"Remaining in queue: {len(queue)}")

    print(f"\n{'='*70}")
    print("DICTIONARIES BY CATEGORY")
    dict_equal, dict_less, dict_greater = build_dictionaries(queue)

    print(f"\n--- Dictionary a == c ({len(dict_equal)} entries) ---")
    for key, val in dict_equal.items():
        print(f"  {key}: {val}")

    print(f"\n--- Dictionary a < c ({len(dict_less)} entries) ---")
    for key, val in dict_less.items():
        print(f"  {key}: {val}")

    print(f"\n--- Dictionary a > c ({len(dict_greater)} entries) ---")
    for key, val in dict_greater.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    main()