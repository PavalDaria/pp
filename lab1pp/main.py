def is_operator(a):
    return a in ['+', '-', '*', '/']


def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0


def apply_operator(op, a, b):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b


def infix_to_postfix(expr):
    stack = []
    postfix = []
    num = ""
    for char in expr:
        if char.isdigit() or char == '.':
            num += char
        else:
            if num:
                postfix.append(num)
                num = ""
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            elif is_operator(char):
                while stack and precedence(stack[-1]) >= precedence(char):
                    postfix.append(stack.pop())
                stack.append(char)
    if num:
        postfix.append(num)
    while stack:
        postfix.append(stack.pop())
    return postfix


def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if token.isdigit() or '.' in token:
            stack.append(float(token))
        elif is_operator(token):
            b = stack.pop()
            a = stack.pop()
            result = apply_operator(token, a, b)
            stack.append(result)
    return stack.pop()


def main():
    expression = "2*(4-5/6)/456"
    print(f"expr initiala: {expression}")
    postfix = infix_to_postfix(expression)
    print(f"expr postfixata: {' '.join(postfix)}")
    result = evaluate_postfix(postfix)
    print(f"rez evaluarii: {result}")


if __name__=="__main__":
    main()