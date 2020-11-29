# -*- coding: utf-8 -*-

import unittest
import math

from fractions import Fraction

from src.engine import runProgram

class TestStringMethods(unittest.TestCase):
  
  def test_dup(self):
    program  = ['🡕🡕++']
    data     = [Fraction(6)]
    output   = runProgram(program, data)
    expected = 18
    self.assertEqual(output, expected)

  def test_pop(self):
    program  = ['🡕🡔🡕+']
    data     = [Fraction(6)]
    output   = runProgram(program, data)
    expected = 12
    self.assertEqual(output, expected)

  def test_clear1(self):
    program  = ['¹¹¹¹🡗']
    data     = [Fraction(6)]
    output   = runProgram(program, data)
    expected = None
    self.assertEqual(output, expected)

  def test_clear2(self):
    program  = ['🡗']
    data     = []
    output   = runProgram(program, data)
    expected = None
    self.assertEqual(output, expected)

  def test_size(self):
    program  = ['¹¹+¹+¹🡖']
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = 3
    self.assertEqual(output, expected)
    
  def test_divide1(self):
    program  = ['1 2/']
    data     = []
    output   = runProgram(program, data)
    expected = 0.5
    self.assertEqual(output, expected)
    
  def test_divide2(self):
    program  = ['15 2÷']
    data     = []
    output   = runProgram(program, data)
    expected = 7
    self.assertEqual(output, expected)

  def test_func1(self):
    program  = ['¹+','λ0+']
    data     = [Fraction(6),Fraction(2)]
    output   = runProgram(program, data)
    expected = 10
    self.assertEqual(output, expected)

  def test_func2(self):
    program  = ['¹¹*','3λ0']
    data     = []
    output   = runProgram(program, data)
    expected = 9
    self.assertEqual(output, expected)

  def test_var(self):
    program  = ['10ẋx🡕+']
    data     = []
    output   = runProgram(program, data)
    expected = 20
    self.assertEqual(output, expected)
  
  def test_frac1(self):
    program  = ['3 2 /']
    data     = []
    output   = runProgram(program, data)
    expected = 1.5
    self.assertEqual(output, expected)

  def test_base1(self):
    program  = ['"ff"’gB']
    data     = []
    output   = runProgram(program, data)
    expected = 255 # 'ff' in base 16 (g has codepage id 16)
    self.assertEqual(output, expected)

  def test_base2(self):
    program  = ['10 8B']
    data     = []
    output   = runProgram(program, data)
    expected = 8
    self.assertEqual(output, expected)

  def test_base3(self):
    program  = ['"100"8B']
    data     = []
    output   = runProgram(program, data)
    expected = 64 
    self.assertEqual(output, expected)

  def test_dec1(self):
    program  = ['"bcd"↓']
    data     = []
    output   = runProgram(program, data)
    expected = 'abc'
    self.assertEqual(output, expected)
    
  def test_pow1(self):
    program  = ['2½^'] 
    data     = []
    output   = runProgram(program, data)
    expected = math.sqrt(2)
    self.assertAlmostEqual(float(output), expected, places=9)

  # def test_primality(self):
  #   program  = ['"abcde"ṗp']
  #   data     = []
  #   output   = runProgram(program, data)
  #   expected = [1]*5
  #   self.assertEqual(output, expected)

  def test_sum_lists1(self):
    program  = ['"abcdefg" "02"+']
    data     = []
    output   = runProgram(program, data)
    expected = 'abcdefg02'
    self.assertEqual(output, expected)

  def test_explode_implode(self):
    program  = ['…ėẹ'] 
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = [4, 3, 2, 1, 0]
    self.assertEqual(output, expected)

  def test_len(self):
    program  = ['…l'] 
    data     = [Fraction(50)]
    output   = runProgram(program, data)
    expected = 50
    self.assertEqual(output, expected)

  def test_range_implode(self):
    program  = ['3…4…ẹ']
    data     = []
    output   = runProgram(program, data)
    expected = [[0, 1, 2, 3], [0, 1, 2]]
    self.assertEqual(output, expected)
    
  def test_for1(self):
    program  = ['1¹{↑*}F']  # factorial with for
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = 120
    self.assertEqual(output, expected)
    
  def test_for2(self):
    program  = ['0 4{ï*+}F']  # produces squares and sum them
    data     = []
    output   = runProgram(program, data)
    expected = 14  # sums [0,1,4,9]
    self.assertEqual(output, expected)

  def test_for_zeroIters(self):
    program  = ['0{ï*}F']  # cycles zero times
    data     = []
    output   = runProgram(program, data)
    expected = None
    self.assertEqual(output, expected)

  def test_for_sciFormat(self):
    program  = ['½3E*']  # half of 1000
    data     = []
    output   = runProgram(program, data)
    expected = 500
    self.assertEqual(output, expected)
    
  def test_multiples(self):
    program  = ['🡕┅↕L*']    # create [n,n*2,n*3,...,n*n]
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = [5,10,15,20,25]
    self.assertEqual(output, expected)
    
  def test_append_begin(self):
    program  = ['3┅6ạ']    
    data     = []
    output   = runProgram(program, data)
    expected = [1,2,3,6]
    self.assertEqual(output, expected)

  def test_append_end(self):
    program  = ['3┅6ȧ']    
    data     = []
    output   = runProgram(program, data)
    expected = [6,1,2,3]
    self.assertEqual(output, expected)
    
  def test_2fors(self):
    program  = ['4{ẇï{🡔wï 2Ḷ}F }Fẹḷ']    # testing second, internal ï
    data     = []
    output   = runProgram(program, data)
    expected = [[0, 1], [0, 2], [1, 2], [0, 3], [1, 3], [2, 3]]
    self.assertEqual(output, expected)
    
  def test_fibonacci(self):
    program  = ['↕²+' , '1 1¹{ν0}R']    # a,b = b,a+b
    data     = [Fraction(15)]
    output   = runProgram(program, data)
    expected = 1597
    self.assertEqual(output, expected)

  def test_factorial_recursive(self):
    program  = ['0={1}{¹↓λ0¹*}⁇','λ0']    # n! = n * (n-1)!
    data     = [Fraction(7)]
    output   = runProgram(program, data)
    expected = 5040
    self.assertEqual(output, expected)

  def test_fibonacci_recursive(self):
    program  = ['2<{1}{¹2-λ0¹↓λ0+}⁇']    # fib(n) = fib(n-2) + fib(n-1)
    data     = [Fraction(7)]
    output   = runProgram(program, data)
    expected = 21
    self.assertEqual(output, expected)
  
  def test_eval(self):
    program  = ['15ẋ "x 2÷"ẇ wə']
    data     = []
    output   = runProgram(program, data)
    expected = 7
    self.assertEqual(output, expected)

  def test_map1(self):
    program  = ['2*','3-','8…1Ṁ']
    data     = []
    output   = runProgram(program, data)
    expected = [-3, -2, -1, 0, 1, 2, 3, 4]
    self.assertEqual(output, expected)
    
  def test_map2(self):
    program  = ['2*','3-','8…0Ṁ']
    data     = []
    output   = runProgram(program, data)
    expected = [0, 2, 4, 6, 8, 10, 12, 14]
    self.assertEqual(output, expected)

  def test_filter1(self):
    program  = ['2<','2>','8…1Ḟ 8…0Ḟ +']
    data     = []
    output   = runProgram(program, data)
    expected = [3, 5, 5, 7, 7]
    self.assertEqual(output, expected)

  def test_reduce1(self):
    program  = ['+','5┅ 0 0Ṙ']   # fold (+) 0 xs
    data     = []
    output   = runProgram(program, data)
    expected = 15
    self.assertEqual(output, expected)

  def test_reduce2(self):
    program  = ['*','┅1 0Ṙ']   # fold (*) 1 xs
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = 120
    self.assertEqual(output, expected)
    
  def test_scan1(self):
    program  = ['*','8┅ 1 0Ṡ']   # fold (*) 1 xs
    data     = [Fraction(5)]
    output   = runProgram(program, data)
    expected = [1, 1, 2, 6, 24, 120, 720, 5040, 40320]
    self.assertEqual(output, expected)
 
  # https://codegolf.stackexchange.com/questions/58615/
  def test_fizzBuzz(self):
    program = ['Lw*', '3%¬', '5%¬', 
               '3%¹5%&', 'c',
               'ẇw┅ẋ "Fizz"λ0x1Ṁ* "Buzz"λ0x2Ṁ* 4Ż x3Ċ 4Ż']  # 56 bytes
    data     = [Fraction(10)]
    output   = runProgram(program, data)
    expected = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz']
    self.assertEqual(output, expected)
    
  def test_fizzBuzz2(self):
    program = ['Lw*', '3%¬', '5%¬', 
               '3%¹5%&', 'c',
               '2Eẇw┅ẋ"Fizz"λ0x1Ṁ*"Buzz"λ0x2Ṁ*4Żx3Ċ4Ż']  # 58 bytes
    data     = []
    output   = runProgram(program, data)
    expected = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz', 'Fizz', '22', '23', 'Fizz', 'Buzz', '26', 'Fizz', '28', '29', 'FizzBuzz', '31', '32', 'Fizz', '34', 'Buzz', 'Fizz', '37', '38', 'Fizz', 'Buzz', '41', 'Fizz', '43', '44', 'FizzBuzz', '46', '47', 'Fizz', '49', 'Buzz', 'Fizz', '52', '53', 'Fizz', 'Buzz', '56', 'Fizz', '58', '59', 'FizzBuzz', '61', '62', 'Fizz', '64', 'Buzz', 'Fizz', '67', '68', 'Fizz', 'Buzz', '71', 'Fizz', '73', '74', 'FizzBuzz', '76', '77', 'Fizz', '79', 'Buzz', 'Fizz', '82', '83', 'Fizz', 'Buzz', '86', 'Fizz', '88', '89', 'FizzBuzz', '91', '92', 'Fizz', '94', 'Buzz', 'Fizz', '97', '98', 'Fizz', 'Buzz']
    self.assertEqual(output, expected)    

  def test_fizzBuzz3(self):
    program = ['3*','5*','15*',
               '101…ẇww0Ṁ"Fizz"Vw1Ṁ"Buzz"Vw2Ṁ"FizzBuzz"Vṫ'] # 51 bytes
    data     = []
    output   = runProgram(program, data)
    expected = [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34, 'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz', 'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz', 'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz', 'Buzz']
    self.assertEqual(output, expected)   
    
  def test_fizzBuzz4(self):
    program = ['3%¹5%&','c', 
               '2E┅0ĊØ2*"Fizz"ạ34*1ŻØ4*"Buzz"ạ34*1Ż'] # 34 bytes
    data     = []
    output   = runProgram(program, data)
    expected = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz', 'Fizz', '22', '23', 'Fizz', 'Buzz', '26', 'Fizz', '28', '29', 'FizzBuzz', '31', '32', 'Fizz', '34', 'Buzz', 'Fizz', '37', '38', 'Fizz', 'Buzz', '41', 'Fizz', '43', '44', 'FizzBuzz', '46', '47', 'Fizz', '49', 'Buzz', 'Fizz', '52', '53', 'Fizz', 'Buzz', '56', 'Fizz', '58', '59', 'FizzBuzz', '61', '62', 'Fizz', '64', 'Buzz', 'Fizz', '67', '68', 'Fizz', 'Buzz', '71', 'Fizz', '73', '74', 'FizzBuzz', '76', '77', 'Fizz', '79', 'Buzz', 'Fizz', '82', '83', 'Fizz', 'Buzz', '86', 'Fizz', '88', '89', 'FizzBuzz', '91', '92', 'Fizz', '94', 'Buzz', 'Fizz', '97', '98', 'Fizz', 'Buzz']
    self.assertEqual(output, expected)   

  # https://codegolf.stackexchange.com/questions/215449/  
  def test_codegolf1(self):
    program  = ['Σ9%↕Σ9%='] 
    data     = ["HMCZQZZRC", "SIQYOBXK"]
    output   = runProgram(program, data)
    expected = 1
    self.assertEqual(output, expected)   
    
  # https://codegolf.stackexchange.com/questions/215607/
  def test_codegolf2(self):
    program  = ['↕¹²>¨*¨÷⁇','┅↑1 0Ṡ'] 
    data     = [Fraction(20)]
    output   = runProgram(program, data)
    expected = [1, 2, 6, 1, 5, 30, 4, 32, 3, 30, 2, 24, 1, 14, 210, 13, 221, 12, 228, 11, 231]
    self.assertEqual(output, expected)   
    
  # https://codegolf.stackexchange.com/questions/215522/
  def test_codegolf3(self):
    program = ['"uber"↕+','w*','"suv""black""plus""xl"’xẹ0Ṁ','1=','↕ẇ1Ṁ20≤3Ḟl↓ẇδ2wî']
    data = [Fraction(30), 
            [Fraction(0.3), Fraction(0.5), Fraction(0.7), 
             Fraction(1), Fraction(1.3)]]
    output   = runProgram(program, data)
    expected = 'uberxl'
    self.assertEqual(output, expected)   

  def test_codegolf3b(self):
    program = ['"uber"↕+','w*','"suv""black""plus""xl"’xẹ0Ṁ','1=','↕ẇ1Ṁ20≤3Ḟl↓ẇδ2wî']
    data = [Fraction(20), 
            [Fraction(0.3), Fraction(0.5), Fraction(0.7), 
             Fraction(1), Fraction(1.3)]]
    output   = runProgram(program, data)
    expected = 'uberblack'
    self.assertEqual(output, expected)   

  def test_codegolf3c(self):
    program = ['"uber"↕+','w*','"suv""black""plus""xl"’xẹ0Ṁ','1=','↕ẇ1Ṁ20≤3Ḟl↓ẇδ2wî']
    data = [Fraction(15), 
            [Fraction(0.3), Fraction(0.5), Fraction(0.7), 
             Fraction(1), Fraction(1.3)]]
    output   = runProgram(program, data)
    expected = 'ubersuv'
    self.assertEqual(output, expected)   
   
if __name__ == '__main__':
    unittest.main()




