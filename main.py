import tkinter as tk
import re
from tkinter.messagebox import showinfo, INFO
from tkinter import ttk
from os import getcwd
import functions

first_number = None
cur_oper = None
num2_waiting = False

def addDigit(digit):
    global num2_waiting
    value = str(calc['text'])
    if (value[0] == '0' and len(value) == 1) or (value == "На ноль делить нельзя!") or (value == "Нельзя брать корень от отрицательного числа!") or (num2_waiting):
        value = ""
        num2_waiting = False
    value = value + str(digit)
    calc['text'] = value

def addOperation(operation):
    global first_number, cur_oper, num2_waiting

    value = str(calc['text']).replace(',','.')
    if value == "На ноль делить нельзя!" or value == "Нельзя брать корень от отрицательного числа!": value = "0"
    if (value[-1]) in "-+*/.": value = value[:-1]
    
    if first_number is not None and cur_oper and not num2_waiting:
        calculate()
        value = calc['text'].replace(',', '.')
    oper_char = operation
    operation = {'+': '+', '-': '-', '×': '*', '÷': '/', 'x^y': 'pow', '√x': 'sqrt', '%': '%'}[operation]
    if operation == 'sqrt':
        try:
            result = float(value) ** 0.5 if float(value) >= 0 else None
            if result is None:
                calc['text'] = "Нельзя брать корень от отрицательного числа!"
            else:
                calc['text'] = str(result).replace('.', ',')
        except:
            calc['text'] = "Ошибка"
        return
    elif operation == 'sqr':
        try:
            result = float(value) ** 2
            calc['text'] = str(result).replace('.', ',')
        except:
            calc['text'] = "Ошибка"
        return
    
    first_number = float(value) if value else 0
    cur_oper = operation
    num2_waiting = True
    if oper_char != 'x^y':
        calc['text'] = str(value) + oper_char

def calculate():
    global first_number, cur_oper, num2_waiting
    if first_number is None or cur_oper is None: return

    second_value = str(calc['text']).replace(',','.')

    if any(oper in second_value for oper in ['+', '-', '*', '/', '%']):
        parts = re.split(r'[+\-*/%]', second_value)
        second_value = parts[1] if len(parts) > 1 else 0
    
    if not second_value or second_value in ['+', '-', '*', '/', '%']:
        second_value = "0"

    second_number = float(second_value)

    if cur_oper == '+':
        result = functions.add(first_number, second_number)
    elif cur_oper == '-':
        result = functions.sub(first_number, second_number)
    elif cur_oper == '*':
        result = functions.mult(first_number, second_number)
    elif cur_oper == '/':
        if second_number == 0:
            calc['text'] = "На ноль делить нельзя!"
            reset_calculator()
            return
        result = functions.div(first_number, second_number)
    elif cur_oper == 'pow':
        result = functions.power(first_number, second_number)
    elif cur_oper == '%':
        if second_number == 0:
            calc['text'] = "На ноль делить нельзя!"
            reset_calculator()
            return
        result = functions.modul(first_number, second_number)
    else:
        result = first_number

    if result == int(result):
        calc['text'] = str(int(result))
    else:
        calc['text'] = str(result).replace('.',',')
    reset_calculator()

def reset_calculator():
    global first_number, cur_oper, num2_waiting
    first_number = None
    cur_oper = None
    num2_waiting = False

def clear(operation):
    global first_number, cur_oper, num2_waiting

    if operation == 'C' or len(calc['text']) == 1 or len(calc['text']) == 2 and str(calc['text'])[0] == '-' or calc['text'] == "На ноль делить нельзя!" or calc['text'] == "Нельзя брать корень от отрицательного числа!":
        calc['text'] = '0'
        reset_calculator()
    else:
        calc['text'] = calc['text'][:-1]
        if not calc['text'] or calc['text'][-1] not in ['+', '-', '*', '/', '%']:
            num2_waiting = False
def changeSign():
    if calc['text'] != 'На ноль делить нельзя!' or calc['text'] != "Нельзя брать корень от отрицательного числа!":
        calc['text'] = str(calc['text'])[1:] if str(calc['text'])[0] == '-' else '-' + str(calc['text'])
def addComma():
    if calc['text'] != 'На ноль делить нельзя!' or calc['text'] != "Нельзя брать корень от отрицательного числа!":
        value = re.split(r'[-+*/]', str(calc['text']))
        calc['text'] = str(calc['text']) + ',' if ',' not in value[-1] and value[-1] != "" else calc['text']

