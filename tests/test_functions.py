import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import functions


class TestCalculatorFunctions(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(functions.add(2, 3), 5)
        self.assertEqual(functions.add(-1, 1), 0)
        self.assertEqual(functions.add(0, 0), 0)
        self.assertEqual(functions.add(-5, -3), -8)
        self.assertEqual(functions.add(1e10, 1e10), 2e10)
    
    def test_sub(self):
        self.assertEqual(functions.sub(5, 3), 2)
        self.assertEqual(functions.sub(1, 1), 0)
        self.assertEqual(functions.sub(0, 5), -5)
    
    def test_mult(self):
        self.assertEqual(functions.mult(2, 3), 6)
        self.assertEqual(functions.mult(-2, 3), -6)
        self.assertEqual(functions.mult(0, 5), 0)
        self.assertEqual(functions.mult(1e6, 1e6), 1e12)
    
    def test_div(self):
        self.assertEqual(functions.div(6, 3), 2)
        self.assertEqual(functions.div(5, 2), 2.5)
        self.assertEqual(functions.div(-10, 2), -5)
        with self.assertRaises(ZeroDivisionError):
            functions.div(5, 0)
    
    def test_power(self):
        self.assertEqual(functions.power(2, 3), 8)
        self.assertEqual(functions.power(5, 0), 1)
        self.assertEqual(functions.power(4, 0.5), 2)
    
    def test_modul(self):
        self.assertEqual(functions.modul(10, 3), 1)
        self.assertEqual(functions.modul(5, 5), 0)
        with self.assertRaises(ZeroDivisionError):
            functions.div(5, 0)
    
    def test_sin(self):
        self.assertAlmostEqual(functions.sin(90), 1.0, places=2)
        self.assertAlmostEqual(functions.sin(0), 0.0, places=2)
    
    def test_cos(self):
        self.assertAlmostEqual(functions.cos(0), 1.0, places=2)  
        self.assertAlmostEqual(functions.cos(90), 0.0, places=2)
    
    def test_floor(self):
        self.assertEqual(functions.floor(2.7), 2)
        self.assertEqual(functions.floor(-2.3), -3)
    
    def test_ceil(self):
        self.assertEqual(functions.ceil(2.3), 3)
        self.assertEqual(functions.ceil(-2.7), -2)
    
    def test_memory_operations(self):
        functions.memory_clear(0)
        self.assertEqual(functions.memory_recall(0), 0)
        
        functions.memory_store(5)
        self.assertEqual(functions.memory_recall(0), 5)
        
        functions.memory_add(3)
        self.assertEqual(functions.memory_recall(0), 8)
        
        functions.memory_subtract(2)
        self.assertEqual(functions.memory_recall(0), 6)
        
        functions.memory_clear(0)
        self.assertEqual(functions.memory_recall(0), 0)


class TestCalculatorLogic(unittest.TestCase):
    
    def test_complex_operations(self):
        self.assertEqual(
            functions.add(functions.mult(2, 3), functions.div(10, 2)),
            11
        )

        self.assertEqual(
            functions.modul(functions.power(functions.add(2, 2), 2), 5),
            1
        )
        
        self.assertAlmostEqual(
            functions.mult(functions.power(2, 3), functions.sin(90)),
            8.0
        )
        
        self.assertEqual(
            functions.add(functions.floor(3.7), functions.ceil(2.3)),
            6
        )
        
        functions.memory_clear(0)
        functions.memory_store(functions.mult(5, 2))
        functions.memory_add(functions.div(15, 3))
        functions.memory_subtract(functions.power(2, 2))
        self.assertEqual(functions.memory_recall(0), 11)
        
        self.assertEqual(
            functions.add(
                functions.mult(3, 4),
                functions.div(
                    functions.power(2, 3),
                    2
                )
            ),
            16
        )


if __name__ == '__main__':
    unittest.main()