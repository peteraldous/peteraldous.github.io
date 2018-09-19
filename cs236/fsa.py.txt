#!/usr/bin/python3

import sys

input_string = sys.argv[1]

def room_for(index, size):
    return index+size <= len(input_string)

class Token:
    def __init__(self, token_type, value, length):
        self.token_type = token_type
        self.value = value
        self.length = length

    def __str__(self):
        return "(" + self.token_type + ',"' + self.value + '")'

def check_Equal(s, index):
    if room_for(index, 1) and s[index] == "=":
        return Token("EQUAL", "=", 1)
    return None

def check_EqualEqual(s, index):
    if not room_for(index, 2):
        return None
    if s[index] == "=":
        if s[index+1] == "=":
            return Token("EQUALEQUAL", "==", 2)
    return None

def check_Undefined(s, index):
    if room_for(index, 1):
        return Token("UNDEFINED", s[index], 1)
    return None

def check_Schemes(s, index):
    if not room_for(index, 7):
        return None
    # s0
    if s[index] != "S":
        return None
    # s1
    if s[index+1] != "c":
        return None
    # s2
    if s[index+2] != "h":
        return None
    # s3
    if s[index+3] != "e":
        return None
    # s4
    if s[index+4] != "m":
        return None
    # s5
    if s[index+5] != "e":
        return None
    # s6
    if s[index+6] != "s":
        return None
    # s7 - accept state (can't transition from 7; just accept)
    return Token("SCHEMES", s[index:index+7], 7)

def check_ID(s, index):
    if not room_for(index, 1):
        return None
    i = index
    # s0
    if s[i].isalpha():
        i += 1
        # s1
        while i < len(s) and (s[i].isalpha() or s[i].isdigit()):
            i += 1
    else:
        # r
        return None
    return Token("ID", s[index:i], i - index)

def check_Whitespace(s, index):
    if not room_for(index, 1):
        return None
    i = index
    if s[i].isspace():
        i += 1
        while i < len(s) and (s[i].isspace()):
            i += 1
    else:
        return None
    return Token("WHITESPACE", s[index:i], i - index)

def check_Bang(s, index):
    if not room_for(index, 1):
        return None
    if s[index] == '!':
        return Token("BANG", "!", 1)
    return None

def main():
    index = 0
    automata = [check_Schemes, check_ID, check_Equal, check_EqualEqual, check_Whitespace, check_Bang, check_Undefined]
    while index < len(input_string):
        token = None
        max_length = 0
        for automaton in automata:
            t = automaton(input_string, index)
            if t is not None and t.length > max_length:
                token = t
                max_length = t.length
        if token is None:
            break
        if token.token_type != "WHITESPACE":
            print(token)
        index += token.length

if __name__ == "__main__":
    main()
