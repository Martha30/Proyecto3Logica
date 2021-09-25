# LIBRERÍAS
import ply.lex as lex
import ply.yacc as yacc

# DICCIONARIO
temp = {}

# LISTADO DE TOKENS QUE SE ASIGNARÁN A CADA VARIABLE
tokens = (
    'VAR',
    'LNOT',
    'LAND',
    'LOR',
    'LCON',
    'LBI',
    'C1',
    'C2',
    'LEQUALS',
    'T',
    'F'
)

# VALOR DE CADA TOKEN QUE SE ASIGNÓ PREVIAMENTE
t_LNOT = r'\~'
t_LAND = r'\^'
t_LOR = r'\|'
t_LCON = r'\=>'
t_LBI = r'\<=>'
t_C1 = r'\('
t_C2 = r'\)'
t_LEQUALS = r'\='

# VALORES IGNORADOS PARA NO OCASIONAR NINGÚN PROBLEMA
t_ignore = r' '

# PRODUCCIONES

# # VARIABLES
def t_VAR(t):
  r"pqrstuvwxyz"
  return 'VAR'

# CONSTANTES
def t_T(t):
    # SINTAXIS DE OPERACIOENS PARA EXPRESIONES REGULARES
    r'1'
    if t.num == '1':
        return True

# CONSTANTES
def t_F(t):
    # SINTAXIS DE OPERACIOENS PARA EXPRESIONES REGULARES
    r'0'
    if t.num == '0':
        return False

# MANEJO DE ERROR EN CARACTERES
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# PARA QUE NO SE TENGA AMBIGUEDAD AL MOMENTO DEL LEXER HACER SU FUNCIÓN O BIEN SU CONVENCIÓN
precedence = (
    ('left', 'LBI'),
    ('left', 'LCON'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'LNOT'),
    ('left', 'C1')
)

def p_expresion_logica(t):
    '''expresion : expresion LAND expresion
                 | expresion LOR expresion
                 | expresion LCON expresion
                 | expresion LBI expresion'''
    #   ^            ^        ^     ^
    #   |            |        |     |
    #  t[0]         t[1]     t[2]  t[3]
    # ORDEN EN QUE LOS REGRESARÁ
    if (t[2] == '^'): t[0] = (t[2], t[1], t[3])
    elif (t[2] == '|'): t[0] = (t[2], t[1], t[3])
    elif (t[2] == '=>'): t[0] = (t[2], t[1], t[3])
    elif (t[2] == '<=>'): t[0] = (t[2], t[1], t[3])

def p_expresion_cnt(t):
    'expresion : C1 expresion C2'
    t[0] = t[2]

def p_expresion_negacion(t):
    '''
    expresion : LNOT T
              | LNOT F
              | LNOT expresion
    '''

    t[0] = (t[1], t[2])

def p_sintaxis(t):
    'sintaxis : VAR LEQUALS expresion'
    temp[t[1]] = t[3]
    print(run(t[1]))

# MANEJO DE ERRORES DE TIPO SINTÁCTICO
def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

out = yacc.yacc()

def run(p):
    if type(p) == tuple:
       
        global temp
        
        if p[0] == '=>':
            p_1 = run(p[1])
            p_2 = run(p[2])
            
            if p_1 == True and p_2 == False:
                return False
            
            return True
        elif p[0] == '<=>':
            p_1 = run(p[1])
            p_2 = run(p[2])
            
            if p_1 == p_2:
                return True
            
            return False
        elif p[0] == '^':
            return (run(p[1]) and run(p[2]))
        elif p[0] == '|':
            return (run(p[1]) or run(p[2]))
        elif p[0] == '~':
            return not run(p[1])
        elif p[0] == '=':
            temp[p[1]] = run(p[2])
        elif p[0] == 'var':
            if p[1] not in temp:
                return 'Undeclared variable.'
            else:
                return temp[p[1]]
    else:
        return p


while True:
    try:
        s = input('INGRESAR GRAMÁTICA >>> ')
    except EOFError:
        break

    out.parse(s)
