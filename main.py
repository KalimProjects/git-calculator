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
                value == '0'
                or
                value in self.messsage_errors
        ):
            value = ""
        
        # Не сбрасываем строку при num2_waiting, а добавляем к существующей
        if self.num2_waiting:
            self.num2_waiting = False
                
        self.calc['text'] = value + digit

    def addOperation(self, operation):
        """Добавление операции"""
        value = self.calc['text'].replace(',','.')

        if value in self.messsage_errors:
            value = "0"
        
        # Если последний символ - оператор, заменяем его
        if value and value[-1] in "-+×÷*/%^":
            value = value[:-1]
        
        if self.first_number and self.cur_oper and not self.num2_waiting:
            self.calculate()
            value = self.calc['text'].replace(',', '.')

        operation_internal = {
            '+': '+',
            '-': '-',
            '×': '*',
            '÷': '÷',
            'x^y': '^',  # Оставляем ^ для отображения
            '√x': 'sqrt',
            '%': '%'
        }[operation]

        if operation_internal == 'sqrt':
            try:
                digit = float(value)
                result = digit ** 0.5 if digit >= 0 else None
                self.calc['text'] = self.format_number(result) if result else self.messsage_errors[1]
            except:
                self.calc['text'] = "Ошибка при вычислении корня!"
            return
        
        self.first_number = float(value) if value else 0
        self.cur_oper = operation_internal
        self.num2_waiting = True

        # Всегда показываем оператор (включая ^ для степени)
        display_value = self.format_number(float(value)) if value else '0'
        self.calc['text'] = display_value + self.cur_oper

    def calculate(self):
        """Вычисление результата"""
        if not self.cur_oper:
            return

        full_expression = self.calc['text'].replace(',', '.')
        
        # Находим позицию оператора
        operator_pos = -1
        for i, char in enumerate(full_expression):
            if char in '+-×÷*/%^':
                # Проверяем, что это не унарный минус
                if char == '-' and (i == 0 or full_expression[i-1] in '+-×÷*/%^'):
                    continue  # Это унарный минус, пропускаем
                operator_pos = i
                break
        
        if operator_pos != -1:
            # Извлекаем второе число (всё что после оператора)
            second_value = full_expression[operator_pos + 1:]
            # Первое число - всё до оператора
            try:
                actual_first_number = float(full_expression[:operator_pos])
            except ValueError:
                actual_first_number = self.first_number
        else:
            # Если оператора нет, используем сохранённое first_number
            second_value = full_expression
            actual_first_number = self.first_number
        
        # Обновляем first_number на актуальное значение из выражения
        self.first_number = actual_first_number
        
        # Обрабатываем второе число
        if not second_value or second_value in '+-×÷*/%^':
            second_number = 0
        else:
            try:
                second_number = float(second_value)
            except ValueError:
                second_number = 0

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
            self.calc['text'] = self.format_number(result)

        self.reset_calculator()

    def format_number(self, num):
        """Форматирование числа: целые числа без запятой, вещественные с запятой"""
        if num is None:
            return "0"
        if isinstance(num, int) or num.is_integer():
            return str(int(num))
        else:
            return str(num).replace('.', ',')

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
                len(text) in (1, 2) and text[0] == '-'
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
        """Изменение знака последнего числа в строке"""
        if self.calc['text'] in self.messsage_errors:
            return
            
        text = self.calc['text']
        
        # Ищем позицию начала последнего числа
        # Игнорируем операторы, но учитываем унарный минус
        operators = '+-×÷*/%^'
        i = len(text) - 1
        while i >= 0:
            if text[i] in operators:
                # Проверяем, это бинарный оператор или унарный минус
                if text[i] == '-' and (i == 0 or text[i-1] in operators):
                    i -= 1  # Это унарный минус, продолжаем поиск
                    continue
                break
            i -= 1
        
        # i теперь указывает на позицию перед последним числом (или -1 если нет операторов)
        start_pos = i + 1
        last_number = text[start_pos:]
        
        if not last_number:
            return
            
        # Переключаем знак
        if last_number.startswith('-'):
            new_last_number = last_number[1:]  # Убираем минус
        else:
            new_last_number = '-' + last_number  # Добавляем минус
        
        # Собираем новую строку
        self.calc['text'] = text[:start_pos] + new_last_number

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

        self.calc['text'] = self.format_number(result)

    def create_memory_button(self, command):
        """Создание кнопок памяти"""
        value_text = self.calc['text']

        if value_text in self.messsage_errors:
            value = 0
        else:
            # Находим последнее число в выражении (учитывая унарный минус)
            full_expression = value_text.replace(',', '.')
            
            # Ищем позицию последнего оператора чтобы извлечь последнее число
            operator_pos = -1
            for i, char in enumerate(full_expression):
                if char in '+-×÷*/%^':
                    # Проверяем, что это не унарный минус
                    if char == '-' and (i == 0 or full_expression[i-1] in '+-×÷*/%^'):
                        continue  # Это унарный минус, пропускаем
                    operator_pos = i
            
            if operator_pos != -1:
                # Берём последнее число (после последнего оператора)
                number_str = full_expression[operator_pos + 1:]
            else:
                # Если операторов нет, берём всю строку
                number_str = full_expression
            
            # Преобразуем в число
            try:
                value = float(number_str) if number_str else 0
            except ValueError:
                value = 0

        command(value)

    def pressKey(self, event):
        """Обработка нажатий клавиш"""

        if not event.char:
            return

        if event.char.isdigit():
            self.addDigit(event.char)
        elif event.char in '-+*/':
            operation = {'*':'×', '/':'÷'}.get(key=event.char, default=event.char)
            self.addOperation(operation)
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
            message="Калькулятор - версия 1.2\n© Калимулин Б.А. и Гнедой М.С., 2025. Все права защищены"
        )

    def run(self):
        """Запуск приложения"""
        self.FormMain.mainloop()


# Запуск калькулятора
if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()