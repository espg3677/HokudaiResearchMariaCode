from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import ast
import inspect
import textwrap

import sys


class MyVisitor():
    def __init__(self, **value_dict):
        self.value_dict = value_dict

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(node)

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            name = arg.arg
            print('Arg: {} = {}'.format(name, self.value_dict[name]))

        for b in node.body:
            self.visit(b)

    def visit_Assign(self, node):
        target = node.targets[0].id
        value = self.visit(node.value)
        self.value_dict[target] = value

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            def op(x, y): return x + y
        elif isinstance(node.op, ast.Sub):
            def op(x, y): return x - y

        left = self.visit(node.left)
        right = self.visit(node.right)
        result = op(left, right)

        return result

    def visit_Name(self, node):
        name = node.id

        if name in self.value_dict:
            value = self.value_dict[name]
        else:
            raise NameError('No such variable: %s' % name)

        return value

    def visit_Return(self, node):
        value = self.visit(node.value)
        print('Return:', value)

    def visit_If(self, node):
        # ----
        left = self.visit(node.test.left)
        for comparator in node.test.comparators:
            self.visit(comparator)

        cond = False
        # ----

        if cond:
            self.visit(node.body)
        else:
            self.visit(node.orelse)

    def visit_Num(self, node):
        return node.n

    def visit_list(self, node):
        for n in node:
            self.visit(n)


# def myfunc():
#    print('Hello, world!')
#
#text = textwrap.dedent(inspect.getsource(myfunc))


def run(**kwargs):
    filename = sys.argv[1]
    text = open(filename).read()
    tree = ast.parse(text).body[0]

    visitor = MyVisitor(**kwargs)
    visitor.visit(tree)


run(a=100, b=200, c=-500)
run(a=10, b=20, c=30)
