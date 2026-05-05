class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack: {self._items}"


def tokenize(expression):

    tokens = []
    i = 0
    expression = expression.replace(" ", "")

    while i < len(expression):
        char = expression[i]

        if char.isdigit() or char == '.':
            num_str = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(num_str)
            continue

        if char == '/' and i + 1 < len(expression) and expression[i + 1] == '/':
            tokens.append('//')
            i += 2
            continue

        if char in '+-*/%^()':
            tokens.append(char)
            i += 1
            continue

        if char == '/':
            tokens.append('/')
            i += 1
            continue

        i += 1

    return tokens


def expression_to_stack(tokens):
    stack = Stack()
    for token in tokens:
        stack.push(token)
    return stack


def check_brackets(tokens):
    stack = Stack()
    issues = []

    for i, token in enumerate(tokens):
        if token == '(':
            stack.push(i)
        elif token == ')':
            if stack.is_empty():
                issues.append(('extra_close', i))
            else:
                stack.pop()

    while not stack.is_empty():
        issues.append(('extra_open', stack.pop()))

    return len(issues) == 0, issues


def fix_brackets(tokens):
    is_valid, issues = check_brackets(tokens)

    if is_valid:
        return tokens, 0, []

    fixed_tokens = list(tokens)
    additions = []

    stack = Stack()
    unmatched_close = []
    unmatched_open = []

    for i, token in enumerate(fixed_tokens):
        if token == '(':
            stack.push(i)
        elif token == ')':
            if stack.is_empty():
                unmatched_close.append(i)
            else:
                stack.pop()

    while not stack.is_empty():
        unmatched_open.append(stack.pop())

    insertions = []

    for pos in unmatched_close:
        insert_pos = _find_subexpression_start(fixed_tokens, pos)
        insertions.append((insert_pos, '('))
        additions.append(f"Added '(' at position {insert_pos} (before token '{fixed_tokens[insert_pos]}')")

    for pos in sorted(unmatched_open):
        insert_pos = _find_subexpression_end(fixed_tokens, pos)
        insertions.append((insert_pos + 1, ')'))
        additions.append(f"Added ')' after position {insert_pos} (after token '{fixed_tokens[insert_pos]}')")

    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, bracket in insertions:
        fixed_tokens.insert(pos, bracket)

    return fixed_tokens, len(insertions), additions


def _find_subexpression_start(tokens, close_pos):
    i = close_pos - 1
    depth = 0
    while i >= 0:
        if tokens[i] == ')':
            depth += 1
        elif tokens[i] == '(':
            if depth == 0:
                return i
            depth -= 1
        i -= 1
    return 0


def _find_subexpression_end(tokens, open_pos):
    i = open_pos + 1
    depth = 0
    while i < len(tokens):
        if tokens[i] == '(':
            depth += 1
        elif tokens[i] == ')':
            if depth == 0:
                return i
            depth -= 1
        i += 1
    return len(tokens) - 1


def process_expression(expression):
    print(f"\nExpression: \"{expression}\"")
    print("-" * 55)

    tokens = tokenize(expression)
    print(f"Tokens: {tokens}")

    stack = expression_to_stack(tokens)
    print(f"Stack: {stack}")

    is_valid, issues = check_brackets(tokens)

    if is_valid:
        print("All brackets are properly matched!")
    else:
        print(f"Brackets are NOT valid. Issues: {len(issues)}")
        for issue_type, pos in issues:
            if issue_type == 'extra_close':
                print(f"  -> Extra ')' at position {pos}")
            else:
                print(f"  -> Unmatched '(' at position {pos}")

        fixed_tokens, added_count, additions = fix_brackets(tokens)
        print(f"\nBrackets added: {added_count}")
        for desc in additions:
            print(f"  -> {desc}")

        fixed_expr = " ".join(str(t) for t in fixed_tokens)
        print(f"Fixed expression: \"{fixed_expr}\"")

        is_now_valid, _ = check_brackets(fixed_tokens)
        print(f"Valid after fix: {'Yes' if is_now_valid else 'No'}")


def main():
    print("=" * 60)
    print("TASK 5: Bracket validation and auto-fix")
    print("=" * 60)

    test_expressions = [
        "(3 + 5) * 2",
        "((3 + 5) * 2",
        "(3 + 5)) * 2",
        "((1 + 2) * (3 + 4)",
        "3 + 5) * (2 + 1",
        "((2 + 3) * ((4 - 1)",
        "(((1 + 2)))",
        "1 + 2) * (3 + 4) - (5",
    ]

    for expr in test_expressions:
        process_expression(expr)
        print()


if __name__ == "__main__":
    main()