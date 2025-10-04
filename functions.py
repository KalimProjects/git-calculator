import math

memory = 0

def add(a, b):
    """Сложение"""
    return a + b

def sub(a, b):
    """Вычитание"""
    return a - b

def mult(a, b):
    """Умножение"""
    return a * b

def div(a, b):
    """Деление"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

def modul(a, b):
    """Остаток от деления"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a % b

def sin(x):
    """Синус"""
    return math.sin(x)

def cos(x):
    """Косинус"""
    return math.cos(x)

def power(a, b):
    """Степень"""
    return a ** b

def sqrt(x):
    """Квадратный корень"""
    return math.sqrt(x)

def floor(x):
    """Округение вниз"""
    return math.floor(x)

def ceil(x):
    """Округение вверх"""
    return math.ceil(x)

def memory_clear():
    """Очистка памяти (MC)"""
    global memory
    memory = 0

def memory_recall():
    """Чтение значения из памяти (MR)"""
    return memory

def memory_add(value):
    """Сложение текущего значения с памятью (M+)"""
    global memory
    memory += value

def memory_subtract(value):
    """Вычитание текущего значения из памяти (M-)"""
    global memory
    memory -= value

def memory_store(value):
    """Сохраняение значение в память (MS)"""
    global memory
    memory = value