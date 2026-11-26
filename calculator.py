# This is addition functionality
def add(a, b):
    return a + b

# This is substraction functionality
def subtract(a, b):
    return a - b

def division(a,b):
    if (b==0):
        raise ZeroDivisionError("Divided my 0")
    return a/b
