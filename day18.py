from pyparsing import (
    pyparsing_common,
    ParserElement,
    oneOf,
    infixNotation,
    opAssoc,
)

import operator

ppc = pyparsing_common

ParserElement.enablePackrat()

integer = ppc.integer
operand = integer

math_op = oneOf("* +")

expr = infixNotation(
    operand,
    [
        (math_op, 2, opAssoc.LEFT),
    ],
)

opn = {
    "+": operator.add,
    "*": operator.mul,
}


def evaluate_expression(expression):
    if isinstance(expression, int):
        return expression
    if len(expression) == 1:
        return evaluate_expression(expression[0])

    op1 = evaluate_expression(expression[0])
    op = expression[1]
    op2 = evaluate_expression(expression[2])
    op1 = opn[op](op1, op2)
    return evaluate_expression([op1] + expression[3:])


def evaluate(expression, rules=expr):
    parse_stack = rules.parseString(expression)
    e = evaluate_expression(parse_stack)
    # print(f"{expression} = {e}")
    return e


assert evaluate('1 + 2') == 3
assert evaluate('3 * 4') == 12
assert evaluate('2 * 3 + (4 * 5)') == 26
assert evaluate('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert evaluate('1 + 2 * 3 + 4 * 5 + 6') == 71
assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

with open(f"inputs/day18.txt") as f:
    formulas = f.read().strip().split("\n")

total = sum(evaluate(f) for f in formulas)
print(f"Part 1 answer: {total}")
assert total == 11004703763391

## Part 2

plus_op = oneOf("+")
mult_op = oneOf("*")

new_rules = infixNotation(
    operand,
    [
        (plus_op, 2, opAssoc.LEFT),
        (mult_op, 2, opAssoc.LEFT),
    ],
)

assert evaluate('2 * 3 + (4 * 5)', new_rules) == 46
total = sum(evaluate(f, new_rules) for f in formulas)
print(f"Part 2 answer: {total}")
