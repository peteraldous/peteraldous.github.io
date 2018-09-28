#!/usr/bin/python3

import os
import subprocess
import sys

s = sys.argv[1]
last_id = 0

def next_token():
    if s == "":
        return None
    return s[0]

def consume():
    global s
    if s == "":
        raise "Tried to consume empty string"
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
            # TX
            t = T.parse()
            x = X.parse()
            return E(t, x)
        raise ValueError("unexpected token: {0}".format(f))
    def __init__(self, t, x):
        self.t = t
        self.x = x
        self.id = get_id()
    def __str__(self):
        id=self.id
        if self.x is None:
            return "  {id} [label=\"E\"];\n".format(id=node_str(id)) + \
                to(id, self.t.id) + \
                str(self.t)
        else:
            return "  {id} [label=\"E\"];\n".format(id=node_str(id)) + \
                to(id, self.t.id) + \
                to(id, self.x.id) + \
                str(self.t) + \
                str(self.x)

class T:
    def parse():
        f = next_token()
        if f.isdigit():
            # int Y
            consume()
            y = Y.parse()
            return T(f, y)
        if f == '(':
            # ( E )
            consume()
            e = E.parse()
            close = consume()
            if (close != ')'):
                raise "Unmatched parenthesis"
            return T(None, e)
    def __init__(self, i, child):
        self.i = i
        self.child = child
        self.id = get_id()
    def __str__(self):
        id=self.id
        if self.i is None:
            # ( E )
            open_id = get_id()
            close_id = get_id()
            return "  {0} [label=\"(\"];\n".format(node_str(open_id)) + \
                "  {id} [label=\"T\"];\n".format(id=node_str(id)) + \
                "  {0} [label=\")\"];\n".format(node_str(close_id)) + \
                to(id, open_id) + \
                to(id, self.child.id) + \
                to(id, close_id) + \
                str(self.child)
        else:
            # int Y
            iid = get_id()
            if self.child is None:
                y_str = ""
            else:
                y_str = to(id, self.child.id) + str(self.child)
            return "  {id} [label=\"T\"];\n".format(id=node_str(id)) + \
                "  {iid} [label=\"{v}\"];\n".format(iid=node_str(iid),
                    v=self.i) + \
                to(id, iid) + y_str

class X:
    def parse():
        f = next_token()
        if f == '+':
            consume()
            e = E.parse()
            return X(e)
        if f == ')':
            return None
        if f is None:
            return None
    def __init__(self, e):
        self.e = e
        self.id = get_id()
    def __str__(self):
        id=self.id
        pid = get_id()
        return "  {id} [label=\"X\"];\n".format(id=node_str(id)) + \
            "  {pid} [label=\"+\"];\n".format(pid=node_str(pid)) + \
            to(id, pid) + \
            to(id, self.e.id) + \
            str(self.e)

class Y:
    def parse():
        f = next_token()
        if f == '*':
            consume()
            t = T.parse()
            return Y(t)
        if f == '+':
            return None
        if f == ')':
            return None
        if f is None:
            return None
    def __init__(self, t):
        self.t = t
        self.id = get_id()
    def __str__(self):
        id=self.id
        mid = get_id()
        return "  {id} [label=\"X\"];\n".format(id=node_str(id)) + \
            "  {mid} [label=\"*\"];\n".format(mid=node_str(mid)) + \
            to(id, mid) + \
            to(id, self.t.id) + \
            str(self.t)

graph = "digraph parse_tree {\n  ordering=\"out\"\n" + \
    str(E.parse()) + \
    "}"

filename="parse-ra.png"
subprocess.run(["dot", "-Tpng", "-o", filename], input=str.encode(graph))
if sys.platform.startswith("darwin"):
    subprocess.call(['open', filename])
elif os.name == 'nt':
    os.startfile(filename)
elif os.name == 'posix':
    # This unnecessarily complex thing allows me to use the alias I defined for
    # xdg-open in bash in WSL
    subprocess.run(["bash", "-i", "-c", "xdg-open {0}".format(filename)])
