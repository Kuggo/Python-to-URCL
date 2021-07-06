

def token_creator(self):
    self = remove_comments(self)
    self = indentation(self)
    program_tokens = []
    indent_line = []
    for i in self:
        tokens = []
        i = i.split(' ', 1)
        indent = int((i[0])[3:])
        i = i[1]
        indent_line.append(indent)
        j = 0
        max_length = len(i)-1
        while j < (max_length + 1):
            while i[j] == ' ' and j < max_length:  # ignore empty spaces
                j += 1
            if i[j] == '#':
                j = max_length
                break

            if i[j] == '!':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_not_equal')
                    else:
                        print('SyntaxError: illegal character "!" used (line {0}, char {1})'.format(str(i),
                                                                                                    str(j)))

                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '=':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_equal')
                    else:
                        tokens.append('tt_assign')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '+':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_plus_assign')
                    else:
                        tokens.append('tt_plus')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '-':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_minus_assign')
                    else:
                        tokens.append('tt_minus')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '%':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_mod_assign')
                    else:
                        tokens.append('tt_mod')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '/':
                try:
                    if i[j + 1] == '/' and i[j + 2] == '=':
                        j += 2
                        tokens.append('tt_div_assign')
                    elif i[j + 1] == '/':
                        j += 1
                        tokens.append('tt_div')
                    elif i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_float_div_assign')
                    else:
                        tokens.append('tt_float_div')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '*':
                try:
                    if i[j + 1] == '*' and i[j + 2] == '=':
                        j += 2
                        tokens.append('tt_pow_assign')
                    elif i[j + 1] == '*':
                        j += 1
                        tokens.append('tt_pow')
                    elif i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_mlt_assign')
                    else:
                        tokens.append('tt_mlt')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '&':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_bitwise_and_assign')
                    else:
                        tokens.append('tt_bitwise_and')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '|':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_bitwise_or_assign')
                    else:
                        tokens.append('tt_bitwise_or')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '^':
                try:
                    if i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_bitwise_xor_assign')
                    else:
                        tokens.append('tt_bitwise_xor')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '<':
                try:
                    if i[j + 1] == '<' and i[j + 2] == '=':
                        j += 2
                        tokens.append('tt_leftshift_assign')
                    elif i[j + 1] == '<':
                        j += 1
                        tokens.append('tt_leftshift')
                    elif i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_less_equal')
                    else:
                        tokens.append('tt_less')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '>':
                try:
                    if i[j + 1] == '>' and i[j + 2] == '=':
                        j += 2
                        tokens.append('tt_rightshift_assign')
                    elif i[j + 1] == '>':
                        j += 1
                        tokens.append('tt_rightshift')
                    elif i[j + 1] == '=':
                        j += 1
                        tokens.append('tt_greater_equal')
                    else:
                        tokens.append('tt_greater')
                except:
                    print('SyntaxError: expression expected (line {0}, char {1})'.format(str(i), str(j)))

            elif i[j] == '(':
                j_copy = j + 1
                maybe_tuple = ''
                comma = False
                while i[j_copy] != ')':
                    maybe_tuple += i[j_copy]
                    if i[j_copy] == ',':
                        comma = True
                    if j_copy < max_length:
                        j_copy += 1
                if comma:
                    tokens.append('tt_tuple:' + maybe_tuple)
                    j = j_copy

            elif i[j] == '{':
                dict_set = ''
                colon = False
                while i[j] != '}':
                    dict_set += i[j]
                    if i[j] == ':':
                        colon = True
                    if j < max_length:
                        i += 1
                if colon:
                    tokens.append('tt_dict:' + dict_set)
                else:
                    tokens.append('tt_set:' + dict_set)
                    
            elif i[j] in '{}[]():~,.':
                tokens.append(check_symbol(i[j]))

            elif i[j] == '"':
                string = ''
                j += 1
                while i[j] != '"':
                    string += i[j]
                    j += 1
                tokens.append('tt_string:' + string)
            elif i[j] == "'":
                string = ''
                j += 1
                while i[j] != "'":
                    string += i[j]
                    j += 1
                tokens.append('tt_string:' + string)
            else:
                if i[j] in '0123456789.':
                    number = ''
                    while i[j] in '0123456789abcdefABCDEF.':
                        number += i[j]
                        if j < max_length:
                            j += 1
                        else:
                            break
                    str_to_num(number)
                elif i[j] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                    name = ''
                    while i[j] in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                        name += i[j]
                        if j < max_length:
                            j += 1
                        else:
                            break

                    if i[j] == '(':
                        tokens.append(check_name2(name))
                        tokens.append('tt_left_parent')

                    else:
                        tokens.append(check_name(name))

                else:
                    pass  # throw off some error of illegal character
            j += 1
        program_tokens.append(tokens)
    return [indent_line, program_tokens]


