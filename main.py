from tkinter.messagebox import showinfo
from tkinter import ttk
import tkinter as tk
import re, os, sys, functions

class Calculator:
    def __init__(self):
        self.first_number = None
        self.cur_oper = None
        self.num2_waiting = False
        self.messsage_errors = ("Невозможно поделить на ноль!", "Невозможно извлечь корень из отрицательного числа!")
        self.application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Главная форма
        self.FormMain = tk.Tk()
        self.FormMain.title("Калькулятор")
        self.FormMain.iconbitmap(default=os.path.join(self.application_path, 'icon.ico'))
        self.FormMain.geometry("{}x{}+{}+{}".format(505, 585, (self.FormMain.winfo_screenwidth() - 505) // 2, (self.FormMain.winfo_screenheight() - 585) // 2))
        self.FormMain.resizable(False, False)

        ttk.Style().configure('TButton', background="white", foreground="black", font=('Arial', 16))

        # Строка вывода
        self.calc = tk.Label(self.FormMain, text='0', anchor='e', font=('Arial', 22))
        self.calc.place(width=505, height=61)

        # Кнопки с числами от 1 до 9
        for i in range(1, 10):
            ttk.Button(
                text = i,
                command = lambda digit=i: self.addDigit(str(digit))
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
            action = (lambda: self.update_display('mr')) if name == 'MR' else (lambda c=cmd: self.create_memory_button(c))

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
                command = lambda x=name: self.update_display(x)
            ).place(
                x = 126 * i,
                y = 136,
                width = 126,
                height = 75
            )

        # Остальные базовые кнопки
        list_func_base = (('±', 'changeSign'), ('0', '0'), (',', 'comma'), ('=', 'calculate'))

        for i, (name, func) in enumerate(list_func_base):
            if func == 'changeSign':
                command = self.changeSign
            elif func == '0':
                command = lambda: self.addDigit('0')
            elif func == 'comma':
                command = self.addComma
            else:  # calculate
                command = self.calculate
                
            ttk.Button(
                text = name,
                command = command
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
                command = lambda x=name: self.addOperation(x)
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
                command = lambda x=name: self.addOperation(x)
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
                command = lambda x=name: self.clear(x)
            ).place(
                x = 252 * i,
                y = 61,
                width = 252,
                height = 75
            )

    def bind_events(self):
        """Привязка событий клавиатуры"""
        self.FormMain.bind('<Key>', self.pressKey)
        self.FormMain.bind('<F1>', self.pressKeyF1)

    def addDigit(self, digit):
        """Добавление цифры"""
        value = self.calc['text']
        if (
                value[0] == '0' and len(value) == 1
                or
                value in self.messsage_errors
                or
                self.num2_waiting
        ):
            value = ""
            self.num2_waiting = False
            
        self.calc['text'] = value + digit

    def addOperation(self, operation):
        """Добавление операции"""
        value = self.calc['text'].replace(',','.')

        if value in self.messsage_errors:
            value = "0"
            
        if value[-1] in "-+*/.":
            value = value[:-1]
        
        if self.first_number and self.cur_oper and not self.num2_waiting:
            self.calculate()
            value = self.calc['text'].replace(',', '.')

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
                self.calc['text'] = str(result).replace('.', ',') if result else self.messsage_errors[1]
            except:
                self.calc['text'] = "Ошибка при вычислении корня!"

            return
        
        self.first_number = float(value) if value else 0
        self.cur_oper = operation
        self.num2_waiting = True

        if operation != 'x^y':
            self.calc['text'] = str(value).replace('.', ',') + operation

    def calculate(self):
        """Вычисление результата"""
        if not self.first_number or not self.cur_oper:
            return

        second_value = self.calc['text'].replace(',','.')

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

        if self.cur_oper in '/%' and second_number == 0:
            self.calc['text'] = self.messsage_errors[0]
        else:
            result = op_funcs[self.cur_oper](self.first_number, second_number) if self.cur_oper in op_funcs else self.first_number
            self.calc['text'] = str(result) if isinstance(result, int) else str(result).replace('.', ',')

        self.reset_calculator()

    def reset_calculator(self):
        """Сброс состояния калькулятора"""
        self.first_number = self.cur_oper = None
        self.num2_waiting = False

    def clear(self, operation):
        """Очистка дисплея"""
        text = self.calc['text']

        if (
                operation == 'C' 
                or 
                len(text) in (1, 2)
                and
                text[0] == '-'
                or 
                text in self.messsage_errors
        ):
            self.calc['text'] = '0'
            self.reset_calculator()
            
        else:
            self.calc['text'] = text = text[:-1]

            if not text or text[-1] not in '+-*/%':
                self.num2_waiting = False

    def changeSign(self):
        """Изменение знака"""
        if self.calc['text'] not in self.messsage_errors:
            self.calc['text'] = self.calc['text'][1:] if self.calc['text'].startswith('-') else '-' + self.calc['text']

    def addComma(self):
        """Добавление запятой"""
        if self.calc['text'] not in self.messsage_errors:
            value = re.split(r'[-+*/]', self.calc['text'])
            if value[-1] and ',' not in value[-1]:
                self.calc['text'] += ','

    def update_display(self, signal):
        """Обновление дисплея для специальных функций"""
        if signal == 'mr':
            result = functions.memory_recall(0)
        else:
            digit = float(self.calc['text'].replace(',', '.'))

            func = {
                'sin': functions.sin,
                'cos': functions.cos,
                'floor': functions.floor,
                'ceil': functions.ceil
            }

            result = func[signal](digit) if signal in func else digit

        self.calc['text'] = str(result).replace('.', ',')

    def create_memory_button(self, command):
        """Создание кнопок памяти"""
        value_text = self.calc['text']

        if value_text in self.messsage_errors:
            value = 0
        else:
            if any(op in value_text for op in ('+', '-', '×', '÷', '%')):
                parts = re.split(r'[+\-×÷%]', value_text)
                value_text = parts[-1] if parts else "0"

            value_text = value_text.replace(',', '.')
            value = float(value_text) if value_text else 0

        command(value)

    def pressKey(self, event):
        """Обработка нажатий клавиш"""
        if event.char.isdigit():
            self.addDigit(event.char)
        elif event.char in '-+*/':
            self.addOperation(event.char)
        elif event.char == ',':
            self.addComma()
        elif event.char == '=' or event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'Escape':
            self.clear('C')
        elif event.keysym == 'BackSpace':
            self.clear('0')

    def pressKeyF1(self, event):
        """Обработка F1 - справка"""
        showinfo(
            title="О программе",
            message="Калькулятор - версия 1.0\n© Калимулин Б.А. и Гнедой М.С., 2025. Все права защищены"
        )

    def run(self):
        """Запуск приложения"""
        self.FormMain.mainloop()


# Запуск калькулятора
if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()