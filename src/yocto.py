# -*- coding: utf-8 -*-

# To run in command line mode:
#   python src\yocto.py 1 1 < egs\t.y

import io
import sys
from fractions import Fraction

from engine import runProgram

if __name__ == '__main__':

  #ref: https://stackoverflow.com/questions/16549332
  input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
  
  # read program from stdin
  program = []  
  for line in input_stream: 
    program.append(line.rstrip())
    
  # print(program)

  # read arguments
  args = [0] * (len(sys.argv)-1)
  for (i,arg) in enumerate(sys.argv[1:]):
    try:
      x = Fraction(int(arg))
    except:
      x = list(arg)
    args[i] = x
      
  output = runProgram(program, args)
  if output != None:
    print(output)