# helper functions
def remove_comments(self):
    i = 0
    output = ''
    commented = False
    while i < len(self):
        if self[i] == '"':  # remove multi line strings with "
            try:
                if self[i + 1] == '"' and self[i + 2] == '"' and not commented:
                    i += 3
                    commented = True
                elif self[i + 1] == '"' and self[i + 2] == '"' and commented:
                    i += 3
                    commented = False
            except:
                pass
        elif self[i] == "'":  # remove multi line strings with '
            try:
                if self[i + 1] == "'" and self[i + 2] == "'" and not commented:
                    i += 3
                    commented = True
                elif self[i + 1] == "'" and self[i + 2] == "'" and commented:
                    i += 3
                    commented = False
            except:
                pass
        if not commented:
            output += self[i]
        i += 1
    return output


def indentation(self):
    self = self.split('\n')
    indent = 0
    output = []
    for i in self:
        space_num = 0
        if i[0] == ' ':
            j = 0
            while i[j] == ' ':
                space_num += 1
                j += 1
            i = i[j:]
            indent = space_num // 4
        output.append('id:' + str(indent) + ' ' + i)
    return output


def str_to_num(self):
    self = self.lower()
    if self[0] == '0' and self[1] == 'b':
        charset = "01"
        output = self[2:]
        for x in output:
            if x not in charset:
                print('SyntaxError: illegal character used')
        output = int(output, 2)

    elif self[0] == '0' and self[1] == 'x':
        charset = "0123456789abcdef"
        output = self[2:]
        for x in output:
            test = False
            for y in charset:
                if x == y:
                    test = True
            if not test:
                print('SyntaxError: illegal character used')
        output = int(output, 16)

    else:
        if self[0] == '0' and self[1] == 'd':
            self = self[2:]
        char_set = "0123456789."
        point_count = 0
        t_type = 'int'
        output = self
        for x in output:
            test = False
            for y in char_set:
                if x == y:
                    test = True
                if x == '.':
                    point_count += 1
                    t_type = 'float'
            if not test:
                print('SyntaxError: illegal character used')
            if point_count > 1:
                print('SyntaxError: Only 1 radix point allowed')
        if t_type == 'int':
            output = int(output)
        else:
            output = float(output)
    return output


def check_symbol(self):  # remove some of the items here to the main program
    symbols = {
        '~': 'tt_bitwise_not',
        '.': 'tt_dot',
        ',': 'tt_comma',
        ':': 'tt_colon',
        '(': 'tt_left_parent',
        ')': 'tt_right_parent',
        '[': 'tt_left_bracket',
        ']': 'tt_right_bracket',
        '{': 'tt_left_curved_bracket',
        '}': 'tt_right_curved_bracket'
    }
    return symbols[self]


def check_name(self):
    # check keywords
    keywords = {
        'def': 'tt_def',
        'if': 'tt_if',
        'elif': 'tt_elif',
        'else': 'tt_else',
        'while': 'tt_while',
        'for': 'tt_for',
        'break': 'tt_break',
        'continue': 'tt_continue',
        'return': 'tt_return',
        'import': 'tt_import',
        'or': 'tt_or',
        'not': 'tt_not',
        'and': 'tt_and',
        'in': 'tt_in',
        'is': 'tt_is',
        'try': 'tt_try',
        'except': 'tt_except',
        'True': 'tt_true',
        'False': 'tt_false',
        'None': 'tt_none',
        'class': 'tt_class',
        'from': 'tt_from',
        'global': 'tt_global',
        'pass': 'tt_pass',
        'raise': 'tt_raise',
        'del': 'tt_del',
        'as': 'tt_as',
        'assert': 'tt_assert',
        'async': 'tt_async',
        'lambda': 'tt_lambda',
        'with': 'tt_with',
        'await': 'tt_await',
        'finally': 'tt_finally',
        'nonlocal': 'tt_nonlocal',
        'yield': 'tt_yield'
    }
    try:
        if keywords[self] is not None:
            return keywords[self]
    except:
        return 'tt_var:' + self


