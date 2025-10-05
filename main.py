from tkinter.messagebox import showinfo
from tkinter import ttk
import tkinter as tk
import re, os, sys, functions

def addDigit(digit):
    global num2_waiting, messsage_errors
    
    value = calc['text']
    if (
            value[0] == '0' and len(value) == 1
            or
            value in messsage_errors
            or
            num2_waiting
    ):
        value = ""
        num2_waiting = False
        
    calc['text'] = value + digit


def addOperation(operation):
    global first_number, cur_oper, num2_waiting, messsage_errors

    value = calc['text'].replace(',','.')

    if value in messsage_errors:
        value = "0"
        
    if value[-1] in "-+*/.":
        value = value[:-1]
    
    if first_number and cur_oper and not num2_waiting:
        calculate()
        value = calc['text'].replace(',', '.')

    operation = {
        '+': '+',
        '-': '-',
        '×': '*',
        '÷': '÷',
        'x^y': '^',
        '√x': 'sqrt',
        '%': '%'
    }[operation]

    if operation == 'sqrt':
        try:
            digit = float(value)
            result = digit ** 0.5 if digit >= 0 else None
            calc['text'] = str(result).replace('.', ',') if result else messsage_errors[1]
        except:
            calc['text'] = "Ошибка при вычислении корня!"

        return
    
    first_number = float(value) if value else 0
    cur_oper = operation
    num2_waiting = True

    if operation != 'x^y':
        calc['text'] = str(value).replace('.', ',') + operation


def calculate():
    global first_number, cur_oper, num2_waiting, messsage_errors

    if not first_number or not cur_oper:
        return

    second_value = calc['text'].replace(',','.')

    if any(oper in second_value for oper in '+-*/%'):
        parts = re.split(r'[+\-*/%]?', second_value)
        second_value = parts[1] if len(parts) > 1 else 0
    
    if not second_value or second_value in '+-*/%':
        second_value = "0"

    second_number = float(second_value)

    op_funcs = {
        '+': functions.add,
        '-': functions.sub,
        '*': functions.mult,
        '÷': functions.div,
        '^': functions.power,
        '%': functions.modul
    }

    if cur_oper in '/%' and second_number == 0:
        calc['text'] = messsage_errors[0]
    else:
        result = op_funcs[cur_oper](first_number, second_number) if cur_oper in op_funcs else first_number
        calc['text'] = str(result) if isinstance(result, int) else str(result).replace('.', ',')

    reset_calculator()


def reset_calculator():
    global first_number, cur_oper, num2_waiting
    first_number = cur_oper = None
    num2_waiting = False


def clear(operation):
    global first_number, cur_oper, num2_waiting, messsage_errors

    text = calc['text']

    if (
            operation == 'C' 
            or 
            len(text) in (1, 2)
            and
            text[0] == '-'
            or 
            text in messsage_errors
    ):
        calc['text'] = '0'
        reset_calculator()
        
    else:
        calc['text'] = text = text[:-1]

        if not text or text[-1] not in '+-*/%':
            num2_waiting = False


def changeSign():
    global messsage_errors
    if calc['text'] not in messsage_errors:
        calc['text'] = calc['text'][1:] if calc['text'].startswith('-') else '-' + calc['text']


def addComma():
    global messsage_errors
    if calc['text'] not in messsage_errors:
        value = re.split(r'[-+*/]', calc['text'])
        if value[-1] and ',' not in value[-1]:
            calc['text'] += ','


def update_display(signal):
    if signal == 'mr':
        result = functions.memory_recall(0)
    else:
        digit = float(calc['text'].replace(',', '.'))

        func = {
            'sin': functions.sin,
            'cos': functions.cos,
            'floor': functions.floor,
            'ceil': functions.ceil
        }

        result = func[signal](digit) if signal in func else digit

    calc['text'] = str(result).replace('.', ',')


def create_memory_button(command):
    global messsage_errors

    value_text = calc['text']

    if value_text in messsage_errors:
        value = 0
    else:
        if any(op in value_text for op in ('+', '-', '×', '÷', '%')):
            parts = re.split(r'[+\-×÷%]', value_text)
            value_text = parts[-1] if parts else "0"

        value_text = value_text.replace(',', '.')
        value = float(value_text) if value_text else 0

    command(value)

    # print(f"Кнопка {name}: передаем значение {value}") # отладка
    # print(f"Текущая память: {functions.memory}") # отладка


def pressKey(event):
    if event.char.isdigit():
        addDigit(event.char)
    elif event.char in '-+*/':
        addOperation(event.char)
    elif event.char == ',':
        addComma()
    elif event.char == '=' or event.keysym == 'Return':
        calculate()
    elif event.keysym == 'Escape':
        clear('C')
    elif event.keysym == 'BackSpace':
        clear('0')


def pressKeyF1(event):
    showinfo(
        title="О программе",
        message="Калькулятор - версия 1.0\n© Калимулин Б.А. и Гнедой М.С., 2025. Все права защищены"
    )

# Общие переменные
first_number = cur_oper = None
num2_waiting = False
messsage_errors = ("Невозможно поделить на ноль!", "Невозможно извлечь корень из отрицательного числа!")
application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)


# Главная форма
FormMain = tk.Tk()
FormMain.title("Калькулятор")
FormMain.iconbitmap(default=os.path.join(application_path, 'icon.ico'))
FormMain.geometry("{}x{}+{}+{}".format(505, 585, (FormMain.winfo_screenwidth() - 505) // 2, (FormMain.winfo_screenheight() - 585) // 2))
FormMain.resizable(False, False)

FormMain.bind('<Key>', pressKey)
FormMain.bind('<F1>', pressKeyF1)

ttk.Style().configure('TButton', background="white", foreground="black", font=('Arial', 16))


# Строка вывода
calc = tk.Label(FormMain, text='0', anchor='e', font=('Arial', 22))
calc.place(width=505, height=61)


# Кнопки с числами от 1 до 9
for i in range(1, 10):
    ttk.Button(
        text = i,
        command = lambda digit=i: addDigit(str(digit))
    ).place(
        x = 101 + ((i-1) % 3) * 101,
        y = 436 - ((i-1) // 3) * 75,
        width = 101,
        height = 75
    )


# Кнопки работы с памятью
memlist = (
    ('MS', functions.memory_store),
    ('M+', functions.memory_add),
    ('M-', functions.memory_subtract),
    ('MC', functions.memory_clear),
    ('MR', None)
)

for i, (name, cmd) in enumerate(memlist):
    action = (lambda: update_display('mr')) if name == 'MR' else (lambda c=cmd: create_memory_button(c))

    ttk.Button(
        text = name,
        command = action
    ).place(
        y = 511 - i * 75,
        width = 101,
        height = 75
    )


# Кнопки работы с функциями
list_func_spec = ('sin', 'cos', 'ceil', 'floor')

for i, name in enumerate(list_func_spec):
    ttk.Button(
        text = name,
        command = lambda x=name: update_display(x)
    ).place(
        x = 126 * i,
        y = 136,
        width = 126,
        height = 75
    )


# Остальные базовые кнопки
list_func_base = (('±', 'changeSign()'), ('0', 'addDigit(\'0\')'), (',', 'addComma()'), ('=', 'calculate()'))

for i, (name, func) in enumerate(list_func_base):
    ttk.Button(
        text = name,
        command = lambda x=func: eval(x)
    ).place(
        x = 101 + 101 * i,
        y = 511,
        width = 101,
        height = 75
    )


# Кнопки базовых мат. операций
list_func_1 = ('+', '-', '×', '÷')

for i, name in enumerate(list_func_1):
    ttk.Button(
        text = name,
        command = lambda x=name: addOperation(x)
    ).place(
        x = 404,
        y = 436 - 75 * i,
        width = 101,
        height = 75
    )


# Кнопки особых операций
list_func_2 = ('x^y', '√x', '%')

for i, name in enumerate(list_func_2):
    ttk.Button(
        text = name,
        command = lambda x=name: addOperation(x)
    ).place(
        x = 101 + 101 * i,
        y = 211,
        width = 101,
        height = 75
    )


# Кнопки очистки
list_func_3 = ('C', '←')

for i, name in enumerate(list_func_3):
    ttk.Button(
        text = name,
        command = lambda x=name: clear(x)
    ).place(
        x = 252 * i,
        y = 61,
        width = 252,
        height = 75
    )


FormMain.mainloop()