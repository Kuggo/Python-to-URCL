def exp_analyzer(self):
    if len(self) == 0:
        return
    operator = self[0]
    precedence = {
        'tt_right_parent': 0,
        'tt_left_parent': 0,
        'tt_pow': 1,
        'tt_bitwise_not': 2,
        'tt_mlt': 3,
        'tt_mod': 3,
        'tt_float_div': 3,
        'tt_div': 3,
        'tt_plus': 4,
        'tt_minus': 4,
        'tt_rightshift': 5,
        'tt_leftshift': 5,
        'tt_bitwise_and': 6,
        'tt_bitwise_xor': 7,
        'tt_bitwise_or': 8,
        'tt_equal': 9,
        'tt_not_equal': 9,
        'tt_greater': 9,
        'tt_greater_equal': 9,
        'tt_less': 9,
        'tt_less_equal': 9,
        'tt_is': 9,
        'tt_in': 9,
        'tt_not': 10,
        'tt_and': 11,
        'tt_or': 12,
    }
    stack = []
    queue = []
    while len(self) != 0:
        operator = self.pop()
    if ':' in operator:  # operator is {'tt_var:', 'tt_int:', 'tt_float:', 'tt_function_call:', 'tt_string:'}:
        queue.append(operator)

    elif operator == '(':
        stack.append(operator)
    elif operator == ')':
        while stack[len(stack)] != '(':
            queue.append(stack.pop())

    elif precedence[operator] <= precedence[stack[len(stack)]]:

    return queue
