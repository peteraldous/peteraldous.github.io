#!/usr/bin/python3

import os
import sys
import subprocess

s = sys.argv[1]
last_id = 0

def next_token():
    if s == "":
        return None
    return s[0]

def consume():
    global s
    if s == "":
        raise ValueError("Tried to consume empty string")
    f = s[0]
    s = s[1:]
    return f

def node_str(id):
    return "n{0}".format(id)

def to(frm, to):
    return "  {0} -> {1};\n".format(node_str(frm), node_str(to))

def get_id():
    global last_id
    last_id += 1
    return last_id

class E:
    def parse():
        f = next_token()
        if f.isdigit() or f == '(':
            # TE'
            t = T.parse()
            ep = Ep.parse()
            return E(t, ep)
        raise ValueError("unmatched token: {0}".format(f))
    def __init__(self, t, ep):
        self.t = t
        self.ep = ep
        self.id = get_id()
    def __str__(self):
        return "  {0} [label=\"E\"]\n".format(node_str(self.id)) + \
            to(self.id, self.t.id) + \
            to(self.id, self.ep.id) + \
            str(self.t) + \
            str(self.ep)

class Ep:
    def parse():
        f = next_token()
        if f == '+':
            # +TE'
            consume()
            t = T.parse()
            ep = Ep.parse()
            return Ep(t, ep)
        if f == ')' or f is None:
            # eps
            return None
        raise ValueError("unmatched token: {0}".format(f))
    def __init__(self, t, ep):
        self.t = t
        self.ep = ep
        self.id = get_id()
    def __str__(self):
        pid = get_id()
        if self.ep is None:
            ep_str = ""
        else:
            ep_str = to(self.id, self.ep.id) + str(self.ep)
        return "  {0} [label=\"E'\"]\n".format(node_str(self.id)) + \
            "  {0} [label=\"+\"]\n".format(node_str(pid)) + \
            to(self.id, pid) + \
            to(self.id, self.t.id) + \
            str(self.t) + \
            ep_str

class T:
    def parse():
        f = next_token()
        if f.isdigit():
            # int T'
            consume()
            tp = Tp.parse()
            return T(True, f, tp)
        if f == '(':
            # ( E ) T'
            consume()
            e = E.parse()
            close = consume()
            if close != ')':
                raise ValueError("unmatched parenthesis; got {0}".format(close))
            tp = Tp.parse()
            return T(False, e, tp)
        raise ValueError("unmatched token: {0}".format(f))
    def __init__(self, is_int, l, r):
        self.is_int = is_int
        self.l = l
        self.r = r
        self.id = get_id()
    def __str__(self):
        if self.r is None:
            r_str = ""
        else:
            r_str = to(self.id, self.r.id) + \
            str(self.r)
        if self.is_int:
            iid = get_id()
            return "  {0} [label=\"T\"]\n".format(node_str(self.id)) + \
                "  {0} [label=\"{1}\"]\n".format(node_str(iid), self.l) + \
                to(self.id, iid) + \
                r_str
        else:
            open_id = get_id()
            close_id = get_id()
            return "  {0} [label=\"T\"]\n".format(node_str(self.id)) + \
                "  {0} [label=\"(\"]\n".format(node_str(open_id)) + \
                str(self.l) + \
                "  {0} [label=\")\"]\n".format(node_str(close_id)) + \
                to(self.id, open_id) + \
                to(self.id, self.l.id) + \
                to(self.id, close_id) + \
                r_str

class Tp:
    def parse():
        f = next_token()
        if f == '*':
            # * int T'
            consume()
            f = consume()
            if not f.isdigit():
                raise ValueError("expected digit; got {0}".format(f))
            tp = Tp.parse()
            return Tp(f, tp)
        if f == ')' or f == '+' or f is None:
            return None
        raise ValueError("unmatched token: {0}".format(f))
    def __init__(self, i, tp):
        self.i = i
        self.tp = tp
        self.id = get_id()
    def __str__(self):
        mid = get_id()
        iid = get_id()
        if self.tp is None:
            tp_str = ""
        else:
            tp_str = to(self.id, self.tp.id) + str(self.tp)
        return "  {0} [label=\"T'\"]\n".format(node_str(self.id)) + \
            "  {0} [label=\"*\"]\n".format(node_str(mid)) + \
            "  {0} [label=\"{1}\"]\n".format(node_str(iid), self.i) + \
            to(self.id, mid) + \
            to(self.id, iid) + \
            tp_str

# print(E.parse())
graph = "digraph parse_tree {\n  ordering=\"out\"\n" + \
    str(E.parse()) + \
    "}"

filename="parse-la.png"
subprocess.run(["dot", "-Tpng", "-o", filename], input=str.encode(graph))
if sys.platform.startswith("darwin"):
    subprocess.call(['open', filename])
elif os.name == 'nt':
    os.startfile(filename)
elif os.name == 'posix':
    # This unnecessarily complex thing allows me to use the alias I defined for
    # xdg-open in bash in WSL
    subprocess.run(["bash", "-i", "-c", "xdg-open {0}".format(filename)])