def check_name2(self):
    # check built in functions
    builtin_functions = {
        'abs': 'tt_builtin_abs',
        'all': 'tt_builtin_all',
        'any': 'tt_builtin_any',
        'ascii': 'tt_builtin_ascii',
        'bin': 'tt_builtin_bin',
        'bool': 'tt_builtin_bool',
        'bytearray': 'tt_builtin_bytearray',
        'bytes': 'tt_builtin_bytes',
        'callable': 'tt_builtin_callable',
        'chr': 'tt_builtin_chr',
        'classmethod': 'tt_builtin_classmethod',
        'compile': 'tt_builtin_compile',
        'complex': 'tt_builtin_complex',
        'delattr': 'tt_builtin_delattr',
        'dict': 'tt_builtin_dict',
        'dir': 'tt_builtin_dir',
        'divmod': 'tt_builtin_divmod',
        'enumerate': 'tt_builtin_enumerate',
        'eval': 'tt_builtin_eval',
        'exec': 'tt_builtin_exec',
        'filter': 'tt_builtin_filter',
        'float': 'tt_builtin_float',
        'format': 'tt_builtin_format',
        'frozenset': 'tt_builtin_frozenset',
        'getattr': 'tt_builtin_getattr',
        'globals': 'tt_builtin_globals',
        'hasattr': 'tt_builtin_hasattr',
        'hash': 'tt_builtin_hash',
        'help': 'tt_builtin_help',
        'hex': 'tt_builtin_hex',
        'id': 'tt_builtin_id',
        'input': 'tt_builtin_input',
        'int': 'tt_builtin_int',
        'isinstance': 'tt_builtin_isinstance',
        'issubclass': 'tt_builtin_issubclass',
        'iter': 'tt_builtin_iter',
        'len': 'tt_builtin_len',
        'list': 'tt_builtin_list',
        'locals': 'tt_builtin_locals',
        'map': 'tt_builtin_map',
        'max': 'tt_builtin_max',
        'memoryview': 'tt_builtin_memoryview',
        'min': 'tt_builtin_min',
        'next': 'tt_builtin_next',
        'object': 'tt_builtin_object',
        'oct': 'tt_builtin_oct',
        'open': 'tt_builtin_open',
        'ord': 'tt_builtin_ord',
        'pow': 'tt_builtin_pow',
        'print': 'tt_builtin_print',
        'property': 'tt_builtin_property',
        'range': 'tt_builtin_range',
        'repr': 'tt_builtin_repr',
        'reversed': 'tt_builtin_reversed',
        'round': 'tt_builtin_round',
        'set': 'tt_builtin_set',
        'setattr': 'tt_builtin_setattr',
        'slice': 'tt_builtin_slice',
        'sorted': 'tt_builtin_sorted',
        '@staticmethod': 'tt_builtin_@staticmethod',
        'str': 'tt_builtin_str',
        'sum': 'tt_builtin_sum',
        'super': 'tt_builtin_super',
        'tuple': 'tt_builtin_tuple',
        'type': 'tt_builtin_type',
        'vars': 'tt_builtin_vars',
        'zip': 'tt_builtin_zip',
    }
    try:
        if builtin_functions[self] is not None:
            return builtin_functions[self]
    except:
        return 'tt_function_call:' + self


print(token_creator('''def my_func():
    print('yeet') # joe mama
    return None'''))
   # check a tuple: if a var is declared with parenthesis then its a tuple
   # check a set/dict: if a var is declared with curved brackets and it has colon its a dict. else is a set