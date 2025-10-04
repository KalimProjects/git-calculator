import tkinter as tk
import re
from tkinter.messagebox import showinfo, INFO
from tkinter import ttk
from os import getcwd

def addDigit(digit):
    value = str(calc['text'])
    if (value[0] == '0' and len(value) == 1) or (value == "На ноль делить нельзя!") or (value == "Нельзя брать корень от отрицательного числа!"):
        value = ""
    value = value + str(digit)
    calc['text'] = value
def addOperation(operation):
    operation = {'+': '+', '-': '-', '×': '*', '÷': '/', 'x^y': 'pow', '√x': 'sqrt', '%': '1/x'}[operation]
    value = str(calc['text']).replace(',','.')
    if value == "На ноль делить нельзя!" or value == "Нельзя брать корень от отрицательного числа!": value = "0"
    if (value[-1]) in "-+*/.": value = value[:-1]
    elif '+' in value or '-' in value or '*' in value or '/' in value:
        calculate()
        value = calc['text']
    if operation == 'sqrt':
        calc['text'] = str(eval(str(value) + '** 0.5')).replace('.', ',') if eval(str(value)) >= 0 else "Нельзя брать корень от отрицательного числа!"
        return
    elif operation == 'sqr':
        calc['text'] = str(eval(str(value) + '** 2')).replace('.', ',')
        return
    elif operation == '1/x':
        calc['text'] = '1/' + value
        calculate()
        return
    calc['text'] = str(value) + operation
def calculate():
    value = str(calc['text']).replace(',','.')
    if value[-1] == '.': value = value[:-1]
    if value[-1] in "-+*/":
        value = value + value[:-1]
    try:
        value = eval(value)
        calc['text'] = str(value).replace('.',',')
    except ZeroDivisionError:
        calc['text'] = "На ноль делить нельзя!"
def clear(operation):
    calc['text'] = '0' if operation == 'C' or len(calc['text']) == 1 or len(calc['text']) == 2 and str(calc['text'])[0] == '-' or calc['text'] == "На ноль делить нельзя!" or calc['text'] == "Нельзя брать корень от отрицательного числа!" else calc['text'][:-1]
def changeSign():
    if calc['text'] != 'На ноль делить нельзя!' or calc['text'] != "Нельзя брать корень от отрицательного числа!":
        calc['text'] = str(calc['text'])[1:] if str(calc['text'])[0] == '-' else '-' + str(calc['text'])
def addComma():
    if calc['text'] != 'На ноль делить нельзя!' or calc['text'] != "Нельзя брать корень от отрицательного числа!":
        value = re.split(r'[-+*/]', str(calc['text']))
        calc['text'] = str(calc['text']) + ',' if ',' not in value[-1] and value[-1] != "" else calc['text']
def pressKey(event):
    print(event)
    if event.char.isdigit(): addDigit(event.char)
    elif event.char in '-+*/': addOperation(event.char)
    elif event.char == '=' or event.keysym == 'Return': calculate()
    elif event.keysym == 'Escape': clear('C')
    elif event.keysym == 'BackSpace': clear('0')
    elif event.char == ',': addComma()
def pressKeyF1(event):
    showinfo(title="О программе", message="Калькулятор - версия 1.0.\n(©)Калимулин Б. А. Все права защищены\n\nОтдельная благодарность:\n- Маме - Красноярцеве Оксане Сергеевне и Папе - Калимулину Александру Викторовичу за их воспитание и веру в автора")

mainForm = tk.Tk()
mainForm.title("Калькулятор")
mainForm.iconbitmap(f"{getcwd()}\calculator.ico")
mainForm.geometry("519x507")
mainForm['bg'] = 'black'
mainForm.bind('<Key>', pressKey)
mainForm.bind('<F1>', pressKeyF1)
mainForm.resizable(0, 0)
ttk.Style().configure('TButton', background="white", foreground="black", font=('Arial', 16))
calc = tk.Label(mainForm, text='0', anchor='e', font=('Arial', 14))
calc.place(width=509, height=40, x=5)
[ttk.Button(text=str(i), command=lambda i=i: addDigit(str(i))).place(x=107+((i-1)%3)*102, y=350-((i-1)//3)*77, width=101, height=75) for i in range(1, 10)]
dict1, list2, list3, list4 = {'±': 'changeSign()', '0': 'addDigit(\'0\')', ',': 'addComma()', '=': 'calculate()'}, ['+', '-', '×', '÷'], ['x^y', '√x', '%'], ['C', '←']
memlist = ['MS', 'M+', 'M-', 'MR', 'MC']
[ttk.Button(text=name).place(x=5, y=427 - memlist.index(name)*77, width=101, height=75) for name in memlist]
[ttk.Button(text=i, command=lambda i=i: eval(dict1[i])).place(x=107+102*list(dict1).index(i), y=427, width=101, height=75) for i in dict1]
[ttk.Button(text=i, command=lambda i=i: addOperation(i)).place(x=413, y=350-77*list2.index(i), width=101, height=75) for i in list2]
[ttk.Button(text=i, command=lambda i=i: addOperation(i)).place(x=107+102*list3.index(i), y=119, width=101, height=75) for i in list3]
[ttk.Button(text=i, command=lambda i=i: clear(i)).place(x=107+205*list4.index(i), y=42, width=202, height=75) for i in list4]
mainForm.mainloop()
