# -*- coding: utf-8 -*-
from fractions import Fraction
from itertools import cycle

from codepage import toChr, toOrd, codepage

def dup(stack):
  stack.append(stack[-1])

def pop(stack):
  stack.pop()

def swap(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(b)
  stack.append(a)

def clear_stack(stack):
  stack.clear()

def pass_command(stack):
  pass

def push_size(stack):
  stack.append(Fraction(len(stack)))

def half(stack):
  stack.append(Fraction(1,2))
  
### 'arithmetic' operators ###

def increment(stack):
  a = stack.pop()
  stack.append(inc_types(a))

def inc_types(x):
  if isinstance(x,Fraction):
    return x+1
  elif isinstance(x,str):
    return ''.join( [ toChr(toOrd(c)+1) for c in x ] ) 
  elif isinstance(x,list):
    return [inc_types(i) for i in x]
  
def decrement(stack):
  a = stack.pop()
  stack.append(dec_types(a))

def dec_types(x):
  if isinstance(x,Fraction):
    return x-1
  elif isinstance(x,str):
    return ''.join( [ toChr(toOrd(c)-1) for c in x ] ) 
  elif isinstance(x,list):
    return [dec_types(i) for i in x]

def addition(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(addition_types(a,b))

def addition_types(x,y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x+y

  elif isinstance(x,Fraction) and isinstance(y,str):
    return ''.join( [ toChr(toOrd(c)+int(x)) for c in y ] ) 
  elif isinstance(x,str) and isinstance(y,Fraction):
    return ''.join( [ toChr(toOrd(c)+int(y)) for c in x ] ) 
  
  elif isinstance(x,str) and isinstance(y,str):
    return x+y
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ addition_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ addition_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ addition_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ addition_types(i,y) for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ addition_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ addition_types(i,j) for (i,j) in zip(cycle(x),y) ]
    
def subtraction(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(subtraction_types(a,b))

def subtraction_types(x,y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x-y

  elif isinstance(x,Fraction) and isinstance(y,str):
    return ''.join( [ toChr(toOrd(c)-int(x)) for c in y ] )
  elif isinstance(x,str) and isinstance(y,Fraction):
    return ''.join( [ toChr(toOrd(c)-int(y)) for c in x ] )

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(toOrd(i)-toOrd(j)) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(toOrd(i)-toOrd(j)) for (i,j) in zip(cycle(x),y) ]    
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ subtraction_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ subtraction_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ subtraction_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ subtraction_types(i,y) for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ subtraction_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ subtraction_types(i,j) for (i,j) in zip(cycle(x),y) ]
    
def product(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(product_types(a,b))

def product_types(x,y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x*y

  elif isinstance(x,Fraction) and isinstance(y,str):
    return int(x)*y
  elif isinstance(x,str) and isinstance(y,Fraction):
    return x*int(y)

  elif isinstance(x,str) and isinstance(y,str):
    return [ [i+j] for i in x for j in y ] # cartesian product
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return y*int(x)
  elif isinstance(x,list) and isinstance(y,Fraction):
    return x*int(y)

  elif isinstance(x,str) and isinstance(y,list):
    return [ [product_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [product_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ product_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ product_types(i,j) for (i,j) in zip(cycle(x),y) ]

def quocient(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(quocient_types(a,b))

def quocient_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(x//y)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(x // toOrd(c)) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [Fraction(toOrd(c) // y) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(toOrd(i)//toOrd(j)) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(toOrd(i)//toOrd(j)) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ quocient_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ quocient_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [quocient_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [quocient_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ quocient_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ quocient_types(i,j) for (i,j) in zip(cycle(x),y) ]

def module(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(module_types(a,b))
  
def module_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x%y

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(x % toOrd(c)) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(toOrd(c) % y) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(toOrd(i)%toOrd(j)) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(toOrd(i)%toOrd(j)) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ module_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ module_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [module_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [module_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ module_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ module_types(i,j) for (i,j) in zip(cycle(x),y) ]  

def make_fraction(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(fraction_types(a,b))
  
def fraction_types(x,y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(x,y).limit_denominator()
  
  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(x,toOrd(c)) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(toOrd(c),y) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(toOrd(i),toOrd(j)) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(toOrd(i),toOrd(j)) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ fraction_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ fraction_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [fraction_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [fraction_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ fraction_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ fraction_types(i,j) for (i,j) in zip(cycle(x),y) ]  

def power(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(power_types(a,b))

def power_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x**y

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(x ** toOrd(c)) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(toOrd(c) ** y) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(toOrd(i)**toOrd(j)) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(toOrd(i)**toOrd(j)) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ power_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ power_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [power_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [power_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ power_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ power_types(i,j) for (i,j) in zip(cycle(x),y) ]  

def less_than(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(less_than_types(a,b))
    
def less_than_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x<y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x<toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)<y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i<j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i<j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ less_than_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ less_than_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [less_than_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [less_than_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ less_than_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ less_than_types(i,j) for (i,j) in zip(cycle(x),y) ]     

def greater_than(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(greater_than_types(a,b))
    
def greater_than_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x>y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x>toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)>y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i>j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i>j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ greater_than(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ greater_than(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [greater_than(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [greater_than(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ greater_than(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ greater_than(i,j) for (i,j) in zip(cycle(x),y) ]     

def less_eq_than(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(less_eq_than_types(a,b))
    
def less_eq_than_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x<=y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x<=toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)<=y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i<=j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i<=j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ less_eq_than_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ less_eq_than_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [less_eq_than_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [less_eq_than_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ less_eq_than_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ less_eq_than_types(i,j) for (i,j) in zip(cycle(x),y) ]     

def greater_eq_than(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(greater_eq_than_types(a,b))
    
def greater_eq_than_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x>=y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x>=toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)>=y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i>=j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i>=j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ greater_eq_than_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ greater_eq_than_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [greater_eq_than_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [greater_eq_than_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ greater_eq_than_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ greater_eq_than_types(i,j) for (i,j) in zip(cycle(x),y) ]     

def equals(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(equal_types(a,b))
  
def equal_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x==y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x==toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)==y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i==j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i==j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ equal_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ equal_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [equal_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [equal_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ equal_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ equal_types(i,j) for (i,j) in zip(cycle(x),y) ]    

def different(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(different_types(a,b))
  
def different_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x!=y else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x!=toOrd(c) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)!=y else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if i!=j else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if i!=j else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ different_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ different_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [different_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [different_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ different_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ different_types(i,j) for (i,j) in zip(cycle(x),y) ]    

def apply_or(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(apply_or_types(a,b))
  
def apply_or_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x!=0 or y!=0 else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x!=0 or toOrd(c)!=0 else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)!=0 or y!=0 else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if toOrd(i)!=0 or toOrd(j)!=0 else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if toOrd(i)!=0 or toOrd(j)!=0 else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ apply_or_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ apply_or_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [apply_or_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [apply_or_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ apply_or_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ apply_or_types(i,j) for (i,j) in zip(cycle(x),y) ]    

def apply_and(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(apply_and_types(a,b))
  
def apply_and_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if x!=0 and y!=0 else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if x!=0 and toOrd(c)!=0 else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if toOrd(c)!=0 and y!=0 else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if toOrd(i)!=0 and toOrd(j)!=0 else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if toOrd(i)!=0 and toOrd(j)!=0 else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ apply_and_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ apply_and_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [apply_and_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [apply_and_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ apply_and_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ apply_and_types(i,j) for (i,j) in zip(cycle(x),y) ]    

def apply_xor(stack):
  b = stack.pop()
  a = stack.pop()
  stack.append(apply_xor_types(a,b))
  
# n1,n2 are numbers  
def xor(n1,n2):
  return (n1==0 and n2!=0) or (n1!=0 and n2==0)
  
def apply_xor_types(x,y):
  
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction(1) if xor(x,y) else Fraction(0)

  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ Fraction(1) if xor(x,toOrd(c)) else Fraction(0) for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return [ Fraction(1) if xor(toOrd(c),y) else Fraction(0) for c in x ]

  elif isinstance(x,str) and isinstance(y,str):
    if len(x) > len(y):
      return [ Fraction(1) if xor(toOrd(i),toOrd(j)) else Fraction(0) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ Fraction(1) if xor(toOrd(i),toOrd(j)) else Fraction(0) for (i,j) in zip(cycle(x),y) ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ apply_xor_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ apply_xor_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [apply_xor_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [apply_xor_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ apply_xor_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ apply_xor_types(i,j) for (i,j) in zip(cycle(x),y) ]    

def apply_not(stack):
  x = stack.pop()
  stack.append(apply_not_types(x)) 

def apply_not_types(x):
  if isinstance(x,Fraction):
    return Fraction(1) if x==0 else Fraction(0)
  elif isinstance(x,str):
    return [ apply_not_types(Fraction(toOrd(c))) for c in x ]
  elif isinstance(x,list):
    return [apply_not_types(i) for i in x]  

def make_ord(stack):
  x = stack.pop()
  stack.append(make_ord_types(x)) 

def make_ord_types(x):
  if isinstance(x,Fraction):
    return [ Fraction(toOrd(c)) for c in str(x) ]
  elif isinstance(x,str):
    return [ Fraction(toOrd(c)) for c in x ]
  elif isinstance(x,list):
    return [make_ord_types(i) for i in x]  

def factorial(stack):
  x = stack.pop()
  stack.append(factorial_types(x)) 

def factorial_types(x):
  if isinstance(x,Fraction):
    fact = Fraction(1)
    for i in range(1,1+int(x)): 
      fact = fact * i 
    return fact
  elif isinstance(x,str):
    return [ factorial_types(Fraction(toOrd(c))) for c in x ]
  elif isinstance(x,list):
    return [factorial_types(i) for i in x]  

def base(stack):
  base  = stack.pop()
  value = stack.pop()
  stack.append(base_types(value, base))
  
def base_types(value, base):
  if isinstance(value,Fraction) and isinstance(base,Fraction):
    result = int(str(int(value)), int(base)) # value must be string
    return Fraction(result, 1)

  elif isinstance(value,Fraction) and isinstance(base,str):
    return [ Fraction( int(str(int(value)), toOrd(c)) ) for c in base ]
  elif isinstance(value,str) and isinstance(base,Fraction):
    result = int(value, int(base)) 
    return Fraction(result, 1)

  elif isinstance(value,str) and isinstance(base,str):
    if len(base) == 1:
      return base_types(value, Fraction(toOrd(base))) 
    else:
      return [ base_types(value, Fraction(toOrd(b))) for b in base ]

  elif isinstance(value,Fraction) and isinstance(base,list):
    return [ base_types(value, b) for b in base ] 
  elif isinstance(value,list) and isinstance(base,Fraction):
    return [ base_types(v, base) for v in value ]

  elif isinstance(value,str) and isinstance(base,list):
    return [ base_types(value, b) for b in base ] 
  elif isinstance(value,list) and isinstance(base,str):
    return [ base_types(v, base) for v in value ]

  # base can be a char, use codepage value to convert
  elif isinstance(value,list) and isinstance(base,list):
    if len(value) > len(base):
      return [ base_types(i,j) for (i,j) in zip(value,cycle(base)) ]
    else:
      return [ base_types(i,j) for (i,j) in zip(cycle(value),base) ]

def sci_format(stack):
  x = stack.pop()
  stack.append(sci_format_types(x))

def sci_format_types(x):
  if isinstance(x,Fraction):
    if x==int(x):
      return Fraction(10**x).limit_denominator(10**abs(int(x)))
    else:
      return Fraction(10**x).limit_denominator(10**abs(int(x))*1000)
  elif isinstance(x,str):
    return [ sci_format_types(Fraction(toOrd(c))) for c in x ]
  elif isinstance(x,list):
    return [ sci_format_types(i) for i in x ]
  
def prime(stack):
  x = stack.pop()
  stack.append(prime_types(x))

def prime_types(x):
  if isinstance(x,Fraction):
    result = nth_prime_number(int(x))
    return Fraction(result)
  elif isinstance(x,str):
    result = nth_prime_number(toOrd(x))
    return Fraction(result)
  elif isinstance(x,list):
    return [ prime_types(i) for i in x ] 
    
# ref: https://stackoverflow.com/questions/48759489
def nth_prime_number(n):
  prime_list = [2]
  num = 3
  while len(prime_list) < n:
    for p in prime_list:
      if num % p == 0:
        break
    else:
      prime_list.append(num)
    num += 2
  return prime_list[-1]

def is_prime(stack):
  x = stack.pop()
  stack.append(is_prime_types(x))

def is_prime_types(x):
  if isinstance(x,Fraction):
    return Fraction(1) * check_prime(int(x))
  elif isinstance(x,str):
    return Fraction(1) * check_prime(int(x))
  elif isinstance(x,list):
    return [ is_prime_types(i) for i in x ]   

# ref: https://stackoverflow.com/questions/15285534
def check_prime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  # since all primes > 3 are of the form 6n ± 1
  # start with f=5 (which is prime)
  # and test f, f+2 for being prime
  # then loop by 6. 
  f = 5
  while f <= r:
    if n % f == 0: return False
    if n % (f+2) == 0: return False
    f += 6
  return True    

######################
### List operators ###
######################

def makeRange0(stack):
  x = stack.pop()
  result = makeRange0_types(x)
  if result != None:
    stack.append(result)
    
def makeRange0_types(x):
  if isinstance(x,Fraction):
    return [ Fraction(i) for i in range(int(x)) ]
  elif isinstance(x, str):
    if x.islower():
      id_a = toOrd('a')
      id_x = toOrd(x)
      return list(codepage[id_a:id_x]) if id_a<id_x else []
    elif x.isupper():
      id_A = toOrd('A')
      id_x = toOrd(x)
      return list(codepage[id_A:id_x])  if id_A<id_x else []
    elif x.isdigit():
      id_0 = toOrd('0')
      id_x = toOrd(x)
      return list(codepage[id_0:id_x])  if id_0<id_x else []
    else:
      return '' # otherwise do nothing  
  elif isinstance(x, list):
    return [ makeRange0_types(i) for i in x ]
  
def makeRange1(stack):
  x = stack.pop()
  result = makeRange1_types(x)
  if result != None:
    stack.append(result)
    
def makeRange1_types(x):   
  if isinstance(x,Fraction):
    return [ Fraction(i) for i in range(1,int(x)+1) ]
  elif isinstance(x, str):    
    if x.islower():
      id_a = toOrd('a')
      id_x = toOrd(x)
      return list(codepage[id_a:id_x+1])
    elif x.isupper():
      id_A = toOrd('A')
      id_x = toOrd(x)
      return list(codepage[id_A:id_x+1])
    elif x.isdigit():
      id_0 = toOrd('1')
      id_x = toOrd(x)
      return list(codepage[id_0:id_x+1])
    else:
      return '' # otherwise do nothing  
  elif isinstance(x, list):
    return [ makeRange1_types(i) for i in x ]
  
def make_list(stack):
  x = stack.pop()
  stack.append(make_list_types(x))
  
def make_list_types(x):
  if isinstance(x,Fraction):
    return [x]
  elif isinstance(x,str):
    return [x] # [ [c] for c in x ]
  elif isinstance(x,list):
    return [ make_list_types(i) for i in x ]

# top must be Float
def make_multiple_list(stack):
  x = stack.pop()
  if isinstance(x,list) or isinstance(x,str):
    return # do nothing
  result = []
  for i in range(int(x)):
    result.append(stack.pop())
  stack.append(result)
    
def append_list_begin(stack):
  x = stack.pop()
  lst = stack.pop()  
  lst.insert(0,x)
  stack.append(lst)
  
def append_list_end(stack):
  x = stack.pop()
  lst = stack.pop()  
  lst.append(x)
  stack.append(lst)  
  
def length(stack):
  x = stack.pop()
  if isinstance(x,Fraction):
    stack.append(Fraction(1))
  if isinstance(x,list) or isinstance(x,str):
    stack.append(Fraction(len(x)))
  
def explode_values(stack):  
  x = stack.pop()
  if isinstance(x,Fraction):
    stack.append(x)
  if isinstance(x,list) or isinstance(x,str):
    for elem in x:
      stack.append(elem)

def implode_values(stack):  
  result = []
  while stack != []:
    result.append(stack.pop())
  stack.append(result)  
  
# does not remove list, only index  
def index(stack):
  idx = stack.pop()
  lst = stack[-1]
  stack.append(index_types(lst, idx))

# same as before, except that removes the list
def index_pop(stack):
  idx = stack.pop()
  lst = stack.pop()
  stack.append(index_types(lst, idx))
  
# return x[y]  
def index_types(x, y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return x.numerator if isTrue(y) else x.denominator 
  
  elif isinstance(x,Fraction) and isinstance(y,str):
    return [ x.numerator if isTrue(c) else x.denominator for c in y ]
  elif isinstance(x,str) and isinstance(y,Fraction):
    return x[int(y)%len(x)]

  elif isinstance(x,str) and isinstance(y,str):
    return [ x[toOrd(c)%len(x)] for c in y ]
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ index_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return x[int(y)] 

  elif isinstance(x,str) and isinstance(y,list):
    return [ [index_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [index_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    if len(x) > len(y):
      return [ index_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    else:
      return [ index_types(i,j) for (i,j) in zip(cycle(x),y) ]    
    
def head_list(stack):
  x = stack.pop()
  if isinstance(x,Fraction):
    return
  if len(x)>0:          # if [] or "" do nothing
    stack.append(x[0])

def tail_list(stack):
  x = stack.pop()
  if isinstance(x,Fraction):
    return
  if len(x)>0:
    stack.append(x[1:])
    
def init_list(stack):
  x = stack.pop()
  if isinstance(x,Fraction):
    return
  if len(x)>0:
    stack.append(x[:-1])

def last_list(stack):
  x = stack.pop()
  if isinstance(x,Fraction):
    return
  if len(x)>0:
    stack.append(x[-1])
  
def invert(stack):
  x = stack.pop()
  stack.append(invert_types(x))

def invert_types(x):
  if isinstance(x,Fraction): 
    if x.numerator!=0:
      return Fraction(x.denominator, x.numerator).limit_denominator()
    else:
      return Fraction(1)
    
  elif isinstance(x,list) or isinstance(x,str): 
    return x[::-1]
  

def make_sum(stack):
  x = stack.pop()
  stack.append(make_sum_types(x))

def make_sum_types(x):
  if isinstance(x,Fraction): 
    digits = str(int(x))
    result = 0
    for d in digits:
      result += int(d)
    return Fraction(result)
  elif isinstance(x,str): 
    return Fraction(sum([int(toOrd(c)) for c in x]))
  elif isinstance(x,list): 
    return Fraction(sum([make_sum_types(i) for i in x]))


def make_prod(stack):
  x = stack.pop()
  stack.append(make_prod_types(x))

def make_prod_types(x):
  if isinstance(x,Fraction): 
    digits = str(int(x))
    result = 1
    for d in digits:
      result *= int(d)
    return Fraction(result)
  elif isinstance(x,str): 
    ords = [int(toOrd(c)) for c in x]
    result = 1
    for d in ords:
      result *= d
    return Fraction(result)
  elif isinstance(x,list): 
    prods = [make_prod_types(i) for i in x]
    result = 1
    for d in prods:
      result *= d
    return Fraction(result)

def make_all(stack):
  x = stack.pop()
  stack.append(make_all_types(x))

def make_all_types(x):
  if isinstance(x,Fraction): 
    return Fraction(1) if x!=0 else Fraction(0)
  elif isinstance(x,str): 
    ords = [int(toOrd(c)) for c in x]
    result = 1
    for d in ords:
      result *= d
    return Fraction(1) if result!=0 else Fraction(0)
  elif isinstance(x,list): 
    prods = [make_all_types(i) for i in x]
    result = 1
    for d in prods:
      result *= d
    return Fraction(1) if result!=0 else Fraction(0)

def make_any(stack):
  x = stack.pop()
  stack.append(make_any_types(x))

def make_any_types(x):
  if isinstance(x,Fraction): 
    return Fraction(1) if x!=0 else Fraction(0)
  elif isinstance(x,str): 
    ords = [int(toOrd(c)) for c in x]
    result = 0
    for d in ords:
      result += d
    return Fraction(1) if result>0 else Fraction(0)
  elif isinstance(x,list): 
    prods = [make_any_types(i) for i in x]
    result = 0
    for d in prods:
      result += d
    return Fraction(1) if result>0 else Fraction(0)

def concatenate(stack):
  idx = stack.pop()
  lst = stack.pop()
  stack.append(concatenate_types(lst, idx))
  
def concatenate_types(x, y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    return Fraction( str(x) + str(y) )
  
  elif isinstance(x,Fraction) and isinstance(y,str):
    return str(x)+y
  elif isinstance(x,str) and isinstance(y,Fraction):
    return x+str(y)

  elif isinstance(x,str) and isinstance(y,str):
    return x+y
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ concatenate_types(x,i) for i in y ]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ concatenate_types(i,y) for i in x ]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [concatenate_types(x,i)] for i in y ]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [concatenate_types(i,y)] for i in x ]

  elif isinstance(x,list) and isinstance(y,list):
    return x+y
    # if len(x) > len(y):
    #   return [ concatenate_types(i,j) for (i,j) in zip(x,cycle(y)) ]
    # else:
    #   return [ concatenate_types(i,j) for (i,j) in zip(cycle(x),y) ]

def list_difference(stack):
  idx = stack.pop()
  lst = stack.pop()
  stack.append(list_difference_types(lst, idx))
  
def list_difference_types(x, y):
  if isinstance(x,Fraction) and isinstance(y,Fraction):
    result = ''.join(set(str(x))-set(str(y)))
    return Fraction(result) if result!='' else ''
  
  elif isinstance(x,Fraction) and isinstance(y,str):
    return ''.join(set(str(x))-set(y))
  elif isinstance(x,str) and isinstance(y,Fraction):
    return ''.join(set(x)-set(str(y)))

  elif isinstance(x,str) and isinstance(y,str):
    return ''.join(set(x)-set(y))
  
  elif isinstance(x,Fraction) and isinstance(y,list):
    return [ list_difference_types(x,i) for i in y if i != x]
  elif isinstance(x,list) and isinstance(y,Fraction):
    return [ list_difference_types(i,y) for i in x if i != y]

  elif isinstance(x,str) and isinstance(y,list):
    return [ [list_difference_types(x,i)] for i in y if i != x]
  elif isinstance(x,list) and isinstance(y,str):
    return [ [list_difference_types(i,y)] for i in x if i != y]

  elif isinstance(x,list) and isinstance(y,list):
    return [elem for elem in x if elem not in y]    

#############################  

def vectorized_assign(stack):
  new_value = stack.pop()
  idxs      = stack.pop()
  values    = stack.pop()
  stack.append(vectorized_assign_types(new_value, idxs, values))
  
def vectorized_assign_types(x, idxs, values):
  if not (isinstance(idxs,list) and isinstance(values,list)):
    return values # leave the original list unchanged
  
  result = values[:] # make a copy
  
  if isinstance(x,Fraction) or isinstance(x,str):
    for idx in idxs:
      if idx >= 0 and idx < len(result):
        result[int(idx)] = x
  
  if isinstance(x,list):
    for (idx,xi) in zip(idxs,cycle(x)):
      result[int(idx)] = xi
    
  return result  

#############################

def lower_letters(stack):
  stack.append("abcdefghijklmnopqrstuvwxyz")

def upper_letters(stack):
  stack.append("ABCDEFGHIJKLMNOPQRSTUWVXYZ")
  
def digits(stack):
  stack.append("0123456789")
  
def print_newline(stack):
  print('')
  
def empty_str_list(stack):
  stack.append([""])
  
def println(stack, end):
  x = stack[-1]
  result = toStr(x)
  if result!='':
    print(result, end=end) 
  
def toStr(x):  
  if isinstance(x, Fraction):
    if int(x) == x:
      return str(int(x))
    else:
      return str(float(x))
  elif isinstance(x, list):
    if len(x)==0:
      return ''
    sep = '' if isinstance(x[0],str) else ' '
    return sep.join([toStr(i) for i in x])
  else:  # is string
    return x
  
def toInt(x):
  if isinstance(x, Fraction):
    return int(x)
  elif isinstance(x, str):
    return toOrd(x)  
  elif isinstance(x, list):
    return len(x)
  
def isTrue(x):
  if isinstance(x, Fraction):
    return x!=0
  if isinstance(x, list) or isinstance(x, str):
    return len(x)>0  

def fracToStr(i):
  if int(i) == i:
    return ' ' + str(int(i)) + ' '
  else:
    return i.numerator + ' ' + i.denominator + ' / '
  
############################################
## define mappings
############################################

mapping = {}

# nullary operators
mapping['🡕'] = dup
mapping['🡖'] = push_size
mapping['🡗'] = clear_stack
mapping['¤'] = pass_command

mapping['½'] = half

mapping['Ȧ'] = upper_letters
mapping['Ạ'] = lower_letters
mapping['Ḍ'] = digits
mapping['¶'] = print_newline

mapping['Ø'] = empty_str_list  # ['']

# unary operators

# these don't print empty strings, use ¶ instead
mapping['.'] = lambda stack : println(stack,'\n')
mapping[','] = lambda stack : println(stack,' ')

mapping['🡔'] = pop
mapping['↑'] = increment
mapping['↓'] = decrement
mapping['¬'] = apply_not
mapping['o'] = make_ord
mapping['!'] = factorial
mapping['ṗ'] = prime
mapping['p'] = is_prime
mapping['L'] = make_list
mapping['l'] = length
mapping['…'] = makeRange0
mapping['┅'] = makeRange1
mapping['ė'] = explode_values
mapping['ẹ'] = implode_values
mapping['ḣ'] = head_list
mapping['ṫ'] = tail_list
mapping['ḥ'] = init_list
mapping['ṭ'] = last_list
mapping['ḷ'] = invert
mapping['Σ'] = make_sum
mapping['Π'] = make_prod
mapping['∧'] = make_all
mapping['∨'] = make_any

# mapping[''] = make_uppercase
# mapping[''] = make_lowercase

# binary operators

mapping['↕'] = swap
mapping['+'] = addition
mapping['-'] = subtraction
mapping['*'] = product
mapping['÷'] = quocient
mapping['%'] = module
mapping['/'] = make_fraction
mapping['^'] = power
mapping['B'] = base
mapping['E'] = sci_format
mapping['<'] = less_than
mapping['>'] = greater_than
mapping['≤'] = less_eq_than
mapping['≥'] = greater_eq_than
mapping['='] = equals
mapping['≠'] = different
mapping['|'] = apply_or
mapping['&'] = apply_and
mapping['⊻'] = apply_xor
mapping['c'] = concatenate
mapping['ŀ'] = list_difference

mapping['i'] = index
mapping['î'] = index_pop
mapping['Ḷ'] = make_multiple_list
mapping['ȧ'] = append_list_begin
mapping['ạ'] = append_list_end


# ternary operators

mapping['V'] = vectorized_assign
