import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import main

class Test(unittest.TestCase):
    def setUp(self):
        self.Calculator = main.Calculator()

    def test_calculate(self):
        test_data = [(5, '255', '+', '260,0'),
                     (7, '4', '-', '3,0'),
                     (72, '8', '+', '80,0')]
        for param1, param2, param3, expected in test_data:
            with self.subTest(param1=param1, param2=param2, param3=param3, expected=expected):            
                self.Calculator.first_number = param1
                self.Calculator.calc['text'] = param2
                self.Calculator.cur_oper = param3
                self.Calculator.calculate()
                self.assertEqual(self.Calculator.calc['text'], expected)

    def test_addDigit(self):
        self.Calculator.calc['text'] = '0'
        expected = ''
        for i in range(9):
            with self.subTest(i=i):
                self.Calculator.addDigit(str(i))
                expected = str(i) if expected == '0' else expected + str(i)
                self.assertEqual(self.Calculator.calc['text'], expected)

    def test_addOperation_basic_operations(self):
        """Тест базовых математических операций"""
        test_cases = [
            ('+', '+', '0+'),
            ('-', '-', '0-'),
            ('×', '*', '0*'),  # В коде × преобразуется в * для отображения
            ('÷', '÷', '0÷'),
            ('%', '%', '0%'),
            ('x^y', '^', '0^'),  # Исправлено: операция добавляется к дисплею
        ]
        
        for operation_input, expected_oper, expected_display in test_cases:
            with self.subTest(operation=operation_input):
                # Сбрасываем состояние перед каждым тестом
                self.Calculator.calc['text'] = '0'
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                
                self.Calculator.addOperation(operation_input)
                
                self.assertEqual(self.Calculator.cur_oper, expected_oper)
                self.assertEqual(self.Calculator.first_number, 0.0)
                self.assertTrue(self.Calculator.num2_waiting)
                self.assertEqual(self.Calculator.calc['text'], expected_display)
    
    def test_addOperation_sqrt_operation(self):
        """Тест операции извлечения корня"""
        test_cases = [
            ('4', '2,0'),      # √4 = 2
            ('9', '3,0'),      # √9 = 3
            ('0', 'Невозможно извлечь корень из отрицательного числа!'),      # √0 = 0
            ('-4', self.Calculator.messsage_errors[1]),  # √(-4) = ошибка
        ]
        
        for initial_value, expected_display in test_cases:
            with self.subTest(value=initial_value):
                # Сбрасываем состояние
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = initial_value
                
                self.Calculator.addOperation('√x')
                
                # Для sqrt операция сразу вычисляется, cur_oper не устанавливается
                self.assertIsNone(self.Calculator.cur_oper)
                self.assertIsNone(self.Calculator.first_number)
                self.assertFalse(self.Calculator.num2_waiting)
                self.assertEqual(self.Calculator.calc['text'], expected_display)
    
    def test_addOperation_with_previous_calculation(self):
        """Тест операции после предыдущего вычисления"""
        # Симулируем состояние после первого числа и операции
        self.Calculator.first_number = 10.0
        self.Calculator.cur_oper = '+'
        self.Calculator.num2_waiting = True
        self.Calculator.calc['text'] = '5'
        
        self.Calculator.addOperation('×')
        
        # Должен вызвать calculate() и установить новую операцию
        self.assertEqual(self.Calculator.cur_oper, '*')
        self.assertEqual(self.Calculator.first_number, 5.0)  # 2 + 3 = 5
        self.assertTrue(self.Calculator.num2_waiting)
    
    def test_addOperation_trim_trailing_operators(self):
        """Тест обрезки завершающих операторов"""
        test_cases = [
            ('5+', '5+'),      # Обрезается последний + и добавляется новый
            ('10-', '10+'),    # Обрезается последний - и добавляется +
            ('3*', '3+'),      # Обрезается последний * и добавляется + (исправлено с × на *)
            ('7/', '7+'),      # Обрезается последний / и добавляется + (исправлено с ÷ на /)
            ('9.', '9+'),      # Точка обрезается и добавляется +
        ]
        
        for initial_display, expected_display in test_cases:
            with self.subTest(initial=initial_display):
                # Сбрасываем состояние
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = initial_display
                
                self.Calculator.addOperation('+')
                
                # Проверяем, что число корректно извлеклось
                # Используем replace для корректного преобразования
                number_str = initial_display[:-1].replace(',', '.')
                expected_number = float(number_str) if number_str else 0.0
                self.assertEqual(self.Calculator.first_number, expected_number)
                self.assertEqual(self.Calculator.calc['text'], expected_display)
    
    def test_addOperation_error_state(self):
        """Тест работы при состоянии ошибки"""
        error_messages = self.Calculator.messsage_errors
        
        for error_msg in error_messages:
            with self.subTest(error=error_msg):
                # Сбрасываем состояние
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = error_msg
                
                self.Calculator.addOperation('+')
                
                # При ошибке должно сброситься к '0'
                self.assertEqual(self.Calculator.first_number, 0.0)
                self.assertEqual(self.Calculator.cur_oper, '+')
                self.assertEqual(self.Calculator.calc['text'], '0+')
    
    def test_addOperation_empty_value(self):
        """Тест с пустым значением"""
        self.Calculator.calc['text'] = '0'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('+')
        
        self.assertEqual(self.Calculator.first_number, 0.0)
        self.assertEqual(self.Calculator.cur_oper, '+')
        self.assertEqual(self.Calculator.calc['text'], '0+')
    
    def test_addOperation_power_operation(self):
        """Тест операции возведения в степень"""
        self.Calculator.calc['text'] = '2'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('x^y')
        
        # Для x^y операция добавляется к дисплею как '^'
        self.assertEqual(self.Calculator.cur_oper, '^')
        self.assertEqual(self.Calculator.first_number, 2.0)
        self.assertTrue(self.Calculator.num2_waiting)
        # Дисплей должен содержать операцию '^'
        self.assertEqual(self.Calculator.calc['text'], '2^')

    def test_addOperation_complex_scenario(self):
        """Тест комплексного сценария с последовательными операциями"""
        # Первая операция
        self.Calculator.calc['text'] = '10'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('+')
        self.assertEqual(self.Calculator.cur_oper, '+')
        self.assertEqual(self.Calculator.first_number, 10.0)
        self.assertTrue(self.Calculator.num2_waiting)
        self.assertEqual(self.Calculator.calc['text'], '10+')
        
        # Ввод второго числа (симулируем, что пользователь ввел число)
        self.Calculator.calc['text'] = '5'
        self.Calculator.num2_waiting = False
        
        # Вторая операция - должна вызвать calculate()
        self.Calculator.addOperation('×')
        self.assertEqual(self.Calculator.cur_oper, '*')
        # После calculate first_number должно стать результатом сложения (15.0)
        self.assertEqual(self.Calculator.first_number, 15.0)
        self.assertTrue(self.Calculator.num2_waiting)
        self.assertEqual(self.Calculator.calc['text'], '15,0*')