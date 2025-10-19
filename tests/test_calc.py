import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import main

class Test(unittest.TestCase):
    def setUp(self):
        self.Calculator = main.Calculator()

    def test_calculate(self):
        test_data = [
            (5, '255', '+', '260'),
            (7, '4', '-', '3'),
            (72, '8', '+', '80'),
            (10, '3', '*', '30'),
            (15, '5', '÷', '3')
        ]
        for param1, param2, param3, expected in test_data:
            with self.subTest(param1=param1, param2=param2, param3=param3, expected=expected):            
                self.Calculator.first_number = param1
                self.Calculator.calc['text'] = param2
                self.Calculator.cur_oper = param3
                self.Calculator.calculate()
                self.assertEqual(self.Calculator.calc['text'], expected)

    def test_addDigit(self):
        self.Calculator.calc['text'] = '0'
        for i in range(1, 10):
            self.Calculator.addDigit(str(i))
            self.assertEqual(self.Calculator.calc['text'], str(i))
            self.Calculator.calc['text'] = '0'  # Сбрасываем перед каждым тестом

    def test_addOperation_basic_operations(self):
        test_cases = [
            ('+', '+', '0+'),
            ('-', '-', '0-'),
            ('×', '*', '0*'),
            ('÷', '÷', '0÷'),
            ('%', '%', '0%'),
            ('x^y', '^', '0^'),
        ]
        
        for operation_input, expected_oper, expected_display in test_cases:
            with self.subTest(operation=operation_input):
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
        test_cases = [
            ('4', '2'),
            ('9', '3'),
            ('0', 'Невозможно извлечь корень из отрицательного числа!'),
            ('-4', 'Невозможно извлечь корень из отрицательного числа!'),
        ]
        
        for initial_value, expected_display in test_cases:
            with self.subTest(value=initial_value):
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = initial_value
                
                self.Calculator.addOperation('√x')
                
                self.assertIsNone(self.Calculator.cur_oper)
                self.assertIsNone(self.Calculator.first_number)
                self.assertFalse(self.Calculator.num2_waiting)
                self.assertEqual(self.Calculator.calc['text'], expected_display)
    
    def test_addOperation_with_previous_calculation(self):
        # Симулируем: 10 + 5 = 15, затем новая операция
        self.Calculator.first_number = 10.0
        self.Calculator.cur_oper = '+'
        self.Calculator.num2_waiting = True
        self.Calculator.calc['text'] = '5'
        
        # Вызываем calculate чтобы получить результат 15
        self.Calculator.calculate()
        self.assertEqual(self.Calculator.calc['text'], '15')
        
        # Теперь добавляем новую операцию
        self.Calculator.addOperation('×')
        
        self.assertEqual(self.Calculator.cur_oper, '*')
        self.assertEqual(self.Calculator.first_number, 15.0)
        self.assertTrue(self.Calculator.num2_waiting)
    
    def test_addOperation_trim_trailing_operators(self):
        test_cases = [
            ('5+', '5+'),
            ('10-', '10+'),
            ('3×', '3+'),
            ('7÷', '7+'),
            ('9.', '9+'),
        ]
        
        for initial_display, expected_display in test_cases:
            with self.subTest(initial=initial_display):
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = initial_display
                
                self.Calculator.addOperation('+')
                
                number_str = initial_display[:-1].replace(',', '.')
                expected_number = float(number_str) if number_str else 0.0
                self.assertEqual(self.Calculator.first_number, expected_number)
                self.assertEqual(self.Calculator.calc['text'], expected_display)
    
    def test_addOperation_error_state(self):
        error_messages = self.Calculator.messsage_errors
        
        for error_msg in error_messages:
            with self.subTest(error=error_msg):
                self.Calculator.first_number = None
                self.Calculator.cur_oper = None
                self.Calculator.num2_waiting = False
                self.Calculator.calc['text'] = error_msg
                
                self.Calculator.addOperation('+')
                
                self.assertEqual(self.Calculator.first_number, 0.0)
                self.assertEqual(self.Calculator.cur_oper, '+')
                self.assertEqual(self.Calculator.calc['text'], '0+')
    
    def test_addOperation_empty_value(self):
        self.Calculator.calc['text'] = '0'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('+')
        
        self.assertEqual(self.Calculator.first_number, 0.0)
        self.assertEqual(self.Calculator.cur_oper, '+')
        self.assertEqual(self.Calculator.calc['text'], '0+')
    
    def test_addOperation_power_operation(self):
        self.Calculator.calc['text'] = '2'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('x^y')
        
        self.assertEqual(self.Calculator.cur_oper, '^')
        self.assertEqual(self.Calculator.first_number, 2.0)
        self.assertTrue(self.Calculator.num2_waiting)
        self.assertEqual(self.Calculator.calc['text'], '2^')

    def test_addOperation_complex_scenario(self):
        self.Calculator.calc['text'] = '10'
        self.Calculator.first_number = None
        self.Calculator.cur_oper = None
        self.Calculator.num2_waiting = False
        
        self.Calculator.addOperation('+')
        self.assertEqual(self.Calculator.cur_oper, '+')
        self.assertEqual(self.Calculator.first_number, 10.0)
        self.assertTrue(self.Calculator.num2_waiting)
        self.assertEqual(self.Calculator.calc['text'], '10+')
        
        # Вводим второе число
        self.Calculator.addDigit('5')
        self.assertEqual(self.Calculator.calc['text'], '10+5')
        self.Calculator.num2_waiting = False
        
        # Добавляем новую операцию - должно вызвать calculate()
        self.Calculator.addOperation('×')
        self.assertEqual(self.Calculator.cur_oper, '*')
        self.assertEqual(self.Calculator.first_number, 15.0)
        self.assertTrue(self.Calculator.num2_waiting)
        self.assertEqual(self.Calculator.calc['text'], '15*')

    def test_changeSign(self):
        test_cases = [
            ('5', '-5'),
            ('-5', '5'),
            ('10+5', '10+-5'),
            ('10-5', '10--5'),
        ]
        
        for initial, expected in test_cases:
            with self.subTest(initial=initial, expected=expected):
                self.Calculator.calc['text'] = initial
                self.Calculator.changeSign()
                self.assertEqual(self.Calculator.calc['text'], expected)

    def test_format_number(self):
        test_cases = [
            (5, '5'),
            (5.0, '5'),
            (5.5, '5,5'),
            (-3, '-3'),
            (-3.5, '-3,5'),
            (None, '0')
        ]
        
        for num, expected in test_cases:
            with self.subTest(num=num, expected=expected):
                result = self.Calculator.format_number(num)
                self.assertEqual(result, expected)