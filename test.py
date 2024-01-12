

def bar(bla):
    return bla + 1

def foo(x):
    bla = x
    bar(bla)

def main():
    x = 1
    foo(x)
