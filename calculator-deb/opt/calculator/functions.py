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
    """Деление (исключение ловится в интерфейсе)"""
    return a / b

def modul(a, b):
    """Остаток от деления (исключение ловится в интерфейсе)"""
    return a % b

def sin(x):
    """Синус"""
    return math.sin(math.radians(x))

def cos(x):
    """Косинус"""
    return math.cos(math.radians(x))

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

def memory_clear(value):
    """Очистка памяти (MC)"""
    global memory
    memory = 0

def memory_recall(value):
    """Чтение значения из памяти (MR)"""
    global memory
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