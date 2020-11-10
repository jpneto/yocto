# -*- coding: utf-8 -*-

           # 0123456789ABCDEF
codepage = ('0123456789abcdef',  #0
            'ghijklmnopqrstuv',  #1
            'wxyzABCDEFGHIJKL',  #2
            'MNOPQRSTUVWXYZ \n',  #3   
            '¹²³⁴⁵⁶⁷⁸⁹⁰⁺⁼|&¬⊻',  #4  
            '=≠<>≤≥_+-*/÷%^!?',  #5
            ',;.:«»()[]{}’"¶$',  #6 
            '~#§@âäêëîïôöûüÿñ', #7
            'αβγδλνμπρφψω∆ΦΨΩ',  #8
            'ȧċḋėḣṁṅȯṗṙṡṫẇẋẏż',  #9  
            'ạḅḍẹḷṃṇọṛṣṭụṿẉỵẓ',  #A
            'ȦĊḊĖḞḢṀṄȮṖṘṠṪẆẎŻ',  #C
            'ẠḄḌẸḤḲḶṂṆỌṚṢṬẈỴẒ',  #B
            '🡔🡕🡖🡗↑↓→←↕↔⮆⮄⮅⮇↻↺',#D
            'ΠΣ∧∨⊂⊃∪∩∊…┅əØ×∞½',#E  
            '‼⁇¿¡▷∇◁◻⊢⊤⊣⊥⊨Ŀŀ¤',  #F
            )

codepage= ''.join(codepage)

def toChr(n):
  return codepage[n%256]

def toOrd(c):
  return codepage.index(c)