def update_display(signal):
    result = None
    if signal == 'mr': 
        result = functions.memory_recall(0)
    elif signal == 'sin':
        calc['text'] = calc['text'].replace(',', '.')
        result = functions.sin(float(calc['text']))
    elif signal == 'cos':
        calc['text'] = calc['text'].replace(',', '.')
        result = functions.cos(float(calc['text']))
    elif signal == 'floor':
        calc['text'] = calc['text'].replace(',', '.')
        result = functions.floor(float(calc['text']))
    elif signal == 'ceil':
        calc['text'] = calc['text'].replace(',', '.')
        result = functions.ceil(float(calc['text']))
    calc['text'] = str(result).replace('.', ',')

def create_memory_button(command, name, index):
    def action():
        value_text = calc['text']
        
        # Обработка специальных сообщений
        if value_text in ["На ноль делить нельзя!", "Нельзя брать корень от отрицательного числа!"]:
            value = 0
        else:
            # Удаляем операторы если они есть
            if any(op in value_text for op in ['+', '-', '×', '÷', '%']):
                parts = re.split(r'[+\-×÷%]', value_text)
                value_text = parts[-1] if parts else "0"
            
            value_text = value_text.replace(',', '.')
            value = float(value_text) if value_text else 0
        
        print(f"Кнопка {name}: передаем значение {value}")
        command(value)
        print(f"Текущая память: {functions.memory}")
    return action

def pressKey(event):
    print(event)
    if event.char.isdigit(): addDigit(event.char)
    elif event.char in '-+*/': addOperation(event.char)
    elif event.char == '=' or event.keysym == 'Return': calculate()
    elif event.keysym == 'Escape': clear('C')
    elif event.keysym == 'BackSpace': clear('0')
    elif event.char == ',': addComma()
def pressKeyF1(event):
    showinfo(title="О программе", message="Калькулятор - версия 2.0.\n(©)Калимулин Б. А. и Гнедой М. С. Все права защищены")

mainForm = tk.Tk()
mainForm.title("Калькулятор")
mainForm.iconbitmap(fr"{getcwd()}\calculator.ico")
mainForm.geometry("519x583")
mainForm['bg'] = 'black'
mainForm.bind('<Key>', pressKey)
mainForm.bind('<F1>', pressKeyF1)
mainForm.resizable(0, 0)
ttk.Style().configure('TButton', background="white", foreground="black", font=('Arial', 16))
calc = tk.Label(mainForm, text='0', anchor='e', font=('Arial', 14))
calc.place(width=509, height=40, x=5)
[ttk.Button(text=str(i), command=lambda i=i: addDigit(str(i))).place(x=107+((i-1)%3)*102, y=426-((i-1)//3)*77, width=101, height=75) for i in range(1, 10)]
dict1, list2, list3, list4 = {'±': 'changeSign()', '0': 'addDigit(\'0\')', ',': 'addComma()', '=': 'calculate()'}, ['+', '-', '×', '÷'], ['x^y', '√x', '%'], ['C', '←']
memlist, funclist = [('MS', functions.memory_store), ('M+', functions.memory_add), ('M-', functions.memory_subtract), ('MC', functions.memory_clear)], ['sin', 'cos', 'ceil', 'floor']
for i, (name, command) in enumerate(memlist):
    btn_action = create_memory_button(command, name, i)
    ttk.Button(text=name,command= btn_action).place(x=5, y=503 - i*77, width=101, height=75)
        
#ttk.Button(text='MS', command=lambda val=float(calc.cget('text')): functions.memory_store(val)).place(x=5, y=503, width=101, height=75)
ttk.Button(text='MR',command= lambda x=0: update_display('mr')).place(x=5, y=195, width=101, height=75)
('MR', "update_display(\'mr\')")
[ttk.Button(text=name, command=lambda x=name: update_display(x)).place(x=5 + 127.25*funclist.index(name), y=118, width=126.25, height=75) for name in funclist]
[ttk.Button(text=i, command=lambda i=i: eval(dict1[i])).place(x=107+102*list(dict1).index(i), y=503, width=101, height=75) for i in dict1]
[ttk.Button(text=i, command=lambda i=i: addOperation(i)).place(x=413, y=426-77*list2.index(i), width=101, height=75) for i in list2]
[ttk.Button(text=i, command=lambda i=i: addOperation(i)).place(x=107+102*list3.index(i), y=195, width=101, height=75) for i in list3]
[ttk.Button(text=i, command=lambda i=i: clear(i)).place(x=5+255*list4.index(i), y=41, width=254, height=75) for i in list4]
mainForm.mainloop()
