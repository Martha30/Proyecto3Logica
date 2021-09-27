"""UNIVERSIDAD DEL VALLE DE GUATEMALA 
 * LOGICA MATEMÁTICA 
 * RESULTADOS: PROYECTO 3 - RECONOCEDOR DE EXPRESIONES DEL CÁLCULO PROPOSICIONAL
 * File:     Proyecto3.py
 * Input:    Lista de elementos            
 * Output:   Grafo
 *
 * Integrantes:
 *    1. Priscilla González 
 *    2. Martha Gomez 
 *    3. María Mercedes Retolaza 
 *    4. Sebastían Maldonado
 *    5. Julio Herrera
 *
 * Referencias: https://ericknavarro.io/2020/02/10/24-Mi-primer-proyecto-utilizando-PLY/
 *              https://saintuszephir.com/programacion/python/calculadora-en-python-usando
 *              -expresiones-regulares-desde-cero/?amp=1
 *""" 

"""------------------------------------------------------------------------------------"""    

# LIBRERÍAS
import networkx as nx
import ply.lex as lex
import ply.yacc as yacc
import matplotlib.pyplot as plt

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
#pt_P = r'\p'

# VALORES IGNORADOS PARA NO OCASIONAR NINGÚN PROBLEMA
t_ignore = r' '

# VARIABLES
def t_VAR(t):
    r"[pqrstuvwxyz]"
    t.type = 'VAR'
    return t

# MANEJO DE ERROR EN CARACTERES
def t_error(t):
    print("Illegal character '%input'" % t.value[0])
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

def p_gramatica(t):
    '''calcu : expresion'''
    print(t[1])
    print("Valor de la expresión regular: ", calcularE(t[1]))
    print(graficar(t[1]))

# OPERADORES LÓGICOS
def p_expresion_logica(t):
    '''expresion : expresion LAND expresion
                 | expresion LOR expresion
                 | expresion LCON expresion
                 | expresion LBI expresion'''
    #   ^            ^        ^     ^
    #   |            |        |     |
    #  t[0]         t[1]     t[2]  t[3]
    # ORDEN EN QUE LOS REGRESARÁ
    t[0] = (t[2], t[1], t[3])

# PARÉNTESIS
def p_expresion_cnt(t):
    'expresion : C1 expresion C2'
    t[0] = (t[2])

# SOLO MUESTRA VARIABLE
def p_expresion_var(t):
    '''expresion : VAR'''
    t[0] = (t[1])

def p_expresion_negacion(t):
    '''expresion : LNOT T
                 | LNOT F
                 | LNOT expresion'''
    t[0] = (t[1], t[2])

# MANEJO DE ERRORES DE TIPO SINTÁCTICO
def p_error(t):
    print("Error sintáctico en '%input'" % t.value)

parser = yacc.yacc()

# FUNCIÓN PARA GRAFICAR EL NODO
def graficar(t):

    # GRAFICAR UN GRAFO VACÍO DIRIGIDO
    g = nx.DiGraph()
    if type(t) == tuple:
        g.add_node(t[0])

        # SE DIBUJAN TANTO NODOS COMO ARISTAS DEPENDIENDO EL CARACTER
        if type(t[1]) == tuple:
            g.add_node(t[1][0])
            g.add_edge(t[0], t[1][0])
            graphAux1 = graficar(t[1])
            g.add_nodes_from(graphAux1)
            g.add_edges_from(graphAux1.edges())
        else:
            g.add_node(t[1])
            g.add_edge(t[0], t[1])
        
        # AUMENTANDO CADA NODO Y ARISTA DEPENDIENDO DE PARÉNTESIS
        if (len(t) > 2):
            if type(t[2]) == tuple:
                g.add_node(t[2][0])
                g.add_edge(t[0], t[2][0])
                grapAux2 = graficar(t[2])
                g.add_nodes_from(grapAux2)
                g.add_edges_from(grapAux2.edges())
            else:
                g.add_node(t[2])
                g.add_edge(t[0], t[2])

    else:
        g.add_node(t[0])

    # CARACTERÍRCAS DEL GRAFO A DIBUJAR
    grafo = {
          'node_color': '#B2EA0D',
          'node_size': 2000,
          'width': 1,
        }    

    # SE DIBUJA EL GRADO POR PARTES
    plt.subplot(111)
    nx.draw(g, with_labels=True, font_size="12", **grafo)
    plt.show()
    return g

# FUNCIÓN PARA VERIFICAR LAS EXPREIOSNES
def calcularE(t):
    if type(t) == tuple:
        global temp
        if t[0] == '=>':
            temp1 = calcularE(t[1])
            temp2 = calcularE(t[2])
            
            if temp1 == True and temp2 == False:
                return 0

            return 1
        elif t[0] == '<=>':
            temp1 = calcularE(t[1])
            temp2 = calcularE(t[2])
            
            if temp1 == temp2:
                return 0
            
            return 1
        elif t[0] == '^':
            #return (calcularE(t[1]) and calcularE(t[2]))
            temp1 = calcularE(t[1])
            #temp2 = calcularE(t[2])
            
            if temp1 == True:
                return 0
            return 1
        elif t[0] == '|':
            return (calcularE(t[1]) or calcularE(t[2]))
        elif t[0] == '~':
            return not calcularE(t[1])
        elif t[0] == 'var':
            if t[1] not in temp:
                return 'No se declaró dicha variable'
            else:
                return temp[t[1]]
    else:
        return True

# SALIDA
while True:
    try: 
        key = input('INGRESE EXPRESIÓN: ')
    except EOFError:
        break
    parser.parse(key)