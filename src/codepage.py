# -*- coding: utf-8 -*-

           # 0123456789ABCDEF
codepage = ('0123456789abcdef',     #0
            'ghijklmnopqrstuv',     #1
            'wxyz ABCDEFGHIJK',     #2
            'LMNOPQRSTUVWXYZ\n',    #3   
            '¹²³⁴⁵⁶⁷⁸⁹⁰⁺⁼|&¬⊻',     #4  
            '=≠<>≤≥_+-*/÷%^!?',     #5
            ',;.:«»()[]{}’"¨$',     #6 
            '~#§@âäêëîïôöûüÿñ',     #7
            'αβγδλνμπρφψω∆ΦΨΩ',     #8
            'ȧċḋėḣṁṅȯṗṙṡṫẇẋẏż',     #9  
            'ạḅḍẹḥṃṇọṛṣṭụṿẉỵẓ',     #A
            'ȦĊḊĖḞḢṀṄȮṖṘṠṪẆẎŻ',     #B
            'ẠḄḌẸḤḲḶṂṆỌṚṢṬẈỴẒ',     #C
            '🡔🡕🡖🡗↑↓→←↕↔⮆⮄⮅⮇↻↺', #D
            'ΠΣ∧∨⊂⊃∪∩∊…┅əØ×∞½', #E  
            '‼⁇¿¡▷∇◁¶⊢⊤⊣⊥ḷĿŀ¤',   #F
            )

codepage= ''.join(codepage)

def toChr(n):
  return codepage[n%256]

def toOrd(c):
  return codepage.index(c)

# not used:
  
#            # 0123456789ABCDEF
# codepage = ('          ab def',     #0
#             'ghijk mn  qrstuv',     #1
#             '    A CD   HIJK ',     #2
#             'MNOPQ STU  X Z \n',    #3   
#             '          ⁺⁼    ',     #4  
#             '                ',     #5
#             ',;  «»()[]     $',     #6 
#             '~ §@âäêë  ôöûüÿñ',     #7
#             'αβγ    πρφψω∆ΦΨΩ',     #8
#             ' ċḋ  ṁṅȯ ṙṡ     ',     #9  
#             ' ḅḍ ḷṃṇọṛṣ ụṿ   ',     #A
#             '  ḊĖḞḢ ṄȮṖ  ṪẆẎ ',     #B
#             ' Ḅ ẸḤḲ ṂṆỌṚṢṬẈỴẒ',     #C
#             '      →← ↔⮆⮄⮅⮇↻↺',  #D
#             '    ⊂⊃∪∩∊    ×∞ ',  #E  
#             '‼ ¿¡▷∇◁ ⊢⊤⊣⊥ Ŀ  ',   #F
#             )  