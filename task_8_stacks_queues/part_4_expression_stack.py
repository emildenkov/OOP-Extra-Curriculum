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

    def items(self):
        return list(self._items)

    def __repr__(self):
        return f"Stack: {self._items}"


def tokenize(expression):
    tokens = []
    i = 0
    expression = expression.replace(" ", "")

    while i < len(expression):
        char = expression[i]

        if char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i + 1].isdigit()):
            num_str = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
            continue

        if char == '-' and (not tokens or tokens[-1] in ['(', '+', '-', '*', '/', '//', '%', '^']):
            num_str = "-"
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            if len(num_str) > 1:
                tokens.append(float(num_str) if '.' in num_str else int(num_str))
                continue
            else:
                tokens.append('-')
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


def get_precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/', '//', '%'):
        return 2
    if op == '^':
        return 3
    return 0


def is_operator(token):
    return token in ('+', '-', '*', '/', '//', '%', '^')


def remove_unmatched_brackets(tokens):
    stack = Stack()
    unmatched_indices = set()

    for i, token in enumerate(tokens):
        if token == '(':
            stack.push(i)
        elif token == ')':
            if not stack.is_empty():
                stack.pop()
            else:
                unmatched_indices.add(i)

    while not stack.is_empty():
        unmatched_indices.add(stack.pop())

    removed_count = len(unmatched_indices)
    cleaned_tokens = [t for i, t in enumerate(tokens) if i not in unmatched_indices]

    return cleaned_tokens, removed_count


def infix_to_postfix(tokens):
    output = []
    operator_stack = Stack()

    for token in tokens:
        if isinstance(token, (int, float)):
            output.append(token)
        elif is_operator(token):
            while (not operator_stack.is_empty() and
                   operator_stack.peek() != '(' and
                   is_operator(operator_stack.peek()) and
                   get_precedence(operator_stack.peek()) >= get_precedence(token)):
                output.append(operator_stack.pop())
            operator_stack.push(token)
        elif token == '(':
            operator_stack.push(token)
        elif token == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                output.append(operator_stack.pop())
            if not operator_stack.is_empty():
                operator_stack.pop()

    while not operator_stack.is_empty():
        output.append(operator_stack.pop())

    return output


def evaluate_postfix(postfix_tokens):
    eval_stack = Stack()

    for token in postfix_tokens:
        if isinstance(token, (int, float)):
            eval_stack.push(token)
        elif is_operator(token):
            if eval_stack.size() < 2:
                raise ValueError(f"Invalid expression: not enough operands for '{token}'")

            b = eval_stack.pop()
            a = eval_stack.pop()

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = a / b
            elif token == '//':
                if b == 0:
                    raise ZeroDivisionError("Integer division by zero")
                result = a // b
            elif token == '%':
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                result = a % b
            elif token == '^':
                result = a ** b
            else:
                raise ValueError(f"Unknown operator: {token}")

            eval_stack.push(result)

    if eval_stack.size() == 1:
        return eval_stack.pop()
    else:
        raise ValueError("Invalid expression")


def expression_to_stack(expression):
    tokens = tokenize(expression)
    stack = Stack()
    for token in tokens:
        stack.push(token)
    return stack, tokens


def process_expression(expression):
    print(f"\nExpression: {expression}")
    print("-" * 50)

    stack, tokens = expression_to_stack(expression)
    print(f"Tokens: {tokens}")
    print(f"Stack: {stack}")

    cleaned_tokens, removed_count = remove_unmatched_brackets(tokens)
    print(f"Cleaned tokens: {cleaned_tokens}")
    print(f"Removed brackets: {removed_count}")

    try:
        postfix = infix_to_postfix(cleaned_tokens)
        print(f"Postfix notation: {postfix}")

        result = evaluate_postfix(postfix)
        print(f"Result: {result}")
        return result, removed_count
    except Exception as e:
        print(f"Evaluation error: {e}")
        return None, removed_count


def main():
    print("=" * 60)
    print("TASK 4: Mathematical expression via stack")
    print("=" * 60)

    test_expressions = [
        "3 + 5 * 2",
        "(3 + 5) * 2",
        "2 ^ 3 + 1",
        "10 // 3 + 10 % 3",
        "((3 + 5) * (2 - 1)",
        "(3 + 5)) * 2",
        "((2 + 3) * (4 - 1))",
        "((1 + 2) * (3 + 4) - (5",
        "3 + ) 5 ( * 2",
    ]

    for expr in test_expressions:
        process_expression(expr)
        print()


if __name__ == "__main__":
    main()