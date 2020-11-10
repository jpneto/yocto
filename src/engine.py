# -*- coding: utf-8 -*-
from fractions import Fraction

import src.operators as op

#########################################################################

def runProgram(program, args, verbose=False):
  """
  program : list of strings with function definitions (one per index)
  args    : list of arguments
  verbose : if true prints final stack state
  """
  
  ### strip comments
  for (i,line) in enumerate(program):
    line = line.lstrip(' \t')  # remove leftmost whitespaces
    if line.count('#') > 0:
      if line.index('#') == 0: # entire line is a comment
        continue
      else:
        program[i] = program[i][1:program.index('#')]

  ### initialize stack with arguments
  stack = list(args)               # save a copy of args
  
  ### prepare program state
  state = {}
  state['func_code'] = program[-1] # last line is main function
  state['arity']     = len(args)   # function arity
  state['vars']      = {}          # local variables
  state['blocks']    = []          # stacked blocks
  
  # push inputs into parameters variables and save them in state
  parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
  for i in range(state['arity']):
    state[parameter_symbols[i]] = args.pop()
  ### end prepare state
  
  ### run program with initial stack and state
  stack = run(program, stack, state)
  
  ### in verbose mode, show remaining stack values (if any)
  if verbose:
    print('----- top stack  -----')
    result = None
    for x in stack[::-1]:
      result = outputValue(x)
      if verbose:
        print(result)
    print('------ bottom ------')
  
  ### by default, we output the stack's top (or None if empty)
  return outputValue(stack[-1]) if len(stack)>0 else None
  
#########################################################################  
  
def run(program, stack, state, counter=0):
  """
  program : a list of strings containing the entire program
  stack   : the current values at program stack
  state   : the current information defining the program state
  counter : which index should be processed next from string
            state['func_code'] (the current function)
  """
  
  code = state['func_code']
  while counter < len(code):
    
    symbol = code[counter]
    
    if symbol in r' \t\n':           # skip spaces
      counter += 1
      
    elif symbol in '_0123456789':    # a number
      num, counter = readNumber(code, counter)
      stack.append(Fraction(num,1))
      
    elif symbol in '¹²³⁴⁵⁶⁷⁸⁹⁰' :    # a function parameter
      stack.append(state[symbol])
      counter += 1
      
    elif symbol == '"':              # a string
      string, counter = readString(code, counter)
      stack.append(string)  
      counter += 1
      
    elif symbol == '’':              # a string with one char
      string = code[counter+1]
      stack.append(string)
      counter += 2
      
    elif symbol in 'ẇẋẏż':           # a variable definition
      idx = 'ẇẋẏż'.index(symbol)
      state['vars']['wxyz'[idx]] = stack.pop()
      counter += 1

    elif symbol in 'wxyzï':          # a variable use
      stack.append(state['vars'][symbol])
      counter += 1

    elif symbol in '?⁇':            # conditionals
      counter = runIf(program, stack, state, counter, symbol!='?')

    elif symbol in 'FG':            # FOR loop
      counter = runForLoop(program, stack, state, counter, symbol=='G')

    elif symbol in 'R':             # REPEAT loop
      counter = runRepeatLoop(program, stack, state, counter)

    elif symbol in 'W':             # WHILE loop
      counter = runWhileLoop(program, stack, state, counter)

    elif symbol in '{':             # block expression
      block, counter = readBlock(code, counter+1)  # +1 skips '{'
      state['blocks'].append(block)
    
    elif symbol in op.mapping:      # default operation
      operation = op.mapping[symbol]
      operation(stack)
      counter += 1
  
    elif symbol in 'δλνμ':          # a function call
      counter += 1          # δ nullary function, λ unary (etc.)
      func_state = {}       
      func_state['blocks'] = [] # function calls don't share blocks
      
      # prepare state for function call
      if code[counter] in '0123456789': 
        function_id, counter    = readNumber(code, counter)
        func_state['arity']     = 'δλνμ'.index(symbol)
        func_state['vars']      = {}
        func_state['func_code'] = program[function_id]

      runFunction(program, stack, func_state)
      
    else:
      # unassigned symbol (do nothing). If needed, use symbol ¤
      counter += 1
  
  return stack

############################################

def runFunction(program, stack, state, counter=0):
  # consume enough stack to initialize parameter symbols
  parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
  for i in range(state['arity']):
    state[parameter_symbols[i]] = stack.pop()
  
  # prepare stack to run function, ie, automatically push 
  # parameters into stack to use them implicitly in function
  for symbol in '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']]:
    stack.append(state[symbol])
  
  run(program, stack, state)

############################################

def runIf(program, stack, state, counter, isIfThenElse):
  
  block1 = state['blocks'].pop()
  if isIfThenElse:                  # block2 block1 IF
    block2 = state['blocks'].pop()  #  then   else
    
  x = stack.pop()
  if isTrue(x) or isIfThenElse:
    ifState = {}
    ifState['arity']  = state['arity']
    ifState['vars']   = state['vars']
    ifState['blocks'] = []
    parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
    for i in range(state['arity']):
      ifState[parameter_symbols[i]] = state[parameter_symbols[i]]

    ifState['func_code'] = block2 if isTrue(x) and isIfThenElse else block1
    run(program, stack, ifState)
 
  return counter + 1
 
############################################
  
# stack top can be Fraction, list of Fractions
def runForLoop(program, stack, state, counter, invert):

  loopBlock = state['blocks'].pop()
  loopState = {}
  loopState['arity']  = state['arity']
  loopState['vars']   = state['vars']
  parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
  for i in range(state['arity']):
    loopState[parameter_symbols[i]] = state[parameter_symbols[i]]
  loopState['blocks'] = []
  
  x = stack.pop()
  # there are two options, stack's top is a number or a indexed type
  if (isinstance(x, Fraction)):
    # regular for loop
    for i in range(int(x)):
      if invert:
        i = int(x)-i-1
      # a for-loop place the progress variable at the block's beginning
      loopState['func_code'] = fracToStr(i) + ' ' + loopBlock  # loop body        
      loopState['vars']['ï'] = Fraction(i)  # progress variable
      run(program, stack, loopState)
      
  else: # or else, it is a for-each
    if invert:
      x = x[::-1]
    for i in x:
      # a for-loop place the progress variable at the block's beginning
      loopState['func_code'] = fracToStr(i) + ' ' + loopBlock  # loop body        
      loopState['vars']['ï'] = Fraction(i)  # progress variable
      run(program, stack, loopState)
    
  return counter+1

############################################

# stack top can be Fraction, list of Fractions
# same as For without the progress variable
def runRepeatLoop(program, stack, state, counter):

  loopBlock = state['blocks'].pop()
  loopState = {}
  loopState['arity']  = state['arity']
  loopState['vars']   = state['vars']
  parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
  for i in range(state['arity']):
    loopState[parameter_symbols[i]] = state[parameter_symbols[i]]
  loopState['blocks'] = []
  
  x = stack.pop()
  # there are two options, stack's top is a number or a indexed type
  if (isinstance(x, Fraction)):
    # regular for loop
    for i in range(int(x)):
      # a for-loop place the progress variable at the block's beginning
      loopState['func_code'] = loopBlock  # loop body        
      run(program, stack, loopState)
      
  else: # or else, it is a for-each
    for i in x:
      # a for-loop place the progress variable at the block's beginning
      loopState['func_code'] = loopBlock  # loop body        
      run(program, stack, loopState)
    
  return counter+1

############################################

def runWhileLoop(program, stack, state, counter):
  loopBlock = state['blocks'].pop()

  loopState = {}
  loopState['arity']     = state['arity']
  loopState['vars']      = state['vars']  
  parameter_symbols = '¹²³⁴⁵⁶⁷⁸⁹⁰'[:state['arity']][::-1]
  for i in range(state['arity']):
    loopState[parameter_symbols[i]] = state[parameter_symbols[i]]  
  loopState['blocks']    = []
  loopState['func_code'] = loopBlock  # loop body        
  
  while isTrue(stack.pop()):
    run(program, stack, loopState)
  
  return counter + 1

############################################

def fracToStr(i):
  if int(i) == i:
    return ' ' + str(int(i)) + ' '
  else:
    return i.numerator + ' ' + i.denominator + ' / '

############################################

def readNumber(code, counter):
  
  if code[counter] == '_':
    negative = True
    counter += 1
  else:
    negative = False

  num = 0
  while counter < len(code) and code[counter] in '0123456789':
    num = num*10 + int(code[counter])
    counter += 1
    
  num = -num if negative else num
  return (num, counter)

############################################

def readString(code, counter):
  result = ''
  counter += 1
  while code[counter] != '"':
    result += code[counter]
    counter  += 1
  return (result, counter)    

############################################
 
def readBlock(code, counter):
  level = 0
  result = ''
  while code[counter] != '}' or level > 0:
    result += code[counter]
    if code[counter] == '{':
      level += 1
    if code[counter] == '}':
      level -= 1
    counter += 1
  return (result, counter+1)  # +1 skips last '}'

############################################

# translate final result (which can be from diff types) for simple output
def outputValue(value):
  if isinstance(value, list) and len(value)>0 and isinstance(value[0], str):
    return ''.join(value)
  elif isinstance(value, list):
    return [ outputValue(x) for x in value ]
  else:
    return getValue(value)
   
def getValue(value):
  if isinstance(value, Fraction):
    if int(value) == value:
      return int(value)
    else:
      return float(value)
  else:
    return str(value)

############################################

# checks which is the highest parameter mentioned
# at the function code, that is its arity
def compute_arity(function_code):
  params = '¹²³⁴⁵⁶⁷⁸⁹'[::-1]
  for (i,c) in enumerate(params):
    if c in function_code:
      return 9-i
  return 0

############################################

def isTrue(x):
  if isinstance(x, Fraction):
    return x!=0
  if isinstance(x, list) or isinstance(x, str):
    return len(x)>0

############################################

#prints the 5 largets prime numbers under 100, in descending order.
# program  = ['¹>','¹┅ṗ¹Ḟ0_5:ḷ']  # filter using func 0
# data     = [Fraction(100)]
# print(runProgram(program, data))

# program  = ['"abc"…']  # filter using func 0
# data     = []
# runProgram(program, data, True)


# program  = ['¹ẇ1{w,↓ẇw}W']  
# program  = ['¹{ ↑ẇ1{ w,↓ẇw } W¶ }F']  
# program  = ['¹{┅.}F']  
# program  = ['{↑’**.}F']
# data     = [Fraction(5)]

# program  = ['5┅ 2î']
# program  = ['"dz" 4… *']
# data     = [Fraction(5)]

# program  = ['5┅ḷẇ wḣ. wṫ. wḥ. wṭ. Ȧḥḷ.']
# data     = []

#program = ['50ẇ 0Lṫ{w}?']
#program = ['ẇw2<{1}{w2-λw↓λ+}⁇.']  
# program = ['↕,²,+.' , '1 1¹{ν0}R.'] 
# data = [Fraction(5)]
# runProgram(program, data, True)

############

program = [' 15 "ff" B ']
data = [Fraction(5)]
output = runProgram(program, data, True)
print('output =', output)
