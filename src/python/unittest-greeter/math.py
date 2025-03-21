
def add(a, b):
    """adds two numbers, from user input"""
    if type(a) not in [int]:
        raise TypeError

    return a + b